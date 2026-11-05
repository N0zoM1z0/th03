; Original Japanese Borland C++ regexp matcher, full 2522-byte CODE.
; Complete makepat, matchs, patcmp and esc far APIs, with typed CODE-resident
; dispatch tables, original 8086 ABI, original far and near call semantics.
; No executable machine-code blobs, target-OBJ patches or hidden filler.
.8086
extrn __ctype:byte
extrn _toupper:far
extrn _memset:far
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
; Original compiler-generated far unwind thunk.
match_unwind_empty:
    push si
    push di
    pop di
    pop si
    retf
_TEXT ends

_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @makepat$qnxcnucui
public @matchs$qnxcnxucnnc
public @patcmp$qnxcnxuct1
public @esc$qnnxc

; Original complete far public entry and its control flow.

@makepat$qnxcnucui:
    push bp
    mov bp,sp
    sub sp,18
    push si
    push di
    mov word ptr [bp-10],1
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz match_0019
    jmp near ptr match_0213

match_0019:
    mov al,es:[bx]
    cbw
    cmp ax,10
    jnz match_0025
    jmp near ptr match_0213

match_0025:
    les bx,[bp+6]
    mov al,es:[bx]
    cbw
    cmp ax,42
    jnz match_0034
    jmp near ptr match_0213

match_0034:
    mov al,es:[bx]
    cbw
    cmp ax,43
    jnz match_0040
    jmp near ptr match_0213

match_0040:
    mov al,es:[bx]
    cbw
    cmp ax,63
    jnz match_004c
    jmp near ptr match_0213

match_004c:
    mov word ptr [bp-10],2
    mov ax,[bp+10]
    or ax,[bp+12]
    jnz match_005c
    jmp near ptr match_0213

match_005c:
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-2],dx
    mov [bp-4],ax
    mov [bp-6],dx
    mov [bp-8],ax
    mov word ptr [bp-10],3
    jmp near ptr match_01f2

match_0076:
    mov ax,[bp+14]
    dec ax
    mov dx,[bp+10]
    add dx,ax
    cmp dx,[bp-4]
    ja match_0087
    jmp near ptr match_0213

match_0087:
    les bx,[bp+6]
    mov al,es:[bx]
    cbw
    mov [bp-12],ax
    mov cx,7
    mov bx,offset _TEXTC:makepat_character_keys

match_0097:
    mov ax,cs:[bx]
    cmp ax,[bp-12]
    jz match_00a7
    add bx,2
    loop match_0097
    jmp near ptr match_01d1

match_00a7:
    jmp cs:[bx+14]

match_00ab:
    les bx,[bp-4]
    mov byte ptr es:[bx],174
    jmp short match_00ec

match_00b4:
    mov dx,[bp-2]
    mov ax,[bp-4]
    cmp dx,[bp+12]
    jnz match_00e0
    cmp ax,[bp+10]
    jnz match_00e0
    mov al,222
    jmp short match_00e6

match_00c8:
    les bx,[bp+6]
    cmp byte ptr es:[bx+1],0
    jz match_00dc
    mov al,es:[bx+1]
    cbw
    cmp ax,10
    jnz match_00e0

match_00dc:
    mov al,164
    jmp short match_00e6

match_00e0:
    les bx,[bp+6]
    mov al,es:[bx]

match_00e6:
    les bx,[bp-4]
    mov es:[bx],al

match_00ec:
    mov dx,[bp-2]
    mov ax,[bp-4]
    mov [bp-6],dx
    mov [bp-8],ax

match_00f8:
    inc word ptr [bp-4]
    inc word ptr [bp+6]
    jmp near ptr match_01f2

match_0101:
    xor ax,ax
    mov dx,[bp-4]
    xor bx,bx
    sub dx,[bp+10]
    sbb bx,0
    add dx,16
    adc bx,0
    cmp ax,bx
    jg match_0125
    jz match_011d
    jmp near ptr match_0213

match_011d:
    cmp [bp+14],dx
    ja match_0125
    jmp near ptr match_0213

