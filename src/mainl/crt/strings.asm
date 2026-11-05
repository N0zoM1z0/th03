; Complete original Japanese Borland C++ strings CRT member.
; 17 far methods, six global option words, real C++ exception/RTTI metadata.
; Natural 8086 mnemonics plus typed relocation-backed exception state only.
; No executable target-byte arrays or patched native output.
.8086
extrn @$bnew$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @_ThrowException$qnvt1t1t1uiuiuinuc:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _memcpy:far
extrn _memmove:far
extrn _memset:far
extrn _free:far
extrn _malloc:far
extrn _realloc:far
extrn @xmsg@$bctr$qmx6string:far
extrn @xmsg@$bctr$qmx4xmsg:far
extrn @xmsg@$bdtr$qv:far
extrn @xalloc@raise$qv:far
extrn @string@$bctr$qnxc:far
extrn ___xalloc:word
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

; Original typed exception records plus four real cleanup helper bodies.

; Original symbolic source block at CODE offset 570
org 570
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short strings_1_0247

strings_1_0243:
    jmp short strings_1_0247

strings_1_0245:
    xor ax,ax

strings_1_0247:
    pop di
    pop si
    pop bp
    retf

; Original symbolic source block at CODE offset 550
org 550
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz strings_1_0243
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original symbolic source block at CODE offset 523
org 523
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original symbolic source block at CODE offset 493
org 493
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short strings_1_01fa

strings_1_01f6:
    jmp short strings_1_01fa

strings_1_01f8:
    xor ax,ax

strings_1_01fa:
    pop di
    pop si
    pop bp
    retf

strings_destruct_out_of_range:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz strings_1_0245

; Original symbolic source block at CODE offset 473
org 473
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz strings_1_01f6
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original symbolic source block at CODE offset 446
org 446
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original symbolic source block at CODE offset 416
org 416
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short strings_1_01ad

strings_1_01a9:
    jmp short strings_1_01ad

strings_1_01ab:
    xor ax,ax

strings_1_01ad:
    pop di
    pop si
    pop bp
    retf

strings_destruct_xalloc:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz strings_1_01f8

; Original symbolic source block at CODE offset 396
org 396
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    jz strings_1_01a9
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original symbolic source block at CODE offset 369
org 369
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original symbolic source block at CODE offset 328
org 328
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

strings_destruct_length_error:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz strings_1_01ab

; Original symbolic source block at CODE offset 320
org 320
    call @xmsg@$bctr$qmx4xmsg
    add sp,8

; Original symbolic source block at CODE offset 297
org 297

strings_exception_297:
    dd strings_exception_285
    dw -30

strings_copy_exception:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original symbolic source block at CODE offset 289
org 289
    dd rtti_string_length_error
    dw 0
    dw 0

; Original symbolic source block at CODE offset 285
org 285

strings_exception_285:
    dd rtti_xalloc

; Original symbolic source block at CODE offset 279
org 279

strings_exception_279:
    dd strings_exception_275
    dw -30

; Original symbolic source block at CODE offset 269
org 269

strings_exception_269:
    dd strings_exception_257
    dw -30

strings_exception_275:
    dw 0
    dw 0

; Original symbolic source block at CODE offset 261
org 261
    dd rtti_string_length_error
    dw 0
    dw 0

; Original symbolic source block at CODE offset 257
org 257

strings_exception_257:
    dd rtti_xalloc

; Original symbolic source block at CODE offset 251
org 251

strings_exception_251:
    dd strings_exception_247
    dw -30

; Original symbolic source block at CODE offset 241
org 241

strings_exception_241:
    dd strings_exception_229
    dw -30

strings_exception_247:
    dw 0
    dw 0

; Original symbolic source block at CODE offset 233
org 233
    dd rtti_string_out_of_range
    dw 0
    dw 0

; Original symbolic source block at CODE offset 229
org 229

strings_exception_229:
    dd rtti_xalloc

; Original symbolic source block at CODE offset 223
org 223

strings_exception_223:
    dd strings_exception_219
    dw -30

; Original symbolic source block at CODE offset 217
org 217
    dw offset _TEXT:strings_exception_183

strings_exception_219:
    dw 0
    dw 0

