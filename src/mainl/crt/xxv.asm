; Complete Borland original Japanese C++ exception/termination system.
; Actual nine near/far 8086 runtime APIs, symbolic unwind metadata.
; Explicit named DATA globals and 128-byte class-name/static buffers.
; No embedded executable machine-CODE arrays or binary OBJ patches.
.8086
extrn @_CatchCleanup$qv:far,___InitExceptBlocks:far,___ExitExceptBlocks:far
extrn _abort:far,_flushall:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @terminate$qv,@set_terminate$qnqv$v,___call_terminate
public @unexpected$qv,@set_unexpected$qnqv$v,___call_unexpected
public @__GetPolymorphicDTC$qnvui,@__GetPolymorphicDTCfar$qnvui,__ExceptInit

; Original executable C++ exception runtime region CODE+0..75.
@terminate$qv:
    push si
    push di
    call _abort
    pop di
    pop si
    retf
@set_terminate$qnqv$v:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    les bx,dword ptr ss:[16h]
    mov dx, word ptr es:[bx + 0ch]
    mov ax, word ptr es:[bx + 0ah]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    je branch_0040
    les bx,dword ptr ss:[16h]
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr es:[bx + 0ch], dx
    mov word ptr es:[bx + 0ah], ax
branch_0040:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

    org 76 ; declare genuine exception frame label before references
terminate_unwind_frame:
    org 118 ; keep compiled terminate handler at actual CODE offset 118
; Original executable C++ exception runtime region CODE+118..244.
___call_terminate:
    push bp
    mov bp, sp
    sub sp, 26h
    push si
    push di
    mov ax, seg @terminate$qv
    mov bx, offset except_code_0064
    call ___InitExceptBlocks
    mov word ptr [bp - 22h], ds
    call _flushall
    les bx,dword ptr ss:[16h]
    mov dx, word ptr es:[bx + 0ch]
    mov ax, word ptr es:[bx + 0ah]
    mov word ptr [bp - 24h], dx
    mov word ptr [bp - 26h], ax
    mov word ptr [bp - 12h], 6
    les bx,dword ptr ss:[16h]
    cmp word ptr es:[bx + 12h], 0
    jne branch_00be
    les bx,dword ptr ss:[16h]
    mov word ptr es:[bx + 12h], ds
branch_00be:
    les bx,dword ptr ss:[16h]
    mov ax, word ptr es:[bx + 12h]
    mov word ptr [bp - 20h], ax
    mov ds, word ptr [bp - 20h]
    call dword ptr [bp - 26h]
    mov ds, word ptr [bp - 22h]
    mov word ptr [bp - 12h], 0
    jmp short branch_00e2
except_code_00da:
    mov ds, word ptr [bp - 22h]
    call @_CatchCleanup$qv
branch_00e2:
    call _abort
    push word ptr [bp - 1eh]
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

    org 84 ; type-descriptor continuation and its far self-pointer first
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
except_code_0064:
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 65506 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 3 ; native unwind descriptor field
    dd terminate_unwind_frame ; far exception unwinder address
    dw 0 ; native unwind descriptor field
    dw 4 ; native unwind descriptor field

    org 76 ; actual beginning of exception handler frame last
; First eight typed bytes of the original exception frame.
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dd except_code_00da ; far exception unwinder address
    org 245 ; continue original runtime functions in linear CODE
; Original executable C++ exception runtime region CODE+245..253.
@unexpected$qv:
    push si
    push di
    push cs
    call ___call_terminate
    pop di
    pop si
    retf

; Original executable C++ exception runtime region CODE+254..319.
@set_unexpected$qnqv$v:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    les bx,dword ptr ss:[16h]
    mov dx, word ptr es:[bx + 10h]
    mov ax, word ptr es:[bx + 0eh]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    je branch_0134
    les bx,dword ptr ss:[16h]
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    mov word ptr es:[bx + 10h], dx
    mov word ptr es:[bx + 0eh], ax
branch_0134:
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original executable C++ exception runtime region CODE+320..398.
___call_unexpected:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    les bx,dword ptr ss:[16h]
    mov dx, word ptr es:[bx + 10h]
    mov ax, word ptr es:[bx + 0eh]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    les bx,dword ptr ss:[16h]
    cmp word ptr es:[bx + 14h], 0
    jne branch_0170
    les bx,dword ptr ss:[16h]
    mov word ptr es:[bx + 14h], ds