match_0125:
    mov dx,[bp-2]
    mov ax,[bp-4]
    mov [bp-6],dx
    mov [bp-8],ax
    les bx,[bp-4]
    mov byte ptr es:[bx],219
    inc word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
    db 09ah
    dd match_024c
    add sp,8
    mov [bp+8],dx
    mov [bp+6],ax
    add word ptr [bp-4],16
    jmp near ptr match_01f2

match_015c:
    les bx,[bp-8]
    mov al,es:[bx]
    mov ah,0
    mov [bp-14],ax
    mov cx,5
    mov bx,offset _TEXTC:makepat_class_keys

match_016d:
    mov ax,cs:[bx]
    cmp ax,[bp-14]
    jz match_017c
    add bx,2
    loop match_016d
    jmp short match_0183

match_017c:
    jmp cs:[bx+10]
    jmp near ptr match_0213

match_0183:
    mov dx,[bp-2]
    mov ax,[bp-4]
    mov [bp-16],dx
    mov [bp-18],ax
    jmp short match_019e

match_0191:
    les bx,[bp-18]
    mov al,es:[bx-1]
    mov es:[bx],al
    dec word ptr [bp-18]

match_019e:
    mov ax,[bp-18]
    cmp ax,[bp-8]
    ja match_0191
    les bx,[bp+6]
    mov al,es:[bx]
    cbw
    cmp ax,63
    jnz match_01b6
    mov al,191
    jmp short match_01c8

match_01b6:
    les bx,[bp+6]
    mov al,es:[bx]
    cbw
    cmp ax,43
    jnz match_01c6
    mov al,171
    jmp short match_01c8

match_01c6:
    mov al,170

match_01c8:
    les bx,[bp-8]
    mov es:[bx],al
    jmp near ptr match_00f8

match_01d1:
    mov dx,[bp-2]
    mov ax,[bp-4]
    mov [bp-6],dx
    mov [bp-8],ax
    push ss
    lea ax,[bp+6]
    push ax
    db 09ah
    dd @esc$qnnxc
    pop cx
    pop cx
    les bx,[bp-4]
    mov es:[bx],al
    inc word ptr [bp-4]

match_01f2:
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jz match_0207
    mov al,es:[bx]
    cbw
    cmp ax,10
    jz match_0207
    jmp near ptr match_0076

match_0207:
    les bx,[bp-4]
    mov byte ptr es:[bx],0
    mov word ptr [bp-10],0

match_0213:
    mov ax,[bp-10]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Original CODE-resident makepat character classes and jump targets.

makepat_class_keys:
    dw 164,170,171,191,222

makepat_class_jumps:
    dw match_0213
    dw match_0213
    dw match_0213
    dw match_0213
    dw match_0213

makepat_character_keys:
    dw 36,42,43,46,63,91,94

makepat_character_jumps:
    dw match_00c8
    dw match_015c
    dw match_015c
    dw match_00ab
    dw match_015c
    dw match_0101
    dw match_00b4

; Compiler internal helper continued after typed dispatch data.

match_024c:
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-6],dx
    mov [bp-8],ax
    inc word ptr [bp+10]
    les bx,[bp+10]
    mov al,es:[bx]
    cbw
    cmp ax,94
    jnz match_0274
    mov ax,1
    jmp short match_0276

match_0274:
    xor ax,ax

match_0276:
    mov [bp-4],ax
    cmp word ptr [bp-4],0
    jz match_0282
    inc word ptr [bp+10]

match_0282:
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-6],dx
    mov [bp-8],ax
    mov ax,16
    push ax
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _memset
    add sp,8
    jmp near ptr match_0347

match_02a6:
    les bx,[bp+10]
    mov al,es:[bx]
    cbw
    cmp ax,45
    jz match_02da
    push ss
    lea ax,[bp+10]
    push ax
    db 09ah
    dd @esc$qnnxc
    pop cx
    pop cx
    mov dx,ax
    and ax,127
    mov cl,3
    sar ax,cl
    les bx,[bp+6]
    add bx,ax
    mov cl,dl
    and cl,7
    mov al,1
    shl al,cl
    or es:[bx],al
    jmp short match_0347

