; Borland original Japanese MAINL formatting engine, 16-bit 8086,
; far string reads / far callback and bounded 80-byte on-stack buffer.
; Converted format specifier branches and jump targets are named, not
; original CODE byte blobs; table entries are relocatable symbolic labels.
.8086
extrn __LONGTOA:near,__REALCVT:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __VPRINTER

format_hex_word:
    mov al, dh
    call format_hex_nibble
    mov al, dl

format_hex_nibble:
    aam 10h
    xchg ah, al
    call emit_hex_nibble
    xchg ah, al

emit_hex_nibble:
    add al, 90h
    daa
    adc al, 40h
    daa
    stosb
    ret

; Exported formatter: near Pascal callback/result, original stack contract.
__VPRINTER proc near
    push bp
    mov bp, sp
    sub sp, 96h
    push si
    push di
    mov word ptr [bp - 12h], 0
    mov word ptr [bp - 14h], 50h
    mov word ptr [bp - 16h], 0
    jmp short loc_007c

string_length:
    push di
    mov cx, 0ffffh
    xor al, al
    repne scasb
    not cx
    dec cx
    pop di
    ret

buffer_putc:
    mov byte ptr ss:[di], al
    inc di
    dec byte ptr [bp - 14h]
    jne loc_007b

flush_buffer:
    push bx
    push cx
    push dx
    push es
    lea ax, [bp - 96h]
    sub di, ax
    push ss
    lea ax, [bp - 96h]
    push ax
    push di
    push word ptr [bp + 0ch]
    push word ptr [bp + 0ah]
    call word ptr [bp + 0eh]
    or ax, ax
    jne loc_006b
    mov word ptr [bp - 16h], 1

loc_006b:
    mov word ptr [bp - 14h], 50h
    add word ptr [bp - 12h], di
    lea di, [bp - 96h]
    pop es
    pop dx
    pop cx
    pop bx

loc_007b:
    ret

loc_007c:
    push es
    cld
    lea di, [bp - 96h]
    mov word ptr [bp - 4], di

loc_0085:
    mov di, word ptr [bp - 4]

loc_0088:
    les si, dword ptr [bp + 6]

loc_008b:
    lods byte ptr es:[si]
    or al, al
    je loc_00a3
    cmp al, 25h
    je loc_00a6

loc_0095:
    mov byte ptr ss:[di], al
    inc di
    dec byte ptr [bp - 14h]
    jg loc_008b
    call flush_buffer
    jmp short loc_008b

loc_00a3:
    jmp near ptr loc_048b

loc_00a6:
    mov word ptr [bp - 10h], si
    lods byte ptr es:[si]
    cmp al, 25h
    je loc_0095
    mov word ptr [bp - 4], di
    xor cx, cx
    mov word ptr [bp - 0eh], cx
    mov word ptr [bp - 2], 20h
    mov byte ptr [bp - 0bh], cl
    mov word ptr [bp - 8], 0ffffh
    mov word ptr [bp - 0ah], 0ffffh
    jmp short loc_00cd

loc_00cb:
    lods byte ptr es:[si]

loc_00cd:
    xor ah, ah
    mov dx, ax
    mov bx, ax
    sub bl, 20h
    cmp bl, 60h
    jae loc_00ee
    mov bl,byte ptr DGROUP:conversion_class[bx]
    cmp bx, 17h
    jbe loc_00e7
    jmp near ptr case_0477

loc_00e7:
    add bx, bx
    jmp word ptr cs:[bx+format_dispatch]

loc_00ee:
    jmp near ptr case_0477

case_00f1:
    cmp ch, 0
    ja loc_00ee
    or word ptr [bp - 2], 1
    jmp short loc_00cb

case_00fc:
    cmp ch, 0
    ja loc_00ee
    or word ptr [bp - 2], 2
    jmp short loc_00cb

case_0107:
    cmp ch, 0
    ja loc_00ee
    cmp byte ptr [bp - 0bh], 2bh
    je loc_0115
    mov byte ptr [bp - 0bh], dl

loc_0115:
    jmp short loc_00cb

case_0117:
    and word ptr [bp - 2], 0ffdfh
    jmp short loc_0121

case_011d:
    or word ptr [bp - 2], 20h

loc_0121:
    mov ch, 5
    jmp short loc_00cb

case_0125:
    cmp ch, 0
    ja case_0177
    test word ptr [bp - 2], 2
    jne loc_015a
    or word ptr [bp - 2], 8
    mov ch, 1
    jmp short loc_00cb

loc_0139:
    jmp near ptr case_0477

