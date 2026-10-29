; DOS overlay execution. A copied load/transfer continuation runs from the top
; of the retained DOS block after runtime cleanup. Buffer addresses within that
; copy are relative to overlay_area, not link-time CS offsets.
.8086
extrn __cexit:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT
extrn __IOERROR:near
_TEXT ends
_DATA segment word public 'DATA'
extrn __envseg:word
_DATA ends
_TEXT segment byte public 'CODE'
extrn DGROUP@:word
_TEXT ends
_DATA segment word public 'DATA'
extrn __psp:word,__version:byte
_DATA ends
DGROUP group _DATA

_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __exec

; The temporary stack occupies the lower buffer; its original odd top is
; intentional. PSP, pathname, FCB results, MZ header and overlay parameters
; are real work fields with no source initializers.
overlay_area label byte
overlay_stack db 143 dup (?)
overlay_psp dw ?
program_path db 80 dup (?)
fcb_first db ?
fcb_second db ?
image_magic dw ?
image_last_bytes dw ?
image_pages dw ?
image_reloc_count dw ?
image_header_paras dw ?
image_min_extra dw ?
image_max_extra dw ?
image_ss dw ?
image_sp dw ?
image_checksum dw ?
image_ip dw ?
image_cs dw ?
load_segment dw ?
relocation_segment dw ?

; Copied continuation, entered with CX environment segment and DX block end.
; DI zero makes every work-field reference relative to the relocated copy.
overlay_load:
    xor di,di
    mov ax,cs
    mov ds,ax
    mov es,ax
    cli
    mov ss,ax
    lea sp,[di+(overlay_psp-overlay_area)]
    sti
    push cx
    push dx
    mov ax,4b03h
    lea bx,[di+(load_segment-overlay_area)]
    lea dx,[di+(program_path-overlay_area)]
    int 21h
    pop dx
    pop cx
    jc overlay_failed
    xor di,di
    cli
    mov ss,word ptr [di+(image_ss-overlay_area)]
    mov sp,word ptr [di+(image_sp-overlay_area)]
    sti
    mov bp,sp
    xor ax,ax
    push ax
    mov ax,word ptr [di+(overlay_psp-overlay_area)]
    mov ds,ax
    mov es,ax
    mov word ptr es:[2],dx
    mov word ptr es:[2ch],cx
    mov ax,word ptr cs:[di+(fcb_first-overlay_area)]
    jmp dword ptr cs:[image_ip-overlay_area]
overlay_failed:
    ; Preserve the original write of15 bytes at the copied buffer start.
    ; There is no initialized error string in the original object.
    mov ah,40h
    mov bx,2
    mov cx,15
    xor dx,dx
    int 21h
    mov ax,4c02h
    int 21h
overlay_copy_end label byte

; Relative IP belongs to the copy. The segment is filled before transfer.
transfer_target dw overlay_load-overlay_area,0
saved_environment dw ?
reuse_environment db 1

; Near cdecl __exec(filename far*, command-tail far*, environment far*).
; BP-2 handle, BP-4 retained paragraphs, BP-6 environment paragraphs,
; BP-10/-8 environment source pointer, BP-12 old PSP environment segment.
__exec proc near
    push bp
    mov bp,sp
    sub sp,12
    cld
    push si
    push ds
    push di
    push es
    mov ax,__envseg
    mov cs:saved_environment,ax
    mov ax,3d00h
    push ds
    lds dx,[bp+4]
    int 21h
    pop ds
    mov [bp-2],ax
    jnc file_opened
    jmp execution_error
file_opened:
    mov es,__psp
    mov cs:overlay_psp,es
    mov ax,word ptr es:[2ch]
    mov [bp-12],ax
    mov di,80h
    push ds
    lds si,[bp+8]
    lodsb
    mov dx,si
    stosb
    xor cx,cx
    mov cl,al
    inc cx
    rep movsb
    mov ax,2901h
    mov si,dx
    mov di,5ch
    int 21h
    mov cs:fcb_first,al
skip_first_argument:
    mov al,[si]
    cmp al,' '
    je parse_second_fcb
    cmp al,9
    je parse_second_fcb
    cmp al,13
    je parse_second_fcb
    inc si
    jmp short skip_first_argument
parse_second_fcb:
    mov ax,2901h
    mov di,6ch
    int 21h
    mov cs:fcb_second,al
    pop ds
    mov ah,4ah
    mov bx,-1
    int 21h
    cmp __version,3
    jae available_paragraphs
    sub bx,280h
available_paragraphs:
    mov [bp-4],bx
    mov ax,[bp+12]
    mov dx,[bp+14]
    mov bx,ax
    or bx,dx
    jne count_environment
    xor ax,ax
    mov di,ax
    jmp short environment_counted
count_environment:
    mov es,dx
    mov di,ax
    push di
    mov cx,-1
    xor ax,ax
environment_string:
    repne scasb
    cmp byte ptr es:[di],al
    jne environment_string
    dec cx
    add di,3
    repne scasb
    dec cx
    mov ax,cx
    neg ax
    pop di
