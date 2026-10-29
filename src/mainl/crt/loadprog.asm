; Program resolution and DOS command/environment preparation. The final target
; is a near callback taking three far pointers, matching the overlay executor.
.8086
include crt_errno.inc
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
extrn __exitbuf:dword
_DATA ends
extrn __DOSCMD:near,__DOSENV:near
extrn _free:far,_getenv:far
_DATA segment word public 'DATA'
extrn __environ:dword
_DATA ends
extrn __searchenv:far
_DATA segment word public 'DATA'
extrn _errno:word
_DATA ends
extrn __access:far,_strcat:far,_strcpy:far,_strlen:far,_stricmp:far,_strrchr:far,___path_isdbcsleadbyte:far

_DATA segment word public 'DATA'
path_variable db 'PATH',0
path_separators db '/',5ch,0
empty_suffix db 0
batch_compare_suffix db '.BAT',0
com_suffix db '.COM',0
exe_suffix db '.EXE',0
batch_probe_suffix db '.BAT',0
shell_variable db 'COMSPEC',0
shell_switch db '/c',0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA

_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __LoadProg

; Far cdecl delimiter scan. Skip the trail byte of a DBCS character; an
; unmatched final lead byte returns null. Offset increments remain16-bit.
find_path_separator proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short separator_test
separator_character:
    les bx,[bp-4]
    mov al,es:[bx]
    push ax
    call ___path_isdbcsleadbyte
    pop cx
    or ax,ax
    je separator_delimiters
    inc word ptr [bp-4]
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jne separator_advance
    jmp short separator_absent
separator_delimiters:
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-6],dx
    mov [bp-8],ax
    jmp short delimiter_test
delimiter_compare:
    les bx,[bp-4]
    mov al,es:[bx]
    les bx,[bp-8]
    cmp al,es:[bx]
    je delimiter_done
    inc word ptr [bp-8]
delimiter_test:
    les bx,[bp-8]
    cmp byte ptr es:[bx],0
    jne delimiter_compare
delimiter_done:
    les bx,[bp-8]
    cmp byte ptr es:[bx],0
    je separator_advance
    mov dx,[bp-2]
    mov ax,[bp-4]
    jmp short separator_done
separator_advance:
    inc word ptr [bp-4]
separator_test:
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jne separator_character
separator_absent:
    xor dx,dx
    xor ax,ax
separator_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
find_path_separator endp

; Far cdecl probe(name,result,extension,search_path). The80-byte candidate
; buffer and unchecked concatenation are original; do not add truncation.
probe_program proc far
    push bp
    mov bp,sp
    sub sp,80
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ss
    lea ax,[bp-80]
    push ax
    call _strcpy
    push word ptr [bp+16]
    push word ptr [bp+14]
    push ss
    lea ax,[bp-80]
    push ax
    call _strcat
    add sp,16
    cmp word ptr [bp+18],0
    je probe_direct
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ds
    mov ax,offset DGROUP:path_variable
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    call __searchenv
    add sp,12
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    je probe_missing
    jmp short probe_present
probe_direct:
    push ss
    lea ax,[bp-80]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    call _strcpy
    add sp,8
    mov ax,4
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    call __access
    add sp,6
    or ax,ax
    jne probe_missing
probe_present:
    mov ax,1
    jmp short probe_done
probe_missing:
    xor ax,ax
probe_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
probe_program endp

; Near cdecl __LoadProg(callback,name far*,argv far*,envp far*,search_path).
; The156-byte frame contains a128-byte resolved path plus28 bytes of pointer,
; flag and result locals. Keep the original deferred argument-stack cleanup.
__LoadProg proc near
    push bp
    mov bp,sp
    sub sp,156
    push si
    push di
    les bx,[bp+6]
    mov al,es:[bx]
    cbw
    mov dx,ax
    cmp ax,'a'
    jb drive_folded
    sub dx,32
drive_folded:
    cmp dx,'A'
    jb check_separators
    cmp dx,'Z'
    ja check_separators
    les bx,[bp+6]
    cmp byte ptr es:[bx+1],':'
    je disable_path_search
check_separators:
    push ds
    mov ax,offset DGROUP:path_separators
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call find_path_separator
    add sp,8
    or ax,dx
    je search_mode_ready
disable_path_search:
    mov word ptr [bp+18],0
search_mode_ready:
    mov word ptr [bp-26],0
    mov ax,'.'
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _strrchr
    add sp,6
    mov [bp-14],dx
    mov [bp-16],ax
    or ax,dx
    je probe_extensions
    push word ptr [bp+18]
    push ds
    mov ax,offset DGROUP:empty_suffix
    push ax
    push ss
    lea ax,[bp-156]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call probe_program
    add sp,14
    mov [bp-24],ax
    or ax,ax
    jne check_explicit_batch
    jmp program_probed