case_013c:
    mov di, word ptr [bp + 4]
    mov ax, word ptr ss:[di]
    add word ptr [bp + 4], 2
    cmp ch, 2
    jae loc_015d
    or ax, ax
    jns loc_0155
    neg ax
    or word ptr [bp - 2], 2

loc_0155:
    mov word ptr [bp - 8], ax
    mov ch, 3

loc_015a:
    jmp near ptr loc_00cb

loc_015d:
    cmp ch, 4
    jne loc_0139
    mov word ptr [bp - 0ah], ax
    inc ch
    jmp near ptr loc_00cb

case_016a:
    cmp ch, 4
    jae loc_0139
    mov ch, 4
    inc word ptr [bp - 0ah]
    jmp near ptr loc_00cb

case_0177:
    xchg dx, ax
    sub al, 30h
    cbw
    cmp ch, 2
    ja loc_0199
    mov ch, 2
    xchg word ptr [bp - 8], ax
    or ax, ax
    jl loc_015a
    shl ax, 1
    mov dx, ax
    shl ax, 1
    shl ax, 1
    add ax, dx
    add word ptr [bp - 8], ax
    jmp near ptr loc_00cb

loc_0199:
    cmp ch, 4
    jne loc_0139
    xchg word ptr [bp - 0ah], ax
    or ax, ax
    je loc_015a
    shl ax, 1
    mov dx, ax
    shl ax, 1
    shl ax, 1
    add ax, dx
    add word ptr [bp - 0ah], ax
    jmp near ptr loc_00cb

case_01b5:
    or word ptr [bp - 2], 10h
    jmp near ptr loc_0121

case_01bc:
    or word ptr [bp - 2], 100h

case_01c1:
    and word ptr [bp - 2], 0ffefh
    jmp near ptr loc_0121

case_01c8:
    mov bh, 8
    jmp short loc_01d6

case_01cc:
    mov bh, 0ah
    jmp short loc_01d6

case_01d0:
    mov bh, 10h
    mov bl, 0e9h
    add bl, dl

loc_01d6:
    mov byte ptr [bp - 0bh], 0
    mov byte ptr [bp - 5], dl
    xor dx, dx
    mov byte ptr [bp - 6], dl
    mov di, word ptr [bp + 4]
    mov ax, word ptr ss:[di]
    jmp short loc_01fa

case_01ea:
    mov bh, 0ah
    mov byte ptr [bp - 6], 1
    mov byte ptr [bp - 5], dl
    mov di, word ptr [bp + 4]
    mov ax, word ptr ss:[di]
    cwd

loc_01fa:
    inc di
    inc di
    mov word ptr [bp + 6], si
    test word ptr [bp - 2], 10h
    je loc_020b
    mov dx, word ptr ss:[di]
    inc di
    inc di

loc_020b:
    mov word ptr [bp + 4], di
    lea di, [bp - 45h]
    or ax, ax
    jne loc_0227
    or dx, dx
    jne loc_0227
    cmp word ptr [bp - 0ah], 0
    jne loc_022b
    mov byte ptr ss:[di], 0
    mov ax, di
    jmp short loc_023b

loc_0227:
    or word ptr [bp - 2], 4

loc_022b:
    push dx
    push ax
    push ss
    push di
    mov al, bh
    cbw
    push ax
    mov al, byte ptr [bp - 6]
    push ax
    push bx
    call __LONGTOA

loc_023b:
    push ss
    pop es
    mov dx, word ptr [bp - 0ah]
    or dx, dx
    jge loc_0247
    jmp near ptr loc_033b

loc_0247:
    jmp near ptr loc_0349

case_024a:
    mov byte ptr [bp - 5], dl
    mov word ptr [bp + 6], si
    lea di, [bp - 46h]
    mov bx, word ptr [bp + 4]
    push word ptr ss:[bx]
    inc bx
    inc bx
    mov word ptr [bp + 4], bx
    test word ptr [bp - 2], 20h
    je loc_0275
    mov dx, word ptr ss:[bx]
    inc bx
    inc bx
    mov word ptr [bp + 4], bx
    push ss
    pop es
    call format_hex_word
    mov al, 3ah
    stosb

loc_0275:
    push ss
    pop es
    pop dx
    call format_hex_word
    mov byte ptr ss:[di], 0
    mov byte ptr [bp - 6], 0
    and word ptr [bp - 2], 0fffbh
    lea cx, [bp - 46h]
    sub di, cx
    xchg cx, di
    mov dx, word ptr [bp - 0ah]
    cmp dx, cx
    jg loc_0297
    mov dx, cx

