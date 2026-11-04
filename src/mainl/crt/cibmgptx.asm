; Original PC-98 IBM get/put text and text-size helpers.
; Full symbolic 8086 CODE, 3 API functions and native screen ABI.
.8086
extrn __wgarbage:word,__wedgectrl:word,__video:byte
extrn __VALIDATEXY:near,__IBM_VPTR:near,__IBM_SCREENIO:near
extrn __IBM_CHECK_DBCS_TRAIL:near,__IBM_FILL_SPACE:near,__IBM_OFF_CURSOR:near
extrn __IBM_SET_CURSOR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___ibm_gettext,___ibm_puttext,___ibm_getputtextsize

; Original public PC-98 text routine CODE+0.
___ibm_gettext:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    cmp byte ptr DGROUP:__video+11, 0
    jne text_0022
    push word ptr [bp + 6]
    push word ptr [bp + 8]
    push word ptr [bp + 0ah]
    push word ptr [bp + 0ch]
    call __VALIDATEXY
    or ax, ax
    jne text_0027
text_0022:
    xor ax, ax
    jmp near ptr text_00dd
text_0027:
    call __IBM_OFF_CURSOR
    mov word ptr [bp - 2], ax
    mov ax, word ptr [bp + 0ah]
    sub ax, word ptr [bp + 6]
    inc ax
    mov word ptr [bp - 4], ax
    cmp word ptr DGROUP:__wedgectrl, 0
    je text_0042
    mov al, 0
    jmp short text_0044
text_0042:
    mov al, 20h
text_0044:
    mov byte ptr [bp - 5], al
    mov ax, word ptr [bp + 8]
    mov word ptr [bp - 8], ax
    jmp short text_00c9
text_004f:
    push word ptr [bp + 10h]
    push word ptr [bp + 0eh]
    push word ptr [bp + 6]
    push word ptr [bp - 8]
    call __IBM_VPTR
    push dx
    push ax
    push word ptr [bp - 4]
    call __IBM_SCREENIO
    cmp word ptr DGROUP:__wgarbage, 0
    jne text_0074
    cmp word ptr DGROUP:__wedgectrl, 0
    je text_00be
text_0074:
    cmp word ptr [bp + 6], 0
    jle text_0094
    mov ax, word ptr [bp + 6]
    dec ax
    push ax
    mov ax, word ptr [bp - 8]
    dec ax
    push ax
    call __IBM_CHECK_DBCS_TRAIL
    or ax, ax
    je text_0094
    les bx,dword ptr [bp + 0eh]
    mov al, byte ptr [bp - 5]
    mov byte ptr es:[bx], al
text_0094:
    mov al, byte ptr DGROUP:__video+10
    mov ah, 0
    cmp ax, word ptr [bp + 0ah]
    jle text_00be
    push word ptr [bp + 0ah]
    mov ax, word ptr [bp - 8]
    dec ax
    push ax
    call __IBM_CHECK_DBCS_TRAIL
    or ax, ax
    je text_00be
    mov ax, word ptr [bp - 4]
    dec ax
    add ax, ax
    les bx,dword ptr [bp + 0eh]
    add bx, ax
    mov al, byte ptr [bp - 5]
    mov byte ptr es:[bx], al
text_00be:
    mov ax, word ptr [bp - 4]
    add ax, ax
    add word ptr [bp + 0eh], ax
    inc word ptr [bp - 8]
text_00c9:
    mov ax, word ptr [bp - 8]
    cmp ax, word ptr [bp + 0ch]
    jg text_00d4
    jmp near ptr text_004f
text_00d4:
    push word ptr [bp - 2]
    call __IBM_SET_CURSOR
    mov ax, 1
text_00dd:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public PC-98 text routine CODE+227.
___ibm_puttext:
    push bp
    mov bp, sp
    sub sp, 10h
    push si
    push di
    cmp byte ptr DGROUP:__video+11, 0
    jne text_0105
    push word ptr [bp + 6]
    push word ptr [bp + 8]
    push word ptr [bp + 0ah]
    push word ptr [bp + 0ch]
    call __VALIDATEXY
    or ax, ax
    jne text_010a
