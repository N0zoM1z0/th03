; Complete original Japanese Borland diagnostic/exception runtime checks.
; Seven far code methods + three original public DATA symbols,
; native output/strstream formatting and typed Borland C++ exception RTTI.
; Two original INIT/EXIT records. All executable statements are real 8086.
.8086
extrn @$bnwa$qui:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @string@$bctr$qnxc:far
extrn @string@$bdtr$qv:far
extrn @ios@$bdtr$qv:far
extrn @streambuf@$bdtr$qv:far
extrn @ostream@$bdtr$qv:far
extrn @ostream@$blsh$qc:far
extrn @ostream@$blsh$qul:far
extrn @ostream@outstr$qnxct1:far
extrn _cout:word
extrn @ends$qm7ostream:far
extrn @strstreambuf@$bdtr$qv:far
extrn @strstreambase@$bdtr$qv:far
extrn @ostrstream@$bctr$qncii:far
extrn @ostrstream@$bdtr$qv:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
_TEXTC ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
_EXIT_ segment word public 'EXITDATA'
_EXIT_ ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Original relocated 8086 or metadata source at +210
org 210
    call @ostrstream@$bdtr$qv
    add sp,6
    pop di
    pop si
    retf

; Original relocated 8086 or metadata source at +206
org 206
    mov ax,offset DGROUP:@TDiagBase@Out
    push ax

; Original relocated 8086 or metadata source at +188
org 188
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

checks_static_finalizer:
    push si
    push di
    mov ax,2
    push ax
    push ds

; Original relocated 8086 or metadata source at +177
org 177
    call @ostrstream@$bctr$qncii
    add sp,14
    push word ptr [bp-30]

; Original relocated 8086 or metadata source at +173
org 173
    mov ax,offset DGROUP:@TDiagBase@Out
    push ax

; Original relocated 8086 or metadata source at +161
org 161
    call @$bnwa$qui
    pop cx
    push dx
    push ax
    xor ax,ax
    push ax
    push ds

; Original relocated 8086 or metadata source at +142
org 142
    call ___InitExceptBlocks
    mov word ptr [bp-18],6
    mov ax,2
    push ax
    mov ax,256
    push ax
    push ax

; Original relocated 8086 or metadata source at +139
org 139
    mov bx,offset _TEXT:checks_frame_114

; Original relocated 8086 or metadata source at +136
org 136
    mov ax,seg _TEXT

; Original relocated 8086 or metadata source at +126
org 126
    dw offset _TEXT:checks_frame_100

checks_static_initializer:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di

; Original relocated 8086 or metadata source at +106
org 106
    dd DGROUP:@TDiagBase@Out
    dw 0
    dw 0

checks_frame_114:
    dw 0
    dw 0
    dw -30
    dw 0
    dw 5
    dw 0

; Original relocated 8086 or metadata source at +100
org 100

checks_frame_100:
    dd rtti_ostrstream
    dw 0

; Original relocated 8086 or metadata source at +98
org 98
    dw offset _TEXT:checks_frame_056

; Original relocated 8086 or metadata source at +90
org 90
    dw offset _TEXT:checks_frame_042
    dw 14
    dw 5
    dw 6

; Original relocated 8086 or metadata source at +82
org 82
    dw offset _TEXT:checks_frame_028
    dw 6
    dw 5
    dw 6

; Original relocated 8086 or metadata source at +56
org 56

checks_frame_056:
    dd rtti_pointer_string
    dw 180
    dw 6
    dw 0
    dw 0
    dw 0

checks_frame_070:
    dw 0
    dw 0
    dw -128
    dw 0
    dw 5
    dw 0

; Original relocated 8086 or metadata source at +42
org 42

checks_frame_042:
    dd rtti_pointer_string
    dw 148
    dw 6
    dw 0
    dw 0
    dw 0

; Original relocated 8086 or metadata source at +28
org 28

checks_frame_028:
    dd rtti_ostrstream
    dw 4
    dw -98
    dw 0
    dw 0
    dw 0

; Original relocated 8086 or metadata source at +26
org 26
    dw offset _TEXT:checks_exception_header_0

; Original relocated 8086 or metadata source at +0
org 0

checks_exception_header_0:
    dd rtti_ostrstream
    dw 4
    dw -98
    dw 0
    dw 0
    dw 0

