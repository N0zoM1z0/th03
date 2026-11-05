; Full original Japanese Borland CRT 10-API multibyte character classification.
; True near/far CTYPE/MBCTYPE masks, actual 8086 instructions, exact public ABI.
.8086
extrn __ctype:byte,__mbctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __ismbbkalpha
public __ismbbkpunct
public __ismbbkana
public __ismbbalpha
public __ismbbpunct
public __ismbbalnum
public __ismbbprint
public __ismbbgraph
public __ismbblead
public __ismbbtrail

; Original BCC emits FIXUPPs in descending member CODE order.

org 321

__ismbbtrail:
    push bp
    mov bp,sp
    push si
    push di
    mov al,[bp+6]
    mov ah,0
    mov bx,ax
    mov al,byte ptr DGROUP:__mbctype[bx+1]
    and al,8
    mov ah,0
    pop di
    pop si
    pop bp
    retf

org 297

__ismbblead:
    push bp
    mov bp,sp
    push si
    push di
    mov al,[bp+6]
    mov ah,0
    mov bx,ax
    mov al,byte ptr DGROUP:__mbctype[bx+1]
    and al,4
    mov ah,0
    pop di
    pop si
    pop bp
    retf

org 279
    test byte ptr DGROUP:__mbctype[bx+1],3
    jz mbbis_0123

mbbis_011e:
    mov ax,1
    jmp short mbbis_0125

mbbis_0123:
    xor ax,ax

mbbis_0125:
    pop di
    pop si
    pop bp
    retf

org 266
    test byte ptr DGROUP:__ctype[bx+1],94
    jnz mbbis_011e
    mov al,dl
    mov ah,0
    mov bx,ax

org 252

__ismbbgraph:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    mov al,dl
    mov ah,0
    mov bx,ax

org 234
    test byte ptr DGROUP:__mbctype[bx+1],3
    jz mbbis_00f6

mbbis_00f1:
    mov ax,1
    jmp short mbbis_00f8

mbbis_00f6:
    xor ax,ax

mbbis_00f8:
    pop di
    pop si
    pop bp
    retf

org 221
    test byte ptr DGROUP:__ctype[bx+1],222
    jnz mbbis_00f1
    mov al,dl
    mov ah,0
    mov bx,ax

org 207

__ismbbprint:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    mov al,dl
    mov ah,0
    mov bx,ax

org 189
    test byte ptr DGROUP:__mbctype[bx+1],1
    jz mbbis_00c9

mbbis_00c4:
    mov ax,1
    jmp short mbbis_00cb

mbbis_00c9:
    xor ax,ax

mbbis_00cb:
    pop di
    pop si
    pop bp
    retf

org 176
    test byte ptr DGROUP:__ctype[bx+1],14
    jnz mbbis_00c4
    mov al,dl
    mov ah,0
    mov bx,ax

org 162

__ismbbalnum:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    mov al,dl
    mov ah,0
    mov bx,ax

org 144
    test byte ptr DGROUP:__mbctype[bx+1],2
    jz mbbis_009c

mbbis_0097:
    mov ax,1
    jmp short mbbis_009e

mbbis_009c:
    xor ax,ax

mbbis_009e:
    pop di
    pop si
    pop bp
    retf

org 131
    test byte ptr DGROUP:__ctype[bx+1],64
    jnz mbbis_0097
    mov al,dl
    mov ah,0
    mov bx,ax

org 117

__ismbbpunct:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    mov al,dl
    mov ah,0
    mov bx,ax

org 99
    test byte ptr DGROUP:__mbctype[bx+1],1
    jz mbbis_006f

mbbis_006a:
    mov ax,1
    jmp short mbbis_0071

mbbis_006f:
    xor ax,ax

mbbis_0071:
    pop di
    pop si
    pop bp
    retf

org 86
    test byte ptr DGROUP:__ctype[bx+1],12
    jnz mbbis_006a
    mov al,dl
    mov ah,0
    mov bx,ax

org 72

__ismbbalpha:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    mov al,dl
    mov ah,0
    mov bx,ax

org 48

__ismbbkana:
    push bp
    mov bp,sp
    push si
    push di
    mov al,[bp+6]
    mov ah,0
    mov bx,ax
    mov al,byte ptr DGROUP:__mbctype[bx+1]
    and al,3
    mov ah,0
    pop di
    pop si
    pop bp
    retf

org 24

__ismbbkpunct:
    push bp
    mov bp,sp
    push si
    push di
    mov al,[bp+6]
    mov ah,0
    mov bx,ax
    mov al,byte ptr DGROUP:__mbctype[bx+1]
    and al,2
    mov ah,0
    pop di
    pop si
    pop bp
    retf

org 0

__ismbbkalpha:
    push bp
    mov bp,sp
    push si
    push di
    mov al,[bp+6]
    mov ah,0
    mov bx,ax
    mov al,byte ptr DGROUP:__mbctype[bx+1]
    and al,1
    mov ah,0
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