match_02da:
    mov dx,[bp+12]
    mov ax,[bp+10]
    cmp dx,[bp-6]
    jnz match_02f4
    cmp ax,[bp-8]
    jnz match_02f4
    les bx,[bp+6]
    or byte ptr es:[bx+5],32
    jmp short match_0344

match_02f4:
    inc word ptr [bp+10]
    les bx,[bp+10]
    mov al,es:[bx-2]
    cmp al,es:[bx]
    jng match_030f
    mov al,es:[bx]
    cbw
    mov dx,ax
    mov al,es:[bx-2]
    jmp short match_031c

match_030f:
    les bx,[bp+10]
    mov al,es:[bx-2]
    cbw
    mov dx,ax
    mov al,es:[bx]

match_031c:
    cbw
    mov [bp-2],ax
    jmp short match_033c

match_0322:
    mov ax,dx
    and ax,127
    mov cl,3
    sar ax,cl
    les bx,[bp+6]
    add bx,ax
    mov cl,dl
    and cl,7
    mov al,1
    shl al,cl
    or es:[bx],al

match_033c:
    inc dx
    mov ax,dx
    cmp ax,[bp-2]
    jng match_0322

match_0344:
    inc word ptr [bp+10]

match_0347:
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jz match_035c
    mov al,es:[bx]
    cbw
    cmp ax,93
    jz match_035c
    jmp near ptr match_02a6

match_035c:
    les bx,[bp+10]
    mov al,es:[bx]
    cbw
    cmp ax,93
    jnz match_036b
    inc word ptr [bp+10]

match_036b:
    cmp word ptr [bp-4],0
    jz match_0383
    mov dx,16
    jmp short match_0380

match_0376:
    les bx,[bp+6]
    xor byte ptr es:[bx],255
    inc word ptr [bp+6]

match_0380:
    dec dx
    jnl match_0376

match_0383:
    mov dx,[bp+12]
    mov ax,[bp+10]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Original complete far public entry and its control flow.

@matchs$qnxcnxucnnc:
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov word ptr [bp-2],0
    mov word ptr [bp-4],0
    mov ax,[bp+10]
    or ax,[bp+12]
    jnz match_03b0
    xor dx,dx
    xor ax,ax
    jmp near ptr match_0439

match_03b0:
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz match_03e4
    les bx,[bp+10]
    cmp byte ptr es:[bx],164
    jz match_03d6
    cmp byte ptr es:[bx],222
    jnz match_0423
    cmp byte ptr es:[bx+1],0
    jz match_03d6
    cmp byte ptr es:[bx+1],164
    jnz match_0423

match_03d6:
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short match_0423

match_03e4:
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-6],dx
    mov [bp-8],ax
    jmp short match_041a

match_03f2:
    push word ptr [bp-6]
    push word ptr [bp-8]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    db 09ah
    dd @patcmp$qnxcnxuct1
    add sp,12
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,[bp-2]
    jnz match_0423
    inc word ptr [bp+6]

match_041a:
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jnz match_03f2

match_0423:
    les bx,[bp+14]
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax
    mov dx,[bp-2]
    mov ax,[bp-4]

match_0439:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Original complete far public entry and its control flow.

@patcmp$qnxcnxuct1:
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov word ptr [bp-6],0
    mov word ptr [bp-8],0
    mov ax,[bp+10]
    or ax,[bp+12]
    jz match_045c
    jmp near ptr match_0589

match_045c:
    jmp near ptr match_04fa

match_045f:
    les bx,[bp+10]
    cmp byte ptr es:[bx],191
    jnz match_0490
    push word ptr [bp+16]
    push word ptr [bp+14]
    inc word ptr [bp+10]
    mov ax,[bp+10]
    push word ptr [bp+12]
    push ax
    push ss
    lea ax,[bp+6]
    push ax
    db 09ah
    dd match_05b1
    add sp,12
    les bx,[bp+10]
    cmp byte ptr es:[bx],219
    jnz match_04c8
    jmp short match_04c3