text_0105:
    xor ax, ax
    jmp near ptr text_0209
text_010a:
    call __IBM_OFF_CURSOR
    mov word ptr [bp - 10h], ax
    mov ax, word ptr [bp + 0ah]
    sub ax, word ptr [bp + 6]
    inc ax
    mov word ptr [bp - 4], ax
    mov ax, word ptr [bp + 8]
    mov word ptr [bp - 2], ax
    jmp near ptr text_01f5
text_0123:
    mov ax, word ptr [bp + 6]
    mov word ptr [bp - 6], ax
    mov ax, word ptr [bp + 0ah]
    mov word ptr [bp - 8], ax
    mov ax, word ptr [bp - 4]
    mov word ptr [bp - 0ah], ax
    mov dx, word ptr [bp + 10h]
    mov ax, word ptr [bp + 0eh]
    mov word ptr [bp - 0ch], dx
    mov word ptr [bp - 0eh], ax
    cmp word ptr DGROUP:__wgarbage, 0
    jne text_014b
    jmp near ptr text_01cd
text_014b:
    cmp word ptr DGROUP:__wedgectrl, 0
    je text_017c
    mov ax, word ptr [bp - 4]
    dec ax
    add ax, ax
    les bx,dword ptr [bp + 0eh]
    add bx, ax
    cmp byte ptr es:[bx], 0
    jne text_0169
    dec word ptr [bp - 8]
    dec word ptr [bp - 0ah]
text_0169:
    les bx,dword ptr [bp + 0eh]
    cmp byte ptr es:[bx], 0
    jne text_017c
    inc word ptr [bp - 6]
    dec word ptr [bp - 0ah]
    add word ptr [bp - 0eh], 2
text_017c:
    cmp word ptr [bp - 0ah], 0
    jle text_01cd
    mov al, byte ptr DGROUP:__video+10
    mov ah, 0
    cmp ax, word ptr [bp - 8]
    jle text_01a7
    push word ptr [bp - 8]
    mov ax, word ptr [bp - 2]
    dec ax
    push ax
    call __IBM_CHECK_DBCS_TRAIL
    or ax, ax
    je text_01a7
    push word ptr [bp - 8]
    mov al, byte ptr [bp - 2]
    add al, 0ffh
    push ax
    call __IBM_FILL_SPACE
text_01a7:
    cmp word ptr [bp - 6], 0
    jle text_01cd
    mov ax, word ptr [bp - 6]
    dec ax
    push ax
    mov ax, word ptr [bp - 2]
    dec ax
    push ax
    call __IBM_CHECK_DBCS_TRAIL
    or ax, ax
    je text_01cd
    mov al, byte ptr [bp - 6]
    add al, 0feh
    push ax
    mov al, byte ptr [bp - 2]
    add al, 0ffh
    push ax
    call __IBM_FILL_SPACE
text_01cd:
    cmp word ptr [bp - 0ah], 0
    jle text_01ea
    push word ptr [bp - 6]
    push word ptr [bp - 2]
    call __IBM_VPTR
    push dx
    push ax
    push word ptr [bp - 0ch]
    push word ptr [bp - 0eh]
    push word ptr [bp - 0ah]
    call __IBM_SCREENIO
text_01ea:
    mov ax, word ptr [bp - 4]
    add ax, ax
    add word ptr [bp + 0eh], ax
    inc word ptr [bp - 2]
text_01f5:
    mov ax, word ptr [bp - 2]
    cmp ax, word ptr [bp + 0ch]
    jg text_0200
    jmp near ptr text_0123
text_0200:
    push word ptr [bp - 10h]
    call __IBM_SET_CURSOR
    mov ax, 1
text_0209:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original public PC-98 text routine CODE+527.
___ibm_getputtextsize:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 0ah]
    sub ax, word ptr [bp + 6]
    inc ax
    mov dx, word ptr [bp + 0ch]
    sub dx, word ptr [bp + 8]
    inc dx
    imul dx
    add ax, ax
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
