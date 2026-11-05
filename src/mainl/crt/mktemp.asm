; Original Japanese Borland CRT _mktemp, not a modern POSIX mkstemp.
; The real template is the six-byte initialized DATA string XXXXXX.
; The original enumerates five letters around a fixed dot and checks DOS
; accessibility, using far string pointers and 16-bit Borland calling ABI.
.8086
extrn _strcmp:far,_strlen:far,_access:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _mktemp
_mktemp proc far
    push bp
    mov bp,sp
    sub sp,14
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _strlen
    pop cx
    pop cx
    mov bx,ax
    cmp bx,6
    jnl short valid_length
    jmp near ptr exhausted
valid_length:
    mov dx,[bp+8]
    mov ax,[bp+6]
    add ax,bx
    add ax,0fffah
    mov [bp-2],dx
    mov [bp-4],ax
    push ds
    mov ax,offset DGROUP:mktemp_template
    push ax
    push dx
    push word ptr [bp-4]
    call _strcmp
    add sp,8
    or ax,ax
    jz short valid_template
    jmp near ptr exhausted
valid_template:
    les bx,dword ptr [bp-4]
    mov byte ptr es:[bx+2],'.'
    mov word ptr [bp-6],'A'
    jmp near ptr check_first
set_first:
    les bx,dword ptr [bp-4]
    mov al,[bp-6]
    mov byte ptr es:[bx],al
    mov word ptr [bp-8],'A'
    jmp short check_second
set_second:
    les bx,dword ptr [bp-4]
    mov al,[bp-8]
    mov byte ptr es:[bx+1],al
    mov word ptr [bp-10],'A'
    jmp short check_third
set_third:
    les bx,dword ptr [bp-4]
    mov al,[bp-10]
    mov byte ptr es:[bx+3],al
    mov word ptr [bp-12],'A'
    jmp short check_fourth
set_fourth:
    les bx,dword ptr [bp-4]
    mov al,[bp-12]
    mov byte ptr es:[bx+4],al
    mov word ptr [bp-14],'A'
    jmp short check_fifth
set_fifth:
    les bx,dword ptr [bp-4]
    mov al,[bp-14]
    mov byte ptr es:[bx+5],al
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _access
    add sp,6
    cmp ax,0ffffh
    jnz short next_fifth
    mov dx,[bp+8]
    mov ax,[bp+6]
    jmp short done
next_fifth:
    inc word ptr [bp-14]
check_fifth:
    cmp word ptr [bp-14],'Z'
    jng short set_fifth
    inc word ptr [bp-12]
check_fourth:
    cmp word ptr [bp-12],'Z'
    jng short set_fourth
    inc word ptr [bp-10]
check_third:
    cmp word ptr [bp-10],'Z'
    jng short set_third
    inc word ptr [bp-8]
check_second:
    cmp word ptr [bp-8],'Z'
    jng short set_second
    inc word ptr [bp-6]
check_first:
    cmp word ptr [bp-6],'Z'
    jg short exhausted
    jmp near ptr set_first
exhausted:
    xor dx,dx
    xor ax,ax
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_mktemp endp
_TEXT ends
_DATA segment word public 'DATA'
mktemp_template db 'XXXXXX',0
_DATA ends
end