; Original symbolic source block at CODE offset 209
org 209
    dw offset _TEXT:strings_exception_159
    dw 6
    dw 5
    dw 1

; Original symbolic source block at CODE offset 197
org 197

strings_exception_197:
    dd strings_exception_151
    dw -38
    dw 0
    dw 5
    dw 0

; Original symbolic source block at CODE offset 183
org 183

strings_exception_183:
    dd rtti_xmsg
    dw 256
    dw 1
    dw 0
    dw 0
    dw 0

; Original symbolic source block at CODE offset 169
org 169
    dd rtti_string_out_of_range
    dw 4
    dw -8
    dw 0
    dw 0
    dw 0

; Original symbolic source block at CODE offset 159
org 159

strings_exception_159:
    dd rtti_string
    dw 4
    dw -4
    dw 0

; Original symbolic source block at CODE offset 151
org 151

strings_exception_151:
    dd rtti_string_out_of_range
    dw 0
    dw 0

; Original symbolic source block at CODE offset 149
org 149
    dw offset _TEXT:strings_exception_115

; Original symbolic source block at CODE offset 141
org 141
    dw offset _TEXT:strings_exception_091
    dw 6
    dw 5
    dw 1

; Original symbolic source block at CODE offset 129
org 129

strings_exception_129:
    dd strings_exception_083
    dw -38
    dw 0
    dw 5
    dw 0

; Original symbolic source block at CODE offset 115
org 115

strings_exception_115:
    dd rtti_xmsg
    dw 256
    dw 1
    dw 0
    dw 0
    dw 0

; Original symbolic source block at CODE offset 101
org 101
    dd rtti_string_out_of_range
    dw 4
    dw -8
    dw 0
    dw 0
    dw 0

; Original symbolic source block at CODE offset 91
org 91

strings_exception_091:
    dd rtti_string
    dw 4
    dw -4
    dw 0

; Original symbolic source block at CODE offset 83
org 83

strings_exception_083:
    dd rtti_string_out_of_range
    dw 0
    dw 0

; Original symbolic source block at CODE offset 81
org 81
    dw offset _TEXT:strings_exception_047

; Original symbolic source block at CODE offset 73
org 73
    dw offset _TEXT:strings_exception_023
    dw 6
    dw 5
    dw 1

; Original symbolic source block at CODE offset 61
org 61

strings_exception_061:
    dd strings_exception_015
    dw -38
    dw 0
    dw 5
    dw 0

; Original symbolic source block at CODE offset 47
org 47

strings_exception_047:
    dd rtti_xmsg
    dw 256
    dw 1
    dw 0
    dw 0
    dw 0

; Original symbolic source block at CODE offset 33
org 33
    dd rtti_string_out_of_range
    dw 4
    dw -8
    dw 0
    dw 0
    dw 0

; Original symbolic source block at CODE offset 23
org 23

strings_exception_023:
    dd rtti_string
    dw 4
    dw -4
    dw 0

; Original symbolic source block at CODE offset 15
org 15

strings_exception_015:
    dd rtti_string_out_of_range
    dw 0
    dw 0

; Original symbolic source block at CODE offset 9
org 9

strings_exception_009:
    dd strings_exception_005
    dw -30

; Original symbolic source block at CODE offset 0
org 0

strings_empty_unwind:
    push si
    push di
    pop di
    pop si
    retf

strings_exception_005:
    dw 0
    dw 0
_TEXT ends

_DATA segment word public 'DATA'
public @string@case_sensitive
@string@case_sensitive dw 1
public @string@paranoid_check
@string@paranoid_check dw 0
public @string@skip_white
@string@skip_white dw 1
public @string@initial_capac
@string@initial_capac dw 63
public @string@resize_inc
@string@resize_inc dw 64
public @string@freeboard
@string@freeboard dw 63
string_out_of_range_message_12 db 'String reference out of range',0
string_out_of_range_message_42 db 'String reference out of range',0
string_out_of_range_message_72 db 'String reference out of range',0
_DATA ends