check_explicit_batch:
    push ds
    mov ax,offset DGROUP:batch_compare_suffix
    push ax
    push word ptr [bp-14]
    push word ptr [bp-16]
    call _stricmp
    add sp,8
    or ax,ax
    jne program_probed
    jmp short mark_batch
probe_extensions:
    push word ptr [bp+18]
    push ds
    mov ax,offset DGROUP:com_suffix
    push ax
    push ss
    lea ax,[bp-156]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call probe_program
    add sp,14
    mov [bp-24],ax
    or ax,ax
    jne program_probed
    push word ptr [bp+18]
    push ds
    mov ax,offset DGROUP:exe_suffix
    push ax
    push ss
    lea ax,[bp-156]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call probe_program
    add sp,14
    mov [bp-24],ax
    or ax,ax
    jne program_probed
    push word ptr [bp+18]
    push ds
    mov ax,offset DGROUP:batch_probe_suffix
    push ax
    push ss
    lea ax,[bp-156]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call probe_program
    add sp,14
    mov [bp-24],ax
    or ax,ax
    je program_probed
mark_batch:
    mov word ptr [bp-26],1
program_probed:
    cmp word ptr [bp-24],0
    je program_missing
    cmp word ptr [bp-26],0
    je prepare_command
    push ds
    mov ax,offset DGROUP:shell_variable
    push ax
    call _getenv
    pop cx
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jne prepare_command
program_missing:
    mov _errno,ENOENT
    jmp load_failed
prepare_command:
    cmp word ptr [bp-26],0
    je prepare_direct_command
    push word ptr [bp-2]
    push word ptr [bp-4]
    push ds
    mov ax,offset DGROUP:shell_switch
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    jmp short make_command
prepare_direct_command:
    push ss
    lea ax,[bp-156]
    push ax
    xor ax,ax
    push ax
    push ax
    mov ax,[bp+10]
    add ax,4
    push word ptr [bp+12]
    push ax
make_command:
    call __DOSCMD
    mov [bp-6],dx
    mov [bp-8],ax
    mov ax,[bp-8]
    or ax,[bp-6]
    jne command_created
    mov _errno,ENOMEM
    jmp load_failed
command_created:
    mov ax,[bp-8]
    inc ax
    push word ptr [bp-6]
    push ax
    call _strlen
    pop cx
    pop cx
    cmp ax,128
    jb command_length_valid
    mov _errno,E2BIG
    push word ptr [bp-6]
    push word ptr [bp-8]
    call _free
    pop cx
    pop cx
    jmp short load_failed
command_length_valid:
    mov ax,[bp+14]
    or ax,[bp+16]
    jne environment_ready
    mov dx,word ptr __environ+2
    mov ax,word ptr __environ
    mov [bp+16],dx
    mov [bp+14],ax
environment_ready:
    push word ptr [bp+16]
    push word ptr [bp+14]
    cmp word ptr [bp-26],0
    je direct_environment_name
    mov dx,[bp-2]
    mov ax,[bp-4]
    jmp short environment_name_ready
direct_environment_name:
    mov dx,ss
    lea ax,[bp-156]
environment_name_ready:
    push dx
    push ax
    push ss
    lea ax,[bp-20]
    push ax
    call __DOSENV
    mov [bp-10],dx
    mov [bp-12],ax
    or ax,dx
    jne execute_prepared
    mov _errno,ENOMEM
    push word ptr [bp-6]
    push word ptr [bp-8]
    call _free
    pop cx
    pop cx
load_failed:
    mov ax,-1
    jmp short load_done
execute_prepared:
    call dword ptr __exitbuf
    push word ptr [bp-10]
    push word ptr [bp-12]
    push word ptr [bp-6]
    push word ptr [bp-8]
    cmp word ptr [bp-26],0
    je direct_execution_name
    mov dx,[bp-2]
    mov ax,[bp-4]
    jmp short execution_name_ready
direct_execution_name:
    mov dx,ss
    lea ax,[bp-156]
execution_name_ready:
    push dx
    push ax
    call word ptr [bp+4]
    add sp,12
    mov [bp-22],ax
    push word ptr [bp-18]
    push word ptr [bp-20]
    call _free
    push word ptr [bp-6]
    push word ptr [bp-8]
    call _free
    add sp,8
    mov ax,[bp-22]
load_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    ret
__LoadProg endp
_TEXT ends

end