checks_frame_014:
    dw 0
    dw 0
    dw -128
    dw 0
    dw 5
    dw 0

_TEXT ends

_DATA segment word public 'DATA'
public @TDiagGroupDef@Name,@TDiagGroupDef@Flags,@TDiagBase@Out
@TDiagGroupDef@Name dd DGROUP:diag_default_name
@TDiagGroupDef@Flags db 1
@TDiagBase@Out db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
diag_default_name db 'Def',0
diag_colon_bracket db ': [',0
diag_bracket_space db '] ',0
diag_crlf db 10, 13, 0
diag_trace_word db 'Trace',0
diag_warning_word db 'Warning',0
diag_failed_word db ' failed ',0
diag_colon_space db ': ',0

_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @TDiagGroupDef@Trace$qucnxct2ul
public @TDiagGroupDef@Warn$qucnxct2ul
public @TDiagBase@Output$qnxc
public @TDiagBase@Message$qnxct1t1t1ul
public @TDiagBase@Trace$qnxct1t1ul
public @TDiagBase@Warn$qnxct1t1ul
public @xerror@MakeString$qnxct1t1ul

; Original BCC CODE4 LEDATA 0..1023

; Original relocated 8086 or metadata source at +1000
org 1000
    dd rtti_string
    db 'string *',0    ; string pointer RTTI

rtti_ostrstream:
    dw 98
    dw 3
    dw 38
    dw 2
    dw 127
    dw 50

; Original relocated 8086 or metadata source at +981
org 981
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

rtti_pointer_string:
    dw 4
    dw 8208
    dw 10

; Original relocated 8086 or metadata source at +970
org 970
    call @ostrstream@$bdtr$qv
    add sp,6
    push word ptr [bp-128]

; Original relocated 8086 or metadata source at +940
org 940
    call @string@$bctr$qnxc
    add sp,36
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov word ptr [bp-116],22
    push dx
    push ax
    mov ax,2
    push ax
    push ss
    lea ax,[bp-98]
    push ax

; Original relocated 8086 or metadata source at +918
org 918
    call @ends$qm7ostream
    mov word ptr [bp-116],14
    push ss
    lea ax,[bp-400]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

; Original relocated 8086 or metadata source at +905
org 905
    call @ostream@outstr$qnxct1
    push word ptr [bp-142]
    push word ptr [bp-144]

; Original relocated 8086 or metadata source at +880
org 880
    call @ostream@outstr$qnxct1
    xor ax,ax
    push ax
    push ax
    push word ptr [bp-130]
    push word ptr [bp-132]
    push word ptr [bp-142]
    push word ptr [bp-144]

; Original relocated 8086 or metadata source at +871
org 871
    mov ax,offset DGROUP:diag_colon_space
    push ax
    push dx
    push word ptr [bp-144]

; Original relocated 8086 or metadata source at +850
org 850
    call @ostream@$blsh$qul
    add sp,8
    mov [bp-142],dx
    mov [bp-144],ax
    xor ax,ax
    push ax
    push ax
    push ds

; Original relocated 8086 or metadata source at +840
org 840
    call @ostream@$blsh$qc
    add sp,6
    push dx
    push ax

; Original relocated 8086 or metadata source at +827
org 827
    call @ostream@outstr$qnxct1
    add sp,12
    lea ax,[bp-44]
    push ss
    push ax

; Original relocated 8086 or metadata source at +802
org 802
    call @ostream@outstr$qnxct1
    add sp,12
    xor ax,ax
    push ax
    push ax
    push word ptr [bp-134]
    push word ptr [bp-136]
    push ss
    lea ax,[bp-44]
    push ax

; Original relocated 8086 or metadata source at +793
org 793
    mov ax,offset DGROUP:diag_failed_word
    push ax
    push ss
    lea ax,[bp-44]
    push ax

; Original relocated 8086 or metadata source at +780
org 780
    call @ostream@outstr$qnxct1
    add sp,12
    xor ax,ax
    push ax
    push ax
    push ds