_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@$bdtr$qv
public @string@assert_element$xqui
public @string@assert_index$xqui
public @TSubString@assert_element$xqui
public @TStringRef@$bctr$qnxcuit1uiui
public @TStringRef@$bdtr$qv
public @TStringRef@reserve$qui
public @TStringRef@check_freeboard$qv
public @TStringRef@grow_to$qui
public @TStringRef@round_capacity$qui
public @TStringRef@splice$quiuinxcui
public @string@set_case_sensitive$qi
public @string@set_paranoid_check$qi
public @string@skip_whitespace$qi
public @string@initial_capacity$qui
public @string@resize_increment$qui
public @string@max_waste$qui

; Real native original string/TStringRef methods and typed 5-class RTTI.

; Original Borland CODE4 LEDATA block 0..1023

; Original symbolic source block at CODE offset 1016
org 1016
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp

; Original symbolic source block at CODE offset 1006
org 1006
    call @$bdele$qnv
    pop cx
    pop cx

strings_4_03f5:
    push word ptr [bp-30]

; Original symbolic source block at CODE offset 987
org 987
    call _free
    pop cx
    pop cx
    test byte ptr [bp+10],1
    jz strings_4_03f5
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original symbolic source block at CODE offset 950
org 950
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov ax,[bp+6]
    or ax,[bp+8]
    jz strings_4_03f5
    les bx,[bp+6]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

; Original symbolic source block at CODE offset 945
org 945
    call ___InitExceptBlocks

; Original symbolic source block at CODE offset 942
org 942
    mov bx,offset _TEXT:strings_exception_223

; Original symbolic source block at CODE offset 939
org 939
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 903
org 903

strings_4_0387:
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

@TStringRef@$bdtr$qv:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di

; Original symbolic source block at CODE offset 876
org 876
    call _memcpy
    add sp,20
    les bx,[bp+6]
    les bx,es:[bx+2]
    mov ax,[bp+14]
    add ax,[bp+20]
    add bx,ax
    mov byte ptr es:[bx],0

; Original symbolic source block at CODE offset 847
org 847
    call _memcpy
    push word ptr [bp+20]
    push word ptr [bp+18]
    push word ptr [bp+16]
    les bx,[bp+6]
    mov ax,es:[bx+2]
    add ax,[bp+14]
    push word ptr es:[bx+4]
    push ax

; Original symbolic source block at CODE offset 820
org 820
    call @xalloc@raise$qv
    pop cx
    pop cx

strings_4_033b:
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

; Original symbolic source block at CODE offset 816
org 816
    mov ax,offset DGROUP:___xalloc
    push ax

; Original symbolic source block at CODE offset 788
org 788
    call _malloc
    pop cx
    les bx,[bp+6]
    mov es:[bx+4],dx
    mov es:[bx+2],ax
    mov ax,es:[bx+2]
    or ax,es:[bx+4]
    jnz strings_4_033b
    push ds

; Original symbolic source block at CODE offset 769
org 769
    db 09ah     ; native far CALL, TASM would shorten to PUSH CS/CALL
    dd @TStringRef@round_capacity$qui
    pop cx
    les bx,[bp+6]
    mov es:[bx+8],ax
    mov ax,es:[bx+8]
    inc ax
    push ax

; Original symbolic source block at CODE offset 718
org 718
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jnz strings_4_02e1
    jmp near ptr strings_4_0387

strings_4_02e1:
    les bx,[bp+6]
    mov word ptr es:[bx],1
    mov word ptr es:[bx+10],0
    mov ax,[bp+14]
    add ax,[bp+20]
    mov es:[bx+6],ax
    mov ax,es:[bx+6]
    add ax,[bp+22]
    push ax

; Original symbolic source block at CODE offset 690
org 690
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TStringRef@$bctr$qnxcuit1uiui:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz strings_4_02e1
    mov ax,12
    push ax

; Original symbolic source block at CODE offset 679
org 679
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,26

strings_4_02af:
    push word ptr [bp-38]

; Original symbolic source block at CODE offset 675
org 675
    mov ax,offset _TEXTC:rtti_string_out_of_range
    push ax

; Original symbolic source block at CODE offset 651
org 651
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    lea ax,[bp-8]
    push ss
    push ax
    push cs

; Original symbolic source block at CODE offset 617
org 617
    call @xmsg@$bctr$qmx6string
    add sp,8
    mov word ptr [bp-26],14
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    push cs
    call @string@$bdtr$qv
    add sp,6
    mov word ptr [bp-26],6