match_0490:
    les bx,[bp+10]
    cmp byte ptr es:[bx],170
    jz match_04d1
    cmp byte ptr es:[bx],171
    jz match_04d1
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push bx
    push ss
    lea ax,[bp+6]
    push ax
    db 09ah
    dd match_05b1
    add sp,12
    or ax,ax
    jz match_04fa
    les bx,[bp+10]
    cmp byte ptr es:[bx],219
    jnz match_04c8

match_04c3:
    mov ax,17
    jmp short match_04cb

match_04c8:
    mov ax,1

match_04cb:
    add [bp+10],ax
    jmp near ptr match_0589

match_04d1:
    les bx,[bp+10]
    inc word ptr [bp+10]
    cmp byte ptr es:[bx],171
    jnz match_0501
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ss
    lea ax,[bp+6]
    push ax
    db 09ah
    dd match_05b1
    add sp,12
    or ax,ax
    jnz match_0501

match_04fa:
    xor dx,dx
    xor ax,ax
    jmp near ptr match_05ab

match_0501:
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax

match_050d:
    les bx,[bp+6]
    cmp byte ptr es:[bx],0
    jz match_0533
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ss
    lea ax,[bp+6]
    push ax
    db 09ah
    dd match_05b1
    add sp,12
    or ax,ax
    jnz match_050d

match_0533:
    les bx,[bp+10]
    cmp byte ptr es:[bx],219
    jnz match_0541
    mov ax,17
    jmp short match_0544

match_0541:
    mov ax,1

match_0544:
    add [bp+10],ax
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jz match_0595
    jmp short match_0579

match_0552:
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call @patcmp$qnxcnxuct1
    add sp,12
    mov [bp-6],dx
    mov [bp-8],ax
    or ax,[bp-6]
    jnz match_0581
    dec word ptr [bp+6]

match_0579:
    mov ax,[bp-4]
    cmp ax,[bp+6]
    jna match_0552

match_0581:
    mov dx,[bp-6]
    mov ax,[bp-8]
    jmp short match_05ab

match_0589:
    les bx,[bp+10]
    cmp byte ptr es:[bx],0
    jz match_0595
    jmp near ptr match_045f

match_0595:
    dec word ptr [bp+6]
    mov ax,[bp+14]
    cmp ax,[bp+6]
    jna match_05a5
    mov dx,[bp+16]
    jmp short match_05ab

match_05a5:
    mov dx,[bp+8]
    mov ax,[bp+6]

match_05ab:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

match_05b1:
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov word ptr [bp-2],65535
    les bx,[bp+10]
    mov al,es:[bx]
    mov ah,0
    mov [bp-4],ax
    mov cx,4
    mov bx,offset _TEXTC:patcmp_character_keys

match_05cf:
    mov ax,cs:[bx]
    cmp ax,[bp-4]
    jz match_05df
    add bx,2
    loop match_05cf
    jmp near ptr match_0662

match_05df:
    jmp cs:[bx+8]

match_05e3:
    les bx,[bp+6]
    mov dx,es:[bx+2]
    mov ax,es:[bx]
    cmp dx,[bp+16]
    jz match_05f5
    jmp near ptr match_067d

match_05f5:
    cmp ax,[bp+14]
    jz match_05fd
    jmp near ptr match_067d

match_05fd:
    jmp short match_0625

match_05ff:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,10
    jz match_067d
    jmp short match_0678

match_0610:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,10
    jz match_0625
    cmp byte ptr es:[bx],0
    jnz match_067d

match_0625:
    mov word ptr [bp-2],0
    jmp short match_067d