loc_0297:
    jmp near ptr loc_033b

case_029a:
    mov word ptr [bp + 6], si
    mov byte ptr [bp - 5], dl
    mov di, word ptr [bp + 4]
    mov ax, word ptr ss:[di]
    add word ptr [bp + 4], 2
    push ss
    pop es
    lea di, [bp - 45h]
    xor ah, ah
    mov word ptr ss:[di], ax
    mov cx, 1
    jmp near ptr loc_037e

case_02ba:
    mov word ptr [bp + 6], si
    mov byte ptr [bp - 5], dl
    mov di, word ptr [bp + 4]
    test word ptr [bp - 2], 20h
    jne loc_02d7
    mov di, word ptr ss:[di]
    add word ptr [bp + 4], 2
    push ds
    pop es
    or di, di
    jmp short loc_02e2

loc_02d7:
    les di, dword ptr ss:[di]
    add word ptr [bp + 4], 4
    mov ax, es
    or ax, di

loc_02e2:
    jne loc_02e9
    push ds
    pop es
    mov di,offset DGROUP:null_pointer_text

loc_02e9:
    call string_length
    cmp cx, word ptr [bp - 0ah]
    jbe loc_02f4
    mov cx, word ptr [bp - 0ah]

loc_02f4:
    jmp near ptr loc_037e

case_02f7:
    mov word ptr [bp + 6], si
    mov byte ptr [bp - 5], dl
    mov di, word ptr [bp + 4]
    mov cx, word ptr [bp - 0ah]
    or cx, cx
    jge loc_030a
    mov cx, 6

loc_030a:
    push ss
    push di
    push cx
    push ss
    lea bx, [bp - 45h]
    push bx
    push dx
    mov ax, 1
    and ax, word ptr [bp - 2]
    push ax
    mov ax, word ptr [bp - 2]
    test ax, 100h
    je loc_032b
    mov ax, 8
    add word ptr [bp + 4], 0ah
    jmp short loc_0332

loc_032b:
    add word ptr [bp + 4], 8
    mov ax, 6

loc_0332:
    push ax
    call __REALCVT
    push ss
    pop es
    lea di, [bp - 45h]

loc_033b:
    test word ptr [bp - 2], 8
    je loc_035a
    mov dx, word ptr [bp - 8]
    or dx, dx
    jle loc_035a

loc_0349:
    call string_length
    cmp byte ptr es:[di], 2dh
    jne loc_0353
    dec cx

loc_0353:
    sub dx, cx
    jle loc_035a
    mov word ptr [bp - 0eh], dx

loc_035a:
    cmp byte ptr es:[di], 2dh
    je loc_036b
    mov al, byte ptr [bp - 0bh]
    or al, al
    je loc_037b
    dec di
    mov byte ptr es:[di], al

loc_036b:
    cmp word ptr [bp - 0eh], 0
    jle loc_037b
    mov cx, word ptr [bp - 0ah]
    or cx, cx
    jge loc_037b
    dec word ptr [bp - 0eh]

loc_037b:
    call string_length

loc_037e:
    mov si, di
    mov di, word ptr [bp - 4]
    mov bx, word ptr [bp - 8]
    mov ax, 5
    and ax, word ptr [bp - 2]
    cmp ax, 5
    jne loc_03a4
    mov ah, byte ptr [bp - 5]
    cmp ah, 6fh
    jne loc_03a6
    cmp word ptr [bp - 0eh], 0
    jg loc_03a4
    mov word ptr [bp - 0eh], 1

loc_03a4:
    jmp short loc_03c1

loc_03a6:
    cmp ah, 78h
    je loc_03b0
    cmp ah, 58h
    jne loc_03c1

loc_03b0:
    or word ptr [bp - 2], 40h
    dec bx
    dec bx
    sub word ptr [bp - 0eh], 2
    jge loc_03c1
    mov word ptr [bp - 0eh], 0

loc_03c1:
    add cx, word ptr [bp - 0eh]
    test word ptr [bp - 2], 2
    jne loc_03d7
    jmp short loc_03d3

loc_03cd:
    mov al, 20h
    call buffer_putc
    dec bx

loc_03d3:
    cmp bx, cx
    jg loc_03cd

loc_03d7:
    test word ptr [bp - 2], 40h
    je loc_03e9
    mov al, 30h
    call buffer_putc
    mov al, byte ptr [bp - 5]
    call buffer_putc