; Original symbolic source block at CODE offset 599
org 599
    call @string@$bctr$qnxc
    add sp,8
    lea ax,[bp-4]
    push ss
    push ax
    push ss
    lea ax,[bp-8]
    push ax

; Original symbolic source block at CODE offset 590
org 590
    mov ax,offset DGROUP:string_out_of_range_message_72
    push ax
    push ss
    lea ax,[bp-4]
    push ax

; Original symbolic source block at CODE offset 576
org 576
    mov ax,offset _TEXT:strings_copy_exception
    push ax
    xor ax,ax
    push ax
    push ax
    mov word ptr [bp-26],6
    push ds

; Original symbolic source block at CODE offset 572
org 572
    mov ax,seg _TEXT
    push ax

; Original symbolic source block at CODE offset 528
org 528
    call ___InitExceptBlocks
    mov ax,[bp+10]
    mov [bp-40],ax
    les bx,[bp+6]
    mov ax,es:[bx+6]
    cmp ax,[bp-40]
    jna strings_4_022c
    mov ax,1
    jmp short strings_4_022e

strings_4_022c:
    xor ax,ax

strings_4_022e:
    or ax,ax
    jnz strings_4_02af
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax

; Original symbolic source block at CODE offset 525
org 525
    mov bx,offset _TEXT:strings_exception_197

; Original symbolic source block at CODE offset 522
org 522
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 503
org 503
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TSubString@assert_element$xqui:
    push bp
    mov bp,sp
    sub sp,40
    push si
    push di

; Original symbolic source block at CODE offset 492
org 492
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,26

strings_4_01f4:
    push word ptr [bp-38]

; Original symbolic source block at CODE offset 488
org 488
    mov ax,offset _TEXTC:rtti_string_out_of_range
    push ax

; Original symbolic source block at CODE offset 464
org 464
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    lea ax,[bp-8]
    push ss
    push ax
    push cs

; Original symbolic source block at CODE offset 430
org 430
    call @xmsg@$bctr$qmx6string
    add sp,8
    mov word ptr [bp-26],14
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    push cs
    call @string@$bdtr$qv
    add sp,6
    mov word ptr [bp-26],6

; Original symbolic source block at CODE offset 412
org 412
    call @string@$bctr$qnxc
    add sp,8
    lea ax,[bp-4]
    push ss
    push ax
    push ss
    lea ax,[bp-8]
    push ax

; Original symbolic source block at CODE offset 403
org 403
    mov ax,offset DGROUP:string_out_of_range_message_42
    push ax
    push ss
    lea ax,[bp-4]
    push ax

; Original symbolic source block at CODE offset 389
org 389
    mov ax,offset _TEXT:strings_copy_exception
    push ax
    xor ax,ax
    push ax
    push ax
    mov word ptr [bp-26],6
    push ds

; Original symbolic source block at CODE offset 385
org 385
    mov ax,seg _TEXT
    push ax

; Original symbolic source block at CODE offset 338
org 338
    call ___InitExceptBlocks
    mov ax,[bp+10]
    mov [bp-40],ax
    les bx,[bp+6]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    cmp ax,[bp-40]
    jc strings_4_0171
    mov ax,1
    jmp short strings_4_0173

strings_4_0171:
    xor ax,ax

strings_4_0173:
    or ax,ax
    jnz strings_4_01f4
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax

; Original symbolic source block at CODE offset 335
org 335
    mov bx,offset _TEXT:strings_exception_129

; Original symbolic source block at CODE offset 332
org 332
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 313
org 313
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@assert_index$xqui:
    push bp
    mov bp,sp
    sub sp,40
    push si
    push di

; Original symbolic source block at CODE offset 302
org 302
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,26

strings_4_0136:
    push word ptr [bp-38]

; Original symbolic source block at CODE offset 298
org 298
    mov ax,offset _TEXTC:rtti_string_out_of_range
    push ax

; Original symbolic source block at CODE offset 274
org 274
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    lea ax,[bp-8]
    push ss
    push ax
    push cs

; Original symbolic source block at CODE offset 240
org 240
    call @xmsg@$bctr$qmx6string
    add sp,8
    mov word ptr [bp-26],14
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    push cs
    call @string@$bdtr$qv
    add sp,6
    mov word ptr [bp-26],6