; Original relocated 8086 or metadata source at +707
org 707
    call @ostrstream@$bctr$qncii
    add sp,14
    mov dx,[bp+16]
    mov ax,[bp+14]
    mov [bp-130],dx
    mov [bp-132],ax
    push word ptr [bp+24]
    push word ptr [bp+22]
    mov al,32
    push ax
    mov dx,[bp+20]
    mov ax,[bp+18]
    mov [bp-134],dx
    mov [bp-136],ax
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-138],dx
    mov [bp-140],ax
    xor ax,ax
    push ax
    push ax
    push dx
    push word ptr [bp-140]
    push ss
    lea ax,[bp-44]
    push ax

; Original relocated 8086 or metadata source at +675
org 675
    call ___InitExceptBlocks
    mov word ptr [bp-116],6
    mov ax,2
    push ax
    mov ax,256
    push ax
    push ss
    lea ax,[bp-400]
    push ax
    xor ax,ax
    push ax
    push ss
    lea ax,[bp-98]
    push ax

; Original relocated 8086 or metadata source at +672
org 672
    mov bx,offset _TEXT:checks_frame_070

; Original relocated 8086 or metadata source at +669
org 669
    mov ax,seg _TEXT

; Original relocated 8086 or metadata source at +645
org 645
    mov ax,offset DGROUP:diag_warning_word
    push ax
    push cs
    call @TDiagBase@Message$qnxct1t1t1ul
    add sp,20
    pop di
    pop si
    pop bp
    retf

@xerror@MakeString$qnxct1t1ul:
    push bp
    mov bp,sp
    sub sp,400
    push si
    push di

; Original relocated 8086 or metadata source at +600
org 600
    mov ax,offset DGROUP:diag_trace_word
    push ax
    push cs
    call @TDiagBase@Message$qnxct1t1t1ul
    add sp,20
    pop di
    pop si
    pop bp
    retf

@TDiagBase@Warn$qnxct1t1ul:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+20]
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ds

; Original relocated 8086 or metadata source at +559
org 559
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TDiagBase@Trace$qnxct1t1ul:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+20]
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ds

; Original relocated 8086 or metadata source at +548
org 548
    call @ostrstream@$bdtr$qv
    add sp,26
    push word ptr [bp-128]

; Original relocated 8086 or metadata source at +524
org 524
    call @ends$qm7ostream
    push ss
    lea ax,[bp-408]
    push ax
    push cs
    call @TDiagBase@Output$qnxc
    mov ax,2
    push ax
    push ss
    lea ax,[bp-98]
    push ax

; Original relocated 8086 or metadata source at +511
org 511
    call @ostream@outstr$qnxct1
    push word ptr [bp-150]
    push word ptr [bp-152]

; Original relocated 8086 or metadata source at +499
org 499
    mov ax,offset DGROUP:diag_crlf
    push ax
    push word ptr [bp-150]
    push word ptr [bp-152]

; Original relocated 8086 or metadata source at +486
org 486
    call @ostream@outstr$qnxct1
    add sp,48
    xor ax,ax
    push ax
    push ax
    push ds

; Original relocated 8086 or metadata source at +461
org 461
    call @ostream@outstr$qnxct1
    xor ax,ax
    push ax
    push ax
    push word ptr [bp-130]
    push word ptr [bp-132]
    push word ptr [bp-150]
    push word ptr [bp-152]

; Original relocated 8086 or metadata source at +449
org 449
    mov ax,offset DGROUP:diag_bracket_space
    push ax
    push word ptr [bp-150]
    push word ptr [bp-152]

; Original relocated 8086 or metadata source at +439
org 439
    call @ostream@outstr$qnxct1
    xor ax,ax
    push ax
    push ax
    push ds

; Original relocated 8086 or metadata source at +414
org 414
    call @ostream@outstr$qnxct1
    xor ax,ax
    push ax
    push ax
    push word ptr [bp-134]
    push word ptr [bp-136]
    push word ptr [bp-150]
    push word ptr [bp-152]

; Original relocated 8086 or metadata source at +405
org 405
    mov ax,offset DGROUP:diag_colon_bracket
    push ax
    push dx
    push word ptr [bp-152]

; Original relocated 8086 or metadata source at +384
org 384
    call @ostream@$blsh$qul
    add sp,8
    mov [bp-150],dx
    mov [bp-152],ax
    xor ax,ax
    push ax
    push ax
    push ds

; Original relocated 8086 or metadata source at +374
org 374
    call @ostream@$blsh$qc
    add sp,6
    push dx
    push ax

