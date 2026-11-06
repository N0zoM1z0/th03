; Shared runtime: complete original bytes, ABI and literal ordered fields.
; Ordinary source spans preserve native record chronology; no storage is filled.
; The pinned compatible emitter keeps all actual near/far call distances intact.
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
DGROUP group _DATA,_BSS

_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __LoadProg

; Far cdecl delimiter scan. Skip the trail byte of a DBCS character; an
; unmatched final lead byte returns null. Offset increments remain16-bit.
; Bind original code labels before scheduling their ordinary instruction spans.
org 0
find_path_separator label far
org 22
separator_character label near
org 53
separator_delimiters label near
org 67
delimiter_compare label near
org 84
delimiter_test label near
org 93
delimiter_done label near
org 110
separator_advance label near
org 113
separator_test label near
org 122
separator_absent label near
org 126
separator_done label near
org 132
probe_program label far
; probe(name,result,extension,search_path) keeps an unchecked 80-byte candidate.
org 216
probe_direct label near
org 256
probe_present label near
org 261
probe_missing label near
org 263
probe_done label near
org 269
__LoadProg label near
; Near cdecl callback and three far pointers; preserve deferred stack cleanup.
; BP-156 holds 128-byte resolved path plus 28 bytes of locals.
org 295
drive_folded label near
org 315
check_separators label near
org 337
disable_path_search label near
org 342
search_mode_ready label near
org 412
check_explicit_batch label near
org 437
probe_extensions label near
org 539
mark_batch label near
org 544
program_probed label near
org 578
program_missing label near
org 587
prepare_command label near
org 612
prepare_direct_command label near
org 632
make_command label near
org 658
command_created label near
org 699
command_length_valid label near
org 720
environment_ready label near
org 740
direct_environment_name label near
org 746
environment_name_ready label near
org 785
load_failed label near
org 790
execute_prepared label near
org 820
direct_execution_name label near
org 826
execution_name_ready label near
org 865
load_done label near

; Original CODE 854..870.
org 854
    call _free
    add sp,8
    mov ax,[bp-22]
    pop di
    pop si
    mov sp,bp
    pop bp
    ret

; Original CODE 843..853.
org 843
    call _free
    push word ptr [bp-6]
    push word ptr [bp-8]

; Original CODE 790..842.
org 790
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
    mov dx,ss
    lea ax,[bp-156]
    push dx
    push ax
    call word ptr [bp+4]
    add sp,12
    mov [bp-22],ax
    push word ptr [bp-18]
    push word ptr [bp-20]

; Original CODE 778..789.
org 778
    call _free
    pop cx
    pop cx
    mov ax,-1
    jmp short load_done

; Original CODE 766..777.
org 766
    mov _errno,ENOMEM
    push word ptr [bp-6]
    push word ptr [bp-8]

; Original CODE 753..765.
org 753
    call __DOSENV
    mov [bp-10],dx
    mov [bp-12],ax
    or ax,dx
    jne execute_prepared

; Original CODE 711..752.
org 711
    mov ax,word ptr __environ
    mov [bp+16],dx
    mov [bp+14],ax
    push word ptr [bp+16]
    push word ptr [bp+14]
    cmp word ptr [bp-26],0
    je direct_environment_name
    mov dx,[bp-2]
    mov ax,[bp-4]
    jmp short environment_name_ready
    mov dx,ss
    lea ax,[bp-156]
    push dx
    push ax
    push ss
    lea ax,[bp-20]
    push ax

; Original CODE 707..710.
org 707
    mov dx,word ptr __environ+2

; Original CODE 690..706.
org 690
    call _free
    pop cx
    pop cx
    jmp short load_failed
    mov ax,[bp+14]
    or ax,[bp+16]
    jne environment_ready

; Original CODE 678..689.
org 678
    mov _errno,E2BIG
    push word ptr [bp-6]
    push word ptr [bp-8]

; Original CODE 666..677.
org 666
    call _strlen
    pop cx
    pop cx
    cmp ax,128
    jb command_length_valid

; Original CODE 649..665.
org 649
    mov _errno,ENOMEM
    jmp near ptr load_failed
    mov ax,[bp-8]
    inc ax
    push word ptr [bp-6]
    push ax

; Original CODE 632..648.
org 632
    call __DOSCMD
    mov [bp-6],dx
    mov [bp-8],ax
    mov ax,[bp-8]
    or ax,[bp-6]
    jne command_created