; Original symbolic source block at CODE offset 222
org 222
    call @string@$bctr$qnxc
    add sp,8
    lea ax,[bp-4]
    push ss
    push ax
    push ss
    lea ax,[bp-8]
    push ax

; Original symbolic source block at CODE offset 213
org 213
    mov ax,offset DGROUP:string_out_of_range_message_12
    push ax
    push ss
    lea ax,[bp-4]
    push ax

; Original symbolic source block at CODE offset 199
org 199
    mov ax,offset _TEXT:strings_copy_exception
    push ax
    xor ax,ax
    push ax
    push ax
    mov word ptr [bp-26],6
    push ds

; Original symbolic source block at CODE offset 195
org 195
    mov ax,seg _TEXT
    push ax

; Original symbolic source block at CODE offset 148
org 148
    call ___InitExceptBlocks
    mov ax,[bp+10]
    mov [bp-40],ax
    les bx,[bp+6]
    les bx,es:[bx]
    mov ax,es:[bx+6]
    cmp ax,[bp-40]
    jna strings_4_00b3
    mov ax,1
    jmp short strings_4_00b5

strings_4_00b3:
    xor ax,ax

strings_4_00b5:
    or ax,ax
    jnz strings_4_0136
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax

; Original symbolic source block at CODE offset 145
org 145
    mov bx,offset _TEXT:strings_exception_061

; Original symbolic source block at CODE offset 142
org 142
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 123
org 123
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@assert_element$xqui:
    push bp
    mov bp,sp
    sub sp,40
    push si
    push di

; Original symbolic source block at CODE offset 113
org 113
    call @$bdele$qnv
    pop cx
    pop cx

strings_4_0078:
    push word ptr [bp-30]

; Original symbolic source block at CODE offset 93
org 93
    db 09ah     ; native far CALL, TASM would shorten to PUSH CS/CALL
    dd @TStringRef@$bdtr$qv
    add sp,6

strings_4_0065:
    test byte ptr [bp+10],1
    jz strings_4_0078
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original symbolic source block at CODE offset 61
org 61
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov ax,3
    push ax
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

; Original symbolic source block at CODE offset 19
org 19
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov ax,[bp+6]
    or ax,[bp+8]
    jz strings_4_0078
    les bx,[bp+6]
    les bx,es:[bx]
    dec word ptr es:[bx]
    mov ax,es:[bx]
    or ax,ax
    jnz strings_4_0065

; Original symbolic source block at CODE offset 14
org 14
    call ___InitExceptBlocks

; Original symbolic source block at CODE offset 11
org 11
    mov bx,offset _TEXT:strings_exception_009

; Original symbolic source block at CODE offset 8
org 8
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 0
org 0

@string@$bdtr$qv:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di

; Original Borland CODE4 LEDATA block 1024..2047

; Original symbolic source block at CODE offset 2023
org 2023
    mov DGROUP:@string@freeboard,ax
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

rtti_string_length_error:
    dw 4
    dw 3
    dw 38
    dw -1
    dw 7
    dw 58
    dw 70

; Original symbolic source block at CODE offset 2014
org 2014
    mov ax,DGROUP:@string@freeboard
    mov [bp-2],ax
    mov ax,[bp+6]

; Original symbolic source block at CODE offset 1991
org 1991
    mov word ptr DGROUP:@string@resize_inc,1

strings_4_07cd:
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@max_waste$qui:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di

; Original symbolic source block at CODE offset 1984
org 1984
    cmp word ptr DGROUP:@string@resize_inc,0
    jnz strings_4_07cd

; Original symbolic source block at CODE offset 1981
org 1981
    mov DGROUP:@string@resize_inc,ax

; Original symbolic source block at CODE offset 1972
org 1972
    mov ax,DGROUP:@string@resize_inc
    mov [bp-2],ax
    mov ax,[bp+6]

; Original symbolic source block at CODE offset 1952
org 1952
    mov DGROUP:@string@initial_capac,ax
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@resize_increment$qui:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di

; Original symbolic source block at CODE offset 1943
org 1943
    mov ax,DGROUP:@string@initial_capac
    mov [bp-2],ax
    mov ax,[bp+6]

; Original symbolic source block at CODE offset 1923
org 1923
    mov DGROUP:@string@skip_white,ax
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@initial_capacity$qui:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di