; Original relocated 8086 or metadata source at +358
org 358
    call @ostream@outstr$qnxct1
    add sp,12
    push word ptr [bp-146]
    push word ptr [bp-148]

; Original relocated 8086 or metadata source at +325
org 325
    call @ostream@$blsh$qc
    add sp,6
    mov [bp-146],dx
    mov [bp-148],ax
    xor ax,ax
    push ax
    push ax
    push word ptr [bp-138]
    push word ptr [bp-140]
    push dx
    push word ptr [bp-148]

; Original relocated 8086 or metadata source at +312
org 312
    call @ostream@outstr$qnxct1
    add sp,12
    lea ax,[bp-44]
    push ss
    push ax

; Original relocated 8086 or metadata source at +222
org 222
    call @ostrstream@$bctr$qncii
    add sp,14
    mov dx,[bp+16]
    mov ax,[bp+14]
    mov [bp-130],dx
    mov [bp-132],ax
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-134],dx
    mov [bp-136],ax
    push word ptr [bp+24]
    push word ptr [bp+22]
    mov al,32
    push ax
    mov dx,[bp+20]
    mov ax,[bp+18]
    mov [bp-138],dx
    mov [bp-140],ax
    mov al,32
    push ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-142],dx
    mov [bp-144],ax
    xor ax,ax
    push ax
    push ax
    push dx
    push word ptr [bp-144]
    push ss
    lea ax,[bp-44]
    push ax

; Original relocated 8086 or metadata source at +190
org 190
    call ___InitExceptBlocks
    mov word ptr [bp-116],6
    mov ax,2
    push ax
    mov ax,256
    push ax
    push ss
    lea ax,[bp-408]
    push ax
    xor ax,ax
    push ax
    push ss
    lea ax,[bp-98]
    push ax

; Original relocated 8086 or metadata source at +187
org 187
    mov bx,offset _TEXT:checks_frame_014

; Original relocated 8086 or metadata source at +184
org 184
    mov ax,seg _TEXT

; Original relocated 8086 or metadata source at +161
org 161
    call @ostream@outstr$qnxct1
    add sp,12
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TDiagBase@Message$qnxct1t1t1ul:
    push bp
    mov bp,sp
    sub sp,408
    push si
    push di

; Original relocated 8086 or metadata source at +157
org 157
    mov ax,offset DGROUP:_cout
    push ax

; Original relocated 8086 or metadata source at +116
org 116
    db 09ah
    dd @TDiagBase@Warn$qnxct1t1ul
    add sp,16

diag_branch_4_007c:
    pop di
    pop si
    pop bp
    retf

@TDiagBase@Output$qnxc:
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-2],dx
    mov [bp-4],ax
    xor ax,ax
    push ax
    push ax
    push dx
    push word ptr [bp-4]
    push ds

; Original relocated 8086 or metadata source at +112
org 112
    push word ptr DGROUP:[@TDiagGroupDef@Name]

; Original relocated 8086 or metadata source at +108
org 108
    push word ptr DGROUP:[@TDiagGroupDef@Name+2]

; Original relocated 8086 or metadata source at +77
org 77
    mov al,DGROUP:[@TDiagGroupDef@Flags]
    shr ax,1
    and ax,127
    cmp al,[bp+6]
    jc diag_branch_4_007c
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]

; Original relocated 8086 or metadata source at +69
org 69
    mov al,DGROUP:[@TDiagGroupDef@Flags]
    and ax,1
    jz diag_branch_4_007c

; Original relocated 8086 or metadata source at +52
org 52
    db 09ah
    dd @TDiagBase@Trace$qnxct1t1ul
    add sp,16

diag_branch_4_003c:
    pop di
    pop si
    pop bp
    retf

@TDiagGroupDef@Warn$qucnxct2ul:
    push bp
    mov bp,sp
    push si
    push di

; Original relocated 8086 or metadata source at +48
org 48
    push word ptr DGROUP:[@TDiagGroupDef@Name]

; Original relocated 8086 or metadata source at +44
org 44
    push word ptr DGROUP:[@TDiagGroupDef@Name+2]

; Original relocated 8086 or metadata source at +13
org 13
    mov al,DGROUP:[@TDiagGroupDef@Flags]
    shr ax,1
    and ax,127
    cmp al,[bp+6]
    jc diag_branch_4_003c
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]

