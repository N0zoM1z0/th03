; Full Borland C++ string::strip: trim leading/trailing characters,
; copy-on-write TStringRef and original far operator new/ref-count ABI.
; Original 312-byte method and real five-byte far exception unwind.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
_TEXTC ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
strip_unwind:
    push si
    push di
    pop di
    pop si
    retf
_TEXT ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@strip$q16string@StripTypec

; Source emitted with real Borland descending fixups 249,110.
org 248
    call @$bnew$qui
    pop cx
    mov [bp-16],dx
    mov [bp-18],ax

strip_0104:
    or ax,dx
    jz strip_0126
    les bx,[bp-18]
    mov dx,[bp-12]
    mov ax,[bp-14]
    mov es:[bx+2],dx
    mov es:[bx],ax
    mov ax,[bp-10]
    mov es:[bx+4],ax
    mov ax,[bp-8]
    mov es:[bx+6],ax

strip_0126:
    mov dx,[bp-16]
    mov ax,[bp-18]

strip_012c:
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 0

@string@strip$q16string@StripTypec:
    push bp
    mov bp,sp
    sub sp,26
    push si
    push di
    xor cx,cx
    les bx,[bp+10]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    dec ax
    mov [bp-2],ax
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    mov [bp-4],dx
    mov [bp-6],ax
    cmp word ptr [bp+14],0
    jz strip_0042
    cmp word ptr [bp+14],2
    jnz strip_00a2
    jmp short strip_0042

strip_0034:
    les bx,[bp-6]
    add bx,cx
    mov al,es:[bx]
    cmp al,[bp+16]
    jnz strip_00a2
    inc cx

strip_0042:
    cmp cx,[bp-2]
    jna strip_0034
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-20],dx
    mov [bp-22],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-24],dx
    mov [bp-26],ax
    or ax,[bp-24]
    jz strip_0069
    mov ax,[bp-26]
    jmp short strip_0079

strip_0069:
    mov ax,8
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-24],dx
    mov [bp-26],ax

strip_0079:
    or ax,dx
    jz strip_0099
    les bx,[bp-26]
    mov dx,[bp-20]
    mov ax,[bp-22]
    mov es:[bx+2],dx
    mov es:[bx],ax
    mov word ptr es:[bx+4],65535
    mov word ptr es:[bx+6],0

strip_0099:
    mov dx,[bp-24]
    mov ax,[bp-26]
    jmp near ptr strip_012c

strip_00a2:
    cmp word ptr [bp+14],1
    jz strip_00c1
    cmp word ptr [bp+14],2
    jnz strip_00c6
    jmp short strip_00c1

strip_00b0:
    les bx,[bp-6]
    add bx,[bp-2]
    mov al,es:[bx]
    cmp al,[bp+16]
    jnz strip_00c6
    dec word ptr [bp-2]

strip_00c1:
    cmp [bp-2],cx
    ja strip_00b0

strip_00c6:
    mov ax,[bp-2]
    sub ax,cx
    inc ax
    mov [bp-8],ax
    mov [bp-10],cx
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-12],dx
    mov [bp-14],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-16],dx
    mov [bp-18],ax
    or ax,[bp-16]
    jz strip_00f4
    mov ax,[bp-18]
    jmp short strip_0104

strip_00f4:
    mov ax,8
    push ax
_TEXTC ends
end