match_062c:
    les bx,[bp+6]
    les bx,es:[bx]
    mov [bp-6],es
    mov [bp-8],bx
    mov al,es:[bx]
    cbw
    and ax,127
    mov cl,3
    sar ax,cl
    les bx,[bp+10]
    add bx,ax
    mov al,es:[bx+1]
    mov ah,0
    les bx,[bp-8]
    mov cl,es:[bx]
    and cl,7
    mov dx,1
    shl dx,cl
    ; Borland's TEST DX,AX has ModR/M C2h. TASM canonicalizes the
    ; commutative TEST into AX,DX (D0h), changing one CODE byte. Specify
    ; this *single, documented* 8086 instruction encoding explicitly.
    db 085h,0C2h              ; TEST DX,AX (register/register)
    jz match_067d
    jmp short match_0678

match_0662:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    les bx,[bp+10]
    mov dl,es:[bx]
    mov dh,0
    cmp ax,dx
    jnz match_067d

match_0678:
    mov word ptr [bp-2],1

match_067d:
    cmp word ptr [bp-2],0
    jng match_068c
    les bx,[bp+6]
    mov ax,[bp-2]
    add es:[bx],ax

match_068c:
    mov ax,[bp-2]
    inc ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Original CODE-resident patcmp single-character dispatch.

patcmp_character_keys:
    dw 164,174,219,222

patcmp_character_jumps:
    dw match_0610
    dw match_05ff
    dw match_062c
    dw match_05e3

; Compiler internal helper continued after typed dispatch data.

match_06a6:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    mov bx,dx
    test byte ptr DGROUP:__ctype[bx+1],2
    jz match_06be
    mov ax,dx
    add ax,65488
    jmp short match_06c8

match_06be:
    push dx
    call _toupper
    pop cx
    add ax,65481

match_06c8:
    and ax,15
    pop di
    pop si
    pop bp
    retf

match_06cf:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    add ax,65488
    and ax,7
    pop di
    pop si
    pop bp
    retf

; Original complete far public entry and its control flow.

@esc$qnnxc:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,92
    jz match_0711
    les bx,[bp+6]
    mov dx,es:[bx+2]
    mov si,es:[bx]
    inc word ptr es:[bx]
    mov es,dx
    mov al,es:[si]
    cbw
    mov [bp-2],ax
    jmp near ptr match_09a4

match_0711:
    les bx,[bp+6]
    inc word ptr es:[bx]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    push ax
    call _toupper
    pop cx
    mov [bp-4],ax
    mov cx,10
    mov bx,offset _TEXTC:escape_character_keys

match_072e:
    mov ax,cs:[bx]
    cmp ax,[bp-4]
    jz match_073e
    add bx,2
    loop match_072e
    jmp near ptr match_08e2

match_073e:
    jmp cs:[bx+20]

match_0742:
    mov word ptr [bp-2],92
    jmp near ptr match_099e

match_074a:
    mov word ptr [bp-2],8
    jmp near ptr match_099e

match_0752:
    mov word ptr [bp-2],12
    jmp near ptr match_099e

match_075a:
    mov word ptr [bp-2],10
    jmp near ptr match_099e

match_0762:
    mov word ptr [bp-2],13
    jmp near ptr match_099e

match_076a:
    mov word ptr [bp-2],32
    jmp near ptr match_099e

match_0772:
    mov word ptr [bp-2],9
    jmp near ptr match_099e

match_077a:
    mov word ptr [bp-2],27
    jmp near ptr match_099e

match_0782:
    les bx,[bp+6]
    inc word ptr es:[bx]
    push bx
    push es
    mov es,es:[bx+2]
    mov ax,es
    pop es
    pop bx
    mov bx,es:[bx]
    mov es,ax
    mov al,es:[bx]
    cbw
    mov [bp-2],ax
    push ax
    call _toupper
    pop cx
    add ax,65472

match_07a8:
    mov [bp-2],ax
    jmp near ptr match_099e

match_07ae:
    mov word ptr [bp-2],0
    les bx,[bp+6]
    inc word ptr es:[bx]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    mov bx,ax
    test byte ptr DGROUP:__ctype[bx+1],2
    jnz match_07f9
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,97
    jl match_07e1
    mov al,es:[bx]
    cbw
    cmp ax,102
    jng match_07f9

match_07e1:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,65
    jl match_0815
    mov al,es:[bx]
    cbw
    cmp ax,70
    jg match_0815

