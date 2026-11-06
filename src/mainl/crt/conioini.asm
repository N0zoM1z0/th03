; Original Japanese Borland conioini: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn ___conio_type:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _DATA,_BSS
_INIT_ segment word public 'INITDATA'
db 0,15
dd ___conio_type_init
_INIT_ ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___conio_type_init
; Complete disjoint instruction chunks follow original OMF field chronology.

org 2
    cmp word ptr DGROUP:___conio_type, 0
    jne short conio_init_return
    mov ah, 4
    xor cx, cx
    int 01ah
    cmp ch, 019h
    je short detected_ibm
    cmp ch, 020h
    je short detected_ibm

org 25
    mov word ptr DGROUP:___conio_type, 2
    jmp short conio_init_return

org 33
detected_ibm:
    mov word ptr DGROUP:___conio_type, 1
conio_init_return:
    pop di
    pop si
    ret

org 0
___conio_type_init label near
    push si
    push di
_TEXT ends
end