; Original symbolic source block at CODE offset 1914
org 1914
    mov ax,DGROUP:@string@skip_white
    mov [bp-2],ax
    mov ax,[bp+6]

; Original symbolic source block at CODE offset 1894
org 1894
    mov DGROUP:@string@paranoid_check,ax
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@skip_whitespace$qi:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di

; Original symbolic source block at CODE offset 1885
org 1885
    mov ax,DGROUP:@string@paranoid_check
    mov [bp-2],ax
    mov ax,[bp+6]

; Original symbolic source block at CODE offset 1865
org 1865
    mov DGROUP:@string@case_sensitive,ax
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@set_paranoid_check$qi:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di

; Original symbolic source block at CODE offset 1856
org 1856
    mov ax,DGROUP:@string@case_sensitive
    mov [bp-2],ax
    mov ax,[bp+6]

; Original symbolic source block at CODE offset 1837
org 1837
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@string@set_case_sensitive$qi:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di

; Original symbolic source block at CODE offset 1810
org 1810
    call _free
    pop cx
    pop cx
    les bx,[bp+6]
    mov dx,[bp-32]
    mov ax,[bp-34]
    mov es:[bx+4],dx
    mov es:[bx+2],ax

strings_4_072a:
    push word ptr [bp-30]

; Original symbolic source block at CODE offset 1741
org 1741
    call _memset
    add sp,8

strings_4_06d5:
    les bx,[bp+6]
    mov ax,[bp-36]
    mov es:[bx+6],ax
    push es
    les ax,[bp-34]
    mov dx,es
    pop es
    add ax,es:[bx+6]
    mov bx,ax
    mov es,dx
    mov byte ptr es:[bx],0
    les bx,[bp+6]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    cmp dx,[bp-32]
    jnz strings_4_0707
    cmp ax,[bp-34]
    jz strings_4_072a

strings_4_0707:
    les bx,[bp+6]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

; Original symbolic source block at CODE offset 1714
org 1714
    call _memmove
    add sp,10
    jmp short strings_4_06d5

strings_4_06bc:
    push word ptr [bp+18]
    mov ax,32
    push ax
    mov ax,[bp-34]
    add ax,[bp+10]
    push word ptr [bp-32]
    push ax

; Original symbolic source block at CODE offset 1673
org 1673
    call _memmove
    add sp,10

strings_4_0691:
    cmp word ptr [bp+18],0
    jz strings_4_06d5
    mov ax,[bp+14]
    or ax,[bp+16]
    jz strings_4_06bc
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    mov ax,[bp-34]
    add ax,[bp+10]
    push word ptr [bp-32]
    push ax

; Original symbolic source block at CODE offset 1565
org 1565
    call _memcpy
    add sp,10

strings_4_0625:
    les bx,[bp+6]
    mov ax,[bp-38]
    mov es:[bx+8],ax
    jmp short strings_4_0642

strings_4_0631:
    les bx,[bp+6]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    mov [bp-32],dx
    mov [bp-34],ax

strings_4_0642:
    les bx,[bp+6]
    mov dx,es:[bx+4]
    mov ax,es:[bx+2]
    cmp dx,[bp-32]
    jnz strings_4_065f
    cmp ax,[bp-34]
    jnz strings_4_065f
    mov ax,[bp+18]
    cmp ax,[bp+12]
    jz strings_4_0691

strings_4_065f:
    les bx,[bp+6]
    mov ax,es:[bx+6]
    sub ax,[bp+10]
    sub ax,[bp+12]
    push ax
    mov ax,es:[bx+2]
    add ax,[bp+10]
    add ax,[bp+12]
    push word ptr es:[bx+4]
    push ax
    mov ax,[bp-34]
    add ax,[bp+10]
    add ax,[bp+18]
    push word ptr [bp-32]
    push ax

; Original symbolic source block at CODE offset 1532
org 1532
    call @xalloc@raise$qv
    pop cx
    pop cx

strings_4_0603:
    cmp word ptr [bp+10],0
    jz strings_4_0625
    push word ptr [bp+10]
    les bx,[bp+6]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    push word ptr [bp-32]
    push word ptr [bp-34]

