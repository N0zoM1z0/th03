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
    dw offset _TEXT:checks_exception_header_0

checks_frame_028:
    dd rtti_ostrstream
    dw 4
    dw -98
    dw 0
    dw 0
    dw 0

checks_frame_042:
    dd rtti_pointer_string
    dw 148
    dw 6
    dw 0
    dw 0
    dw 0

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
    dw offset _TEXT:checks_frame_028
    dw 6
    dw 5
    dw 6
    dw offset _TEXT:checks_frame_042
    dw 14
    dw 5
    dw 6
    dw offset _TEXT:checks_frame_056

checks_frame_100:
    dd rtti_ostrstream
    dw 0
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
    dw offset _TEXT:checks_frame_100

checks_static_initializer:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di
    mov ax,seg _TEXT
    mov bx,offset _TEXT:checks_frame_114
    call ___InitExceptBlocks
    mov word ptr [bp-18],6
    mov ax,2
    push ax
    mov ax,256
    push ax
    push ax
    call @$bnwa$qui
    pop cx
    push dx
    push ax
    xor ax,ax
    push ax
    push ds
    mov ax,offset DGROUP:@TDiagBase@Out
    push ax
    call @ostrstream@$bctr$qncii
    add sp,14
    push word ptr [bp-30]
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
    mov ax,offset DGROUP:@TDiagBase@Out
    push ax
    call @ostrstream@$bdtr$qv
    add sp,6
    pop di
    pop si
    retf

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

@TDiagGroupDef@Trace$qucnxct2ul:
    push bp
    mov bp,sp
    push si
    push di
    mov al,DGROUP:[@TDiagGroupDef@Flags]
    and ax,1
    jz diag_branch_4_003c
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
    push word DGROUP:[@TDiagGroupDef@Name+2]
    push word DGROUP:[@TDiagGroupDef@Name]
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
    mov al,DGROUP:[@TDiagGroupDef@Flags]
    and ax,1
    jz diag_branch_4_007c
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
    push word DGROUP:[@TDiagGroupDef@Name+2]
    push word DGROUP:[@TDiagGroupDef@Name]
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
    mov ax,offset DGROUP:_cout
    push ax
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
    mov ax,seg _TEXT
    mov bx,offset _TEXT:checks_frame_014
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
    call @ostream@outstr$qnxct1
    add sp,12
    lea ax,[bp-44]
    push ss
    push ax
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
    call @ostream@outstr$qnxct1
    add sp,12
    push word ptr [bp-146]
    push word ptr [bp-148]
    call @ostream@$blsh$qc
    add sp,6
    push dx
    push ax
    call @ostream@$blsh$qul
    add sp,8
    mov [bp-150],dx
    mov [bp-152],ax
    xor ax,ax
    push ax
    push ax
    push ds
    mov ax,offset DGROUP:diag_colon_bracket
    push ax
    push dx
    push word ptr [bp-152]
    call @ostream@outstr$qnxct1
    xor ax,ax
    push ax
    push ax
    push word ptr [bp-134]
    push word ptr [bp-136]
    push word ptr [bp-150]
    push word ptr [bp-152]
    call @ostream@outstr$qnxct1
    xor ax,ax
    push ax
    push ax
    push ds
    mov ax,offset DGROUP:diag_bracket_space
    push ax
    push word ptr [bp-150]
    push word ptr [bp-152]
    call @ostream@outstr$qnxct1
    xor ax,ax
    push ax
    push ax
    push word ptr [bp-130]
    push word ptr [bp-132]
    push word ptr [bp-150]
    push word ptr [bp-152]
    call @ostream@outstr$qnxct1
    add sp,48
    xor ax,ax
    push ax
    push ax
    push ds
    mov ax,offset DGROUP:diag_crlf
    push ax
    push word ptr [bp-150]
    push word ptr [bp-152]
    call @ostream@outstr$qnxct1
    push word ptr [bp-150]
    push word ptr [bp-152]
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
    call @ostrstream@$bdtr$qv
    add sp,26
    push word ptr [bp-128]
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
    mov ax,seg _TEXT
    mov bx,offset _TEXT:checks_frame_070
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
    call @ostream@outstr$qnxct1
    add sp,12
    xor ax,ax
    push ax
    push ax
    push ds
    mov ax,offset DGROUP:diag_failed_word
    push ax
    push ss
    lea ax,[bp-44]
    push ax
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
    call @ostream@outstr$qnxct1
    add sp,12
    lea ax,[bp-44]
    push ss
    push ax
    call @ostream@$blsh$qc
    add sp,6
    push dx
    push ax
    call @ostream@$blsh$qul
    add sp,8
    mov [bp-142],dx
    mov [bp-144],ax
    xor ax,ax
    push ax
    push ax
    push ds
    mov ax,offset DGROUP:diag_colon_space
    push ax
    push dx
    push word ptr [bp-144]
    call @ostream@outstr$qnxct1
    xor ax,ax
    push ax
    push ax
    push word ptr [bp-130]
    push word ptr [bp-132]
    push word ptr [bp-142]
    push word ptr [bp-144]
    call @ostream@outstr$qnxct1
    push word ptr [bp-142]
    push word ptr [bp-144]
    call @ends$qm7ostream
    mov word ptr [bp-116],14
    push ss
    lea ax,[bp-400]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
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
    call @ostrstream@$bdtr$qv
    add sp,6
    push word ptr [bp-128]
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
    dd rtti_string
    db 'string *',0    ; string pointer RTTI

rtti_ostrstream:
    dw 98
    dw 3
    dw 38
    dw 2
    dw 127
    dw 50

; Original BCC CODE4 LEDATA 1024..1486
    dw 70
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 6
    dw 5
    dd @ostrstream@$bdtr$qv
    dw 5
    dw 82
    db 'ostrstream',0,0    ; ostrstream RTTI
    dd rtti_strstreambase
    dw 0
    dw 3
    dd rtti_ostream
    dw 54
    dw 3
    dw 0
    dw 0
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
    dd @ostream@$bdtr$qv
    dw 5
    dw 62
    db 'ostream',0,0,0,0,0    ; ostream RTTI
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
    dd @strstreambase@$bdtr$qv
    dw 5
    dw 68
    db 'strstreambase',0,0,0,0,0    ; strstreambase RTTI
    dd rtti_ios
    dw 0
    dw 7
    dw 0
    dw 0
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
    dd @strstreambuf@$bdtr$qv
    dw 5
    dw 68
    db 'strstreambuf',0,0    ; strstreambuf RTTI
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
    dd @streambuf@$bdtr$qv
    dw 5
    dw 56
    db 'streambuf',0,0,0,0,0,0,0,0,0,0,0,0,0    ; streambuf RTTI

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