loc_03e9:
    mov dx, word ptr [bp - 0eh]
    or dx, dx
    jle loc_0417
    sub cx, dx
    sub bx, dx
    mov al, byte ptr es:[si]
    cmp al, 2dh
    je loc_0403
    cmp al, 20h
    je loc_0403
    cmp al, 2bh
    jne loc_040a

loc_0403:
    lods byte ptr es:[si]
    call buffer_putc
    dec cx
    dec bx

loc_040a:
    xchg cx, dx
    jcxz loc_0415

loc_040e:
    mov al, 30h
    call buffer_putc
    loop loc_040e

loc_0415:
    xchg cx, dx

loc_0417:
    jcxz loc_042b
    sub bx, cx

loc_041b:
    lods byte ptr es:[si]
    mov byte ptr ss:[di], al
    inc di
    dec byte ptr [bp - 14h]
    jg loc_0429
    call flush_buffer

loc_0429:
    loop loc_041b

loc_042b:
    or bx, bx
    jle loc_0438
    mov cx, bx

loc_0431:
    mov al, 20h
    call buffer_putc
    loop loc_0431

loc_0438:
    jmp near ptr loc_0088

case_043b:
    mov word ptr [bp + 6], si
    mov di, word ptr [bp + 4]
    test word ptr [bp - 2], 20h
    jne loc_0453
    mov di, word ptr ss:[di]
    add word ptr [bp + 4], 2
    push ds
    pop es
    jmp short loc_045a

loc_0453:
    les di, dword ptr ss:[di]
    add word ptr [bp + 4], 4

loc_045a:
    mov ax, 50h
    sub al, byte ptr [bp - 14h]
    add ax, word ptr [bp - 12h]
    mov word ptr es:[di], ax
    test word ptr [bp - 2], 10h
    je loc_0474
    inc di
    inc di
    mov word ptr es:[di], 0

loc_0474:
    jmp near ptr loc_0085

case_0477:
    mov si, word ptr [bp - 10h]
    mov es, word ptr [bp + 8]
    mov di, word ptr [bp - 4]
    mov al, 25h

loc_0482:
    call buffer_putc
    lods byte ptr es:[si]
    or al, al
    jne loc_0482

loc_048b:
    cmp byte ptr [bp - 14h], 50h
    jge loc_0494
    call flush_buffer

loc_0494:
    pop es
    cmp word ptr [bp - 16h], 0
    je loc_04a0
    mov ax, 0ffffh
    jmp short loc_04a3

loc_04a0:
    mov ax, word ptr [bp - 12h]

loc_04a3:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0ch
__VPRINTER endp

; Word-offset selector jump table used by the percent conversion parser.
format_dispatch label word
    dw case_0107 ; format class 0
    dw case_00f1 ; format class 1
    dw case_013c ; format class 2
    dw case_00fc ; format class 3
    dw case_016a ; format class 4
    dw case_0177 ; format class 5
    dw case_01b5 ; format class 6
    dw case_01bc ; format class 7
    dw case_01c1 ; format class 8
    dw case_0125 ; format class 9
    dw case_01ea ; format class 10
    dw case_01c8 ; format class 11
    dw case_01cc ; format class 12
    dw case_01d0 ; format class 13
    dw case_024a ; format class 14
    dw case_02f7 ; format class 15
    dw case_029a ; format class 16
    dw case_02ba ; format class 17
    dw case_043b ; format class 18
    dw case_0477 ; format class 19
    dw case_0477 ; format class 20
    dw case_0477 ; format class 21
    dw case_0117 ; format class 22
    dw case_011d ; format class 23
_TEXT ends
_DATA segment word public 'DATA'
null_pointer_text db '(null)',0
; Specifier character-class lookup. The 96 entries encode parser cases
; for characters 0x20 through 0x7f, not executable bytes.
conversion_class label byte
    db 0,14h,14h,1,14h,15h,14h,14h,14h,14h,2,0,14h,3,4,14h
    db 9,5,5,5,5,5,5,5,5,5,14h,14h,14h,14h,14h,14h
    db 14h,14h,14h,14h,14h,0fh,17h,0fh,8,14h,14h,14h,7,14h,16h,14h
    db 14h,14h,14h,14h,14h,14h,14h,14h,0dh,14h,14h,14h,14h,14h,14h,14h
    db 14h,14h,14h,10h,0ah,0fh,0fh,0fh,8,0ah,14h,14h,6,14h,12h,0bh
    db 0eh,14h,14h,11h,14h,0ch,14h,14h,0dh,14h,14h,14h,14h,14h,14h,14h
_DATA ends
end