environment_counted:
    mov [bp-10],di
    mov [bp-8],es
    add ax,15
    mov cx,4
    shr ax,cl
    mov [bp-6],ax
    mov si,__envseg
    dec si
    mov es,si
    cmp ax,word ptr es:[3]
    jbe environment_fits
    dec cs:reuse_environment
    inc ax
    sub [bp-4],ax
environment_fits:
    lds si,[bp+4]
    push cs
    pop es
    mov di,offset program_path
copy_filename:
    lodsb
    stosb
    or al,al
    jne copy_filename
    mov bx,[bp-2]
    push ds
    pop es
    push cs
    pop ds
    mov di,offset overlay_area
    mov ah,3fh
    mov cx,24
    lea dx,[di+(image_magic-overlay_area)]
    int 21h
    jc close_error
    cmp word ptr [di+(image_magic-overlay_area)],('M' OR ('Z' SHL 8))
    je prepare_mz
    mov ax,word ptr es:[si-5]
    or ah,20h
    cmp ax,('.' OR ('c' SHL 8))
    jne invalid_image
    mov ax,word ptr es:[si-3]
    or ax,2020h
    cmp ax,('o' OR ('m' SHL 8))
    jne invalid_image
    jmp short prepare_com
invalid_image:
    mov ax,11
close_error:
    push ax
    mov ah,3eh
    mov bx,[bp-2]
    int 21h
    pop ax
    jmp execution_error
prepare_mz:
    mov ax,word ptr [di+(image_pages-overlay_area)]
    xor dx,dx
    mov dl,ah
    mov ah,al
    xor al,al
    shl ax,1
    rcl dx,1
    add ax,word ptr [di+(image_last_bytes-overlay_area)]
    adc dx,0
    mov cx,4
mz_paragraphs:
    shr dx,1
    rcr ax,1
    loop mz_paragraphs
    inc ax
    sub ax,word ptr [di+(image_header_paras-overlay_area)]
    add ax,word ptr [di+(image_min_extra-overlay_area)]
    xchg ax,bx
    mov ax,word ptr [di+(overlay_psp-overlay_area)]
    add ax,10h
    add word ptr [di+(image_cs-overlay_area)],ax
    add word ptr [di+(image_ss-overlay_area)],ax
    xchg ax,bx
    jmp short prepare_load_parameters
prepare_com:
    mov ax,4202h
    xor cx,cx
    xor dx,dx
    int 21h
    mov cx,4
com_paragraphs:
    shr dx,1
    rcr ax,1
    loop com_paragraphs
    inc ax
    xchg ax,bx
    mov ax,word ptr [di+(overlay_psp-overlay_area)]
    mov word ptr [di+(image_cs-overlay_area)],ax
    mov word ptr [di+(image_ip-overlay_area)],100h
    mov word ptr [di+(image_ss-overlay_area)],ax
    add ax,10h
    xchg ax,bx
prepare_load_parameters:
    mov word ptr [di+(load_segment-overlay_area)],bx
    mov word ptr [di+(relocation_segment-overlay_area)],bx
    add ax,16h
    cmp ax,[bp-4]
    mov ax,8
    jbe close_image
    jmp close_error
close_image:
    mov ah,3eh
    mov bx,[bp-2]
    int 21h
    mov es,word ptr [di+(overlay_psp-overlay_area)]
    mov ah,4ah
    mov bx,[bp-4]
    int 21h
    jnc dos_block_resized
    jmp close_error
dos_block_resized:
    add bx,word ptr [di+(overlay_psp-overlay_area)]
    mov dx,bx
    sub bx,17h
    mov word ptr cs:transfer_target+2,bx
    mov es,bx
    mov cx,(overlay_copy_end-overlay_area)/2
    mov si,offset overlay_area
    xor di,di
    rep movsw
    mov es,[bp-12]
    mov cx,[bp-6]
    cmp cs:reuse_environment,0
    jne reuse_old_environment
    mov ah,48h
    mov bx,cx
    int 21h
    jc execution_error
    jmp short copy_environment
reuse_old_environment:
    mov ax,cs:saved_environment
copy_environment:
    mov es,ax
    xor di,di
    lds si,[bp-10]
    add cx,cx
    add cx,cx
    add cx,cx
    rep movsw
    push es
    push dx
    push ds
    ; DGROUP@ is the real CS-resident startup word containing DGROUP.
    mov ds,cs:DGROUP@
    call __cexit
    pop ds
    pop dx
    cmp cs:reuse_environment,0
    jne transfer_overlay
    mov es,cs:saved_environment
    mov ah,49h
    int 21h
transfer_overlay:
    pop cx
    jmp dword ptr cs:transfer_target
execution_error:
    pop es
    pop di
    pop ds
    pop si
    push ax
    call __IOERROR
    mov sp,bp
    pop bp
    ret
__exec endp
_TEXT ends
end
