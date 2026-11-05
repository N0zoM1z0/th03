; Original Borland TStringRef(char, unsigned int) C++ constructor.
; Allocates the 12-byte object, rounds capacity, initializes the
; owning FAR character buffer, terminates it and updates global
; reference destructor count. All original unchecked paths retained.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn _memset:far
extrn _malloc:far
extrn @xalloc@raise$qv:far
extrn @TStringRef@round_capacity$qui:far
extrn ___xalloc:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @TStringRef@$bctr$qcui
@TStringRef@$bctr$qcui proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short object_exists
    mov ax,0ch
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jnz short object_exists
    jmp near ptr constructor_done
object_exists:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],1
    mov word ptr es:[bx+0ah],0
    mov ax,[bp+0ch]
    mov word ptr es:[bx+6],ax
    push word ptr es:[bx+6]
    call @TStringRef@round_capacity$qui
    pop cx
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+8],ax
    mov ax,word ptr es:[bx+8]
    inc ax
    push ax
    call _malloc
    pop cx
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+4],dx
    mov word ptr es:[bx+2],ax
    mov ax,word ptr es:[bx+2]
    or ax,word ptr es:[bx+4]
    jnz short initialize_character_buffer
    push ds
    mov ax,offset DGROUP:___xalloc
    push ax
    call @xalloc@raise$qv
    pop cx
    pop cx
initialize_character_buffer:
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+6]
    mov al,byte ptr [bp+0ah]
    cbw
    push ax
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    call _memset
    add sp,8
    les bx,dword ptr [bp+6]
    les ax,dword ptr es:[bx+2]
    push es
    mov es,word ptr [bp+8]
    add ax,word ptr es:[bx+6]
    mov bx,ax
    pop es
    mov byte ptr es:[bx],0
constructor_done:
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
@TStringRef@$bctr$qcui endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