; Original symbolic source block at CODE offset 1528
org 1528
    mov ax,offset DGROUP:___xalloc
    push ax

; Original symbolic source block at CODE offset 1502
org 1502
    call _malloc
    pop cx
    mov [bp-32],dx
    mov [bp-34],ax
    les bx,[bp+6]
    mov ax,es:[bx+2]
    or ax,es:[bx+4]
    jnz strings_4_0603
    push ds

; Original symbolic source block at CODE offset 1484
org 1484
    cmp ax,DGROUP:@string@freeboard
    jna strings_4_0631
    test byte ptr es:[bx+10],1
    jnz strings_4_0631
    mov ax,[bp-38]
    inc ax
    push ax

; Original symbolic source block at CODE offset 1416
org 1416
    call ___InitExceptBlocks
    les bx,[bp+6]
    mov ax,es:[bx+6]
    add ax,[bp+18]
    sub ax,[bp+12]
    mov [bp-36],ax
    push ax
    push cs
    call @TStringRef@round_capacity$qui
    pop cx
    mov [bp-38],ax
    les bx,[bp+6]
    mov ax,es:[bx+8]
    cmp ax,[bp-38]
    jnc strings_4_05c2
    push word ptr [bp-38]
    push word ptr [bp+8]
    push bx
    push cs
    call @TStringRef@grow_to$qui
    add sp,6
    jmp short strings_4_0631

strings_4_05c2:
    les bx,[bp+6]
    mov ax,es:[bx+8]
    sub ax,[bp-38]

; Original symbolic source block at CODE offset 1413
org 1413
    mov bx,offset _TEXT:strings_exception_297

; Original symbolic source block at CODE offset 1410
org 1410
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 1390
org 1390
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TStringRef@splice$quiuinxcui:
    push bp
    mov bp,sp
    sub sp,38
    push si
    push di

; Original symbolic source block at CODE offset 1364
org 1364
    mov cx,DGROUP:@string@resize_inc
    mov ax,[bp+6]
    sub ax,[bp-32]
    add ax,cx
    dec ax
    xor dx,dx
    div cx
    imul cx
    add ax,[bp-32]
    push ax
    push word ptr [bp-30]

; Original symbolic source block at CODE offset 1358
org 1358
    mov ax,DGROUP:@string@initial_capac
    mov [bp-32],ax

; Original symbolic source block at CODE offset 1353
org 1353
    call ___InitExceptBlocks

; Original symbolic source block at CODE offset 1350
org 1350
    mov bx,offset _TEXT:strings_exception_279

; Original symbolic source block at CODE offset 1347
org 1347
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 1328
org 1328
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TStringRef@round_capacity$qui:
    push bp
    mov bp,sp
    sub sp,32
    push si
    push di

; Original symbolic source block at CODE offset 1318
org 1318
    call @xalloc@raise$qv
    pop cx
    pop cx

strings_4_052d:
    push word ptr [bp-30]

; Original symbolic source block at CODE offset 1314
org 1314
    mov ax,offset DGROUP:___xalloc
    push ax

; Original symbolic source block at CODE offset 1284
org 1284
    call _realloc
    add sp,6
    les bx,[bp+6]
    mov es:[bx+4],dx
    mov es:[bx+2],ax
    mov ax,es:[bx+2]
    or ax,es:[bx+4]
    jnz strings_4_052d
    push ds

; Original symbolic source block at CODE offset 1255
org 1255
    call ___InitExceptBlocks
    les bx,[bp+6]
    mov ax,[bp+10]
    mov es:[bx+8],ax
    mov ax,es:[bx+8]
    inc ax
    push ax
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

; Original symbolic source block at CODE offset 1252
org 1252
    mov bx,offset _TEXT:strings_exception_269

; Original symbolic source block at CODE offset 1249
org 1249
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 1230
org 1230
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TStringRef@grow_to$qui:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di

; Original symbolic source block at CODE offset 1201
org 1201
    call _realloc
    add sp,6
    les bx,[bp+6]
    mov es:[bx+4],dx
    mov es:[bx+2],ax
    mov ax,[bp-32]
    mov es:[bx+8],ax

strings_4_04cb:
    push word ptr [bp-30]

; Original symbolic source block at CODE offset 1182
org 1182
    cmp ax,DGROUP:@string@freeboard
    jna strings_4_04cb
    mov ax,[bp-32]
    inc ax
    push ax
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