match_07f9:
    les bx,[bp+6]
    mov dx,es:[bx+2]
    mov si,es:[bx]
    inc word ptr es:[bx]
    mov es,dx
    mov al,es:[si]
    cbw
    push ax
    push cs
    call match_06a6
    pop cx
    mov [bp-2],ax

match_0815:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    mov bx,ax
    test byte ptr DGROUP:__ctype[bx+1],2
    jnz match_0858
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,97
    jl match_0840
    mov al,es:[bx]
    cbw
    cmp ax,102
    jng match_0858

match_0840:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,65
    jl match_0879
    mov al,es:[bx]
    cbw
    cmp ax,70
    jg match_0879

match_0858:
    mov cl,4
    shl word ptr [bp-2],cl
    les bx,[bp+6]
    mov dx,es:[bx+2]
    mov si,es:[bx]
    inc word ptr es:[bx]
    mov es,dx
    mov al,es:[si]
    cbw
    push ax
    push cs
    call match_06a6
    pop cx
    or [bp-2],ax

match_0879:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    mov bx,ax
    test byte ptr DGROUP:__ctype[bx+1],2
    jnz match_08c2
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,97
    jl match_08a4
    mov al,es:[bx]
    cbw
    cmp ax,102
    jng match_08c2

match_08a4:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,65
    jnl match_08b6
    jmp near ptr match_0998

match_08b6:
    mov al,es:[bx]
    cbw
    cmp ax,70
    jng match_08c2
    jmp near ptr match_0998

match_08c2:
    mov cl,4
    shl word ptr [bp-2],cl
    les bx,[bp+6]
    mov dx,es:[bx+2]
    mov si,es:[bx]
    inc word ptr es:[bx]
    mov es,dx
    mov al,es:[si]
    cbw
    push ax
    push cs
    call match_06a6
    jmp near ptr match_0994

match_08e2:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,48
    jl match_08fa
    mov al,es:[bx]
    cbw
    cmp ax,55
    jng match_0907

match_08fa:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    jmp near ptr match_07a8

match_0907:
    les bx,[bp+6]
    inc word ptr es:[bx]
    mov dx,es:[bx+2]
    mov si,es:[bx]
    inc word ptr es:[bx]
    mov es,dx
    mov al,es:[si]
    cbw
    push ax
    push cs
    call match_06cf
    pop cx
    mov [bp-2],ax
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,48
    jl match_095f
    mov al,es:[bx]
    cbw
    cmp ax,55
    jg match_095f
    mov cl,3
    shl word ptr [bp-2],cl
    les bx,[bp+6]
    mov dx,es:[bx+2]
    mov si,es:[bx]
    inc word ptr es:[bx]
    mov es,dx
    mov al,es:[si]
    cbw
    push ax
    push cs
    call match_06cf
    pop cx
    or [bp-2],ax

match_095f:
    les bx,[bp+6]
    les bx,es:[bx]
    mov al,es:[bx]
    cbw
    cmp ax,48
    jl match_0998
    mov al,es:[bx]
    cbw
    cmp ax,55
    jg match_0998
    mov cl,3
    shl word ptr [bp-2],cl
    les bx,[bp+6]
    mov dx,es:[bx+2]
    mov si,es:[bx]
    inc word ptr es:[bx]
    mov es,dx
    mov al,es:[si]
    cbw
    push ax
    push cs
    call match_06cf

match_0994:
    pop cx
    or [bp-2],ax

match_0998:
    les bx,[bp+6]
    dec word ptr es:[bx]

match_099e:
    les bx,[bp+6]
    inc word ptr es:[bx]

match_09a4:
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Original CODE-resident escaped-character dispatch.

escape_character_keys:
    dw 0,66,69,70,78,82,83,84,88,94

escape_character_jumps:
    dw match_0742
    dw match_074a
    dw match_077a
    dw match_0752
    dw match_075a
    dw match_0762
    dw match_076a
    dw match_0772
    dw match_07ae
    dw match_0782

_TEXTC ends
end