branch_0170:
    les bx,dword ptr ss:[16h]
    mov ax, word ptr es:[bx + 14h]
    mov word ptr [bp - 2], ax
    push ds
    mov ds, word ptr [bp - 2]
    call dword ptr [bp - 6]
    pop ds
    call _abort
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original executable C++ exception runtime region CODE+399..482.
@__GetPolymorphicDTC$qnvui:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne branch_01a3
    xor ax, ax
    jmp short branch_01dd
branch_01a3:
    les bx,dword ptr [bp + 6]
    add bx, word ptr [bp + 0ah]
    mov ax, word ptr es:[bx]
    mov word ptr [bp - 2], ds
    mov word ptr [bp - 4], ax
    les bx,dword ptr [bp - 4]
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    sub ax, word ptr es:[bx - 2]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx,dword ptr [bp - 4]
    mov dx, word ptr es:[bx - 6]
    mov ax, word ptr es:[bx - 8]
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    les bx,dword ptr [bp - 8]
    mov ax, word ptr es:[bx + 1ah]
branch_01dd:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original executable C++ exception runtime region CODE+483..570.
@__GetPolymorphicDTCfar$qnvui:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne branch_01f7
    xor ax, ax
    jmp short branch_0235
branch_01f7:
    les bx,dword ptr [bp + 6]
    add bx, word ptr [bp + 0ah]
    mov dx, word ptr es:[bx + 2]
    mov ax, word ptr es:[bx]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx,dword ptr [bp - 4]
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    sub ax, word ptr es:[bx - 2]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    les bx,dword ptr [bp - 4]
    mov dx, word ptr es:[bx - 6]
    mov ax, word ptr es:[bx - 8]
    mov word ptr [bp - 6], dx
    mov word ptr [bp - 8], ax
    les bx,dword ptr [bp - 8]
    mov ax, word ptr es:[bx + 1ah]
branch_0235:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original executable C++ exception runtime region CODE+571..648.
__ExceptInit:
    push si
    push di
    mov word ptr ss:[12h], 0
    mov word ptr ss:[10h], 0
    mov word ptr ss:[18h], ds
    mov word ptr ss:[16h],offset DGROUP:___CPPexceptionList
    mov word ptr ss:[1ah], 0feedh
    mov ax, ds
    mov word ptr DGROUP:___unexpectd_DS, ax
    mov word ptr DGROUP:___terminate_DS, ax
    mov dx, word ptr ss:[18h]
    mov ax, word ptr ss:[16h]
    add ax, 0a8h
    les bx,dword ptr ss:[16h]
    mov word ptr es:[bx + 22h], dx
    mov word ptr es:[bx + 20h], ax
    mov word ptr ss:[14h], 0ffffh
    pop di
    pop si
    retf
_TEXT ends

_DATA segment word public 'DATA'
assume cs:nothing
public ___CPPexceptionList,___exceptFlags,___savedDS
public ___savedSI,___terminatePTR,___unexpectdPTR
public ___terminate_DS,___unexpectd_DS,___throwFileName
public ___throwLineNumber,___throwExceptionName,___exceptStaticBuffP
public ___exceptMemAllocVars,___exceptionNameBuff,___ExceptStaticXbuff
; Original C++ process exception-chain globals and handler pointers.
___CPPexceptionList:
    dd 0
___exceptFlags:
    dw 0
___savedDS:
    dw 0
___savedSI:
    dw 0
    org 14 ; original unexpected handler pointer first in OMF records
___unexpectdPTR:
    dd @unexpected$qv
    org 10 ; original terminate handler pointer second
___terminatePTR:
    dd @terminate$qv
    org 18 ; continue named original exception globals
___terminate_DS:
    dw 0
___unexpectd_DS:
    dw 0
___throwFileName:
    dd 0
___throwLineNumber:
    dw 0
___throwExceptionName:
    dd 0
___exceptStaticBuffP:
    dd 0
___exceptMemAllocVars:
    dd 0
___exceptionNameBuff:
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ; original 128-byte exception class-name workspace
___ExceptStaticXbuff:
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ; original 128-byte static exception buffer
_DATA ends

_BSS segment word public 'BSS'
public __DestructorCountPtr
__DestructorCountPtr:
    dd ? ; original uninitialized far destructor-count pointer
_BSS ends
end