; Original symbolic source block at CODE offset 1163
org 1163
    db 09ah     ; native far CALL, TASM would shorten to PUSH CS/CALL
    dd @TStringRef@round_capacity$qui
    pop cx
    mov [bp-32],ax
    les bx,[bp+6]
    mov ax,es:[bx+8]
    sub ax,[bp-32]

; Original symbolic source block at CODE offset 1151
org 1151
    call ___InitExceptBlocks
    les bx,[bp+6]
    push word ptr es:[bx+6]

; Original symbolic source block at CODE offset 1148
org 1148
    mov bx,offset _TEXT:strings_exception_251

; Original symbolic source block at CODE offset 1145
org 1145
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 1126
org 1126
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TStringRef@check_freeboard$qv:
    push bp
    mov bp,sp
    sub sp,32
    push si
    push di

; Original symbolic source block at CODE offset 1097
org 1097
    call _realloc
    add sp,6
    les bx,[bp+6]
    mov es:[bx+4],dx
    mov es:[bx+2],ax
    mov ax,[bp-32]
    mov es:[bx+8],ax

strings_4_0463:
    push word ptr [bp-30]

; Original symbolic source block at CODE offset 1078
org 1078
    cmp ax,DGROUP:@string@freeboard
    jna strings_4_0463
    mov ax,[bp-32]
    inc ax
    push ax
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

; Original symbolic source block at CODE offset 1059
org 1059
    db 09ah     ; native far CALL, TASM would shorten to PUSH CS/CALL
    dd @TStringRef@round_capacity$qui
    pop cx
    mov [bp-32],ax
    les bx,[bp+6]
    mov ax,es:[bx+8]
    sub ax,[bp-32]

; Original symbolic source block at CODE offset 1041
org 1041
    call ___InitExceptBlocks
    les bx,[bp+6]
    or word ptr es:[bx+10],1
    mov ax,[bp+10]
    inc ax
    push ax

; Original symbolic source block at CODE offset 1038
org 1038
    mov bx,offset _TEXT:strings_exception_241

; Original symbolic source block at CODE offset 1035
org 1035
    mov ax,seg _TEXT

; Original symbolic source block at CODE offset 1025
org 1025
    pop bp
    retf

@TStringRef@reserve$qui:
    push bp
    mov bp,sp
    sub sp,32
    push si
    push di

; Original Borland CODE4 LEDATA block 2048..2370

; Original symbolic source block at CODE offset 2351
org 2351
    dd rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

; Original symbolic source block at CODE offset 2323
org 2323
    dd strings_destruct_out_of_range
    dw 5
    dw 74
    db 'string::outofrange',0,0

; Original symbolic source block at CODE offset 2265
org 2265
    dd @string@$bdtr$qv
    dw 5
    dw 54
    db 'string',0,0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_string_out_of_range:
    dw 4
    dw 3
    dw 38
    dw -1
    dw 7
    dw 58
    dw 70
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 2
    dw 2

; Original symbolic source block at CODE offset 2209
org 2209
    dd @xmsg@$bdtr$qv
    dw 5
    dw 52
    db 'xmsg',0,0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_string:
    dw 4
    dw 3
    dw 38
    dw -1
    dw 3
    dw 46
    dw 50
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 1
    dw 1

; Original symbolic source block at CODE offset 2159
org 2159
    dd rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_xmsg:
    dw 4
    dw 3
    dw 38
    dw -1
    dw 3
    dw 44
    dw 48
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 1
    dw 1

; Original symbolic source block at CODE offset 2143
org 2143
    dd strings_destruct_xalloc
    dw 5
    dw 62
    db 'xalloc',0,0

; Original symbolic source block at CODE offset 2093
org 2093
    dd rtti_xmsg
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_xalloc:
    dw 6
    dw 3
    dw 38
    dw -1
    dw 7
    dw 46
    dw 58
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 2
    dw 2

; Original symbolic source block at CODE offset 2065
org 2065
    dd strings_destruct_length_error
    dw 5
    dw 74
    db 'string::lengtherror',0

; Original symbolic source block at CODE offset 2049
org 2049
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 2
    dw 2
_TEXTC ends
end