; Original CODE 600..631.
org 600
    mov ax,offset DGROUP:shell_switch
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    jmp short make_command
    push ss
    lea ax,[bp-156]
    push ax
    xor ax,ax
    push ax
    push ax
    mov ax,[bp+10]
    add ax,word ptr 4
    push word ptr [bp+12]
    push ax

; Original CODE 578..599.
org 578
    mov _errno,ENOENT
    jmp near ptr load_failed
    cmp word ptr [bp-26],0
    je prepare_direct_command
    push word ptr [bp-2]
    push word ptr [bp-4]
    push ds

; Original CODE 561..577.
org 561
    call _getenv
    pop cx
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jne prepare_command

; Original CODE 557..560.
org 557
    mov ax,offset DGROUP:shell_variable
    push ax

; Original CODE 509..556.
org 509
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
    mov word ptr [bp-26],1
    cmp word ptr [bp-24],0
    je program_missing
    cmp word ptr [bp-26],0
    je prepare_command
    push ds

; Original CODE 475..508.
org 475
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

; Original CODE 441..474.
org 441
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

; Original CODE 423..440.
org 423
    call _stricmp
    add sp,8
    or ax,ax
    jne program_probed
    jmp short mark_batch
    push word ptr [bp+18]
    push ds

; Original CODE 413..422.
org 413
    mov ax,offset DGROUP:batch_compare_suffix
    push ax
    push word ptr [bp-14]
    push word ptr [bp-16]

; Original CODE 379..412.
org 379
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
    jmp near ptr program_probed
    push ds

; Original CODE 357..378.
org 357
    call _strrchr
    add sp,6
    mov [bp-14],dx
    mov [bp-16],ax
    or ax,dx
    je probe_extensions
    push word ptr [bp+18]
    push ds

; Original CODE 316..356.
org 316
    mov ax,offset DGROUP:path_separators
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call find_path_separator
    add sp,8
    or ax,dx
    je search_mode_ready
    mov word ptr [bp+18],0
    mov word ptr [bp-26],0
    mov ax,'.'
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original CODE 244..315.
org 244
    call __access
    add sp,6
    or ax,ax
    jne probe_missing
    mov ax,1
    jmp short probe_done
    xor ax,ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
    push bp
    mov bp,sp
    sub sp,156
    push si
    push di
    les bx,[bp+6]
    mov al,es:[bx]
    cbw
    mov dx,ax
    cmp ax,word ptr 'a'
    jb drive_folded
    sub dx,32
    cmp dx,'A'
    jb check_separators
    cmp dx,'Z'
    ja check_separators
    les bx,[bp+6]
    cmp byte ptr es:[bx+1],':'
    je disable_path_search
    push ds

; Original CODE 227..243.
org 227
    call _strcpy
    add sp,8
    mov ax,4
    push ax
    push ss
    lea ax,[bp-80]
    push ax

; Original CODE 197..226.
org 197
    call __searchenv
    add sp,12
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    je probe_missing
    jmp short probe_present
    push ss
    lea ax,[bp-80]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]

; Original CODE 188..196.
org 188
    mov ax,offset DGROUP:path_variable
    push ax
    push ss
    lea ax,[bp-80]
    push ax

; Original CODE 167..187.
org 167
    call _strcat
    add sp,16
    cmp word ptr [bp+18],0
    je probe_direct
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ds

; Original CODE 151..166.
org 151
    call _strcpy
    push word ptr [bp+16]
    push word ptr [bp+14]
    push ss
    lea ax,[bp-80]
    push ax

; Original CODE 29..150.
org 29
    call ___path_isdbcsleadbyte
    pop cx
    or ax,ax
    je separator_delimiters
    inc word ptr [bp-4]
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jne separator_advance
    jmp short separator_absent
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-6],dx
    mov [bp-8],ax
    jmp short delimiter_test
    les bx,[bp-4]
    mov al,es:[bx]
    les bx,[bp-8]
    cmp al,es:[bx]
    je delimiter_done
    inc word ptr [bp-8]
    les bx,[bp-8]
    cmp byte ptr es:[bx],0
    jne delimiter_compare
    les bx,[bp-8]
    cmp byte ptr es:[bx],0
    je separator_advance
    mov dx,[bp-2]
    mov ax,[bp-4]
    jmp short separator_done
    inc word ptr [bp-4]
    les bx,[bp-4]
    cmp byte ptr es:[bx],0
    jne separator_character
    xor dx,dx
    xor ax,ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
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

; Original CODE 0..28.
org 0
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
    les bx,[bp-4]
    mov al,es:[bx]
    push ax
_TEXT ends

end