; Original relocated 8086 or metadata source at +5
org 5
    mov al,DGROUP:[@TDiagGroupDef@Flags]
    and ax,1
    jz diag_branch_4_003c

; Original relocated 8086 or metadata source at +0
org 0

@TDiagGroupDef@Trace$qucnxct2ul:
    push bp
    mov bp,sp
    push si
    push di

; Original BCC CODE4 LEDATA 1024..1486

; Original relocated 8086 or metadata source at +1457
org 1457
    dd @streambuf@$bdtr$qv
    dw 5
    dw 56
    db 'streambuf',0,0,0,0,0,0,0,0,0,0,0,0,0    ; streambuf RTTI

; Original relocated 8086 or metadata source at +1407
org 1407
    dd rtti_streambuf
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_streambuf:
    dw 38
    dw 3
    dw 38
    dw 0
    dw 115
    dw 48
    dw 52
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 1
    dw 1

; Original relocated 8086 or metadata source at +1385
org 1385
    dd @strstreambuf@$bdtr$qv
    dw 5
    dw 68
    db 'strstreambuf',0,0    ; strstreambuf RTTI

; Original relocated 8086 or metadata source at +1327
org 1327
    dd @string@$bdtr$qv
    dw 5
    dw 54
    db 'string',0,0,0,0,0,0,0,0,0,0,0,0,0,0    ; string RTTI

rtti_strstreambuf:
    dw 50
    dw 3
    dw 38
    dw 0
    dw 119
    dw 52
    dw 64
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 2
    dw 2

; Original relocated 8086 or metadata source at +1287
org 1287
    dd rtti_strstreambuf
    dw 4
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

; Original relocated 8086 or metadata source at +1275
org 1275
    dd rtti_ios
    dw 0
    dw 7
    dw 0
    dw 0

; Original relocated 8086 or metadata source at +1249
org 1249
    dd @strstreambase@$bdtr$qv
    dw 5
    dw 68
    db 'strstreambase',0,0,0,0,0    ; strstreambase RTTI

; Original relocated 8086 or metadata source at +1203
org 1203
    dd rtti_ios
    dw 0
    dw 7
    dw 0
    dw 0
    dw 0
    dw 0

rtti_strstreambase:
    dw 94
    dw 3
    dw 38
    dw 2
    dw 127
    dw 52
    dw 56
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 4
    dw 3

; Original relocated 8086 or metadata source at +1183
org 1183
    dd @ostream@$bdtr$qv
    dw 5
    dw 62
    db 'ostream',0,0,0,0,0    ; ostream RTTI

; Original relocated 8086 or metadata source at +1129
org 1129
    dd @ios@$bdtr$qv
    dw 5
    dw 50
    db 'ios',0,0,0,0,0,0,0,0,0,0,0,0,0    ; ios RTTI

rtti_ostream:
    dw 44
    dw 3
    dw 38
    dw 2
    dw 127
    dw 46
    dw 50
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 2
    dw 1

; Original relocated 8086 or metadata source at +1083
org 1083
    dd rtti_ios
    dw 0
    dw 13
    dw 0
    dw 0
    dw 0
    dw 0

rtti_ios:
    dw 40
    dw 3
    dw 38
    dw 0
    dw 115
    dw 42
    dw 46
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 1
    dw 1

; Original relocated 8086 or metadata source at +1071
org 1071
    dd rtti_ostream
    dw 54
    dw 3
    dw 0
    dw 0

; Original relocated 8086 or metadata source at +1063
org 1063
    dd rtti_strstreambase
    dw 0
    dw 3

; Original relocated 8086 or metadata source at +1043
org 1043
    dd @ostrstream@$bdtr$qv
    dw 5
    dw 82
    db 'ostrstream',0,0    ; ostrstream RTTI

; Original relocated 8086 or metadata source at +1025
org 1025
    dw 70
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 6
    dw 5

_TEXTC ends

_INIT_ segment word public 'INITDATA'
    dw 2001h
    dd checks_static_initializer
_INIT_ ends

_EXIT_ segment word public 'EXITDATA'
    dw 2001h
    dd checks_static_finalizer
_EXIT_ ends
end
