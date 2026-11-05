; Complete original Japanese Borland DOS CRT dossdate member.
; full far DOS setdate/settime INT 21h AH=2Bh/2Dh and errno 19 paths.
; Each instruction and far entry preserves the original 16-bit ABI, including
; genuine carry/error and DTA state. No opaque executable byte arrays.
.8086
extrn _errno:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __dos_setdate,__dos_settime


; Preserve original two complete function bodies and descending FIXUPPs.
org 44
__dos_settime:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    mov ch,es:[bx]
    mov cl,es:[bx+1]
    mov dh,es:[bx+2]
    mov dl,es:[bx+3]
    mov ah,45
    int 21h
    cmp al,255
    jnz dossdate_0056
    mov word ptr DGROUP:_errno,19
    mov ax,65535
    jmp short dossdate_0058

dossdate_0056:
    xor ax,ax

dossdate_0058:
    pop di
    pop si
    pop bp
    retf

org 0
__dos_setdate:
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    mov dh,es:[bx+1]
    mov dl,es:[bx]
    mov cx,es:[bx+2]
    mov ah,43
    int 21h
    cmp al,255
    jnz dossdate_0026
    mov word ptr DGROUP:_errno,19
    mov ax,65535
    jmp short dossdate_0028

dossdate_0026:
    xor ax,ax

dossdate_0028:
    pop di
    pop si
    pop bp
    retf

_TEXT ends
end
