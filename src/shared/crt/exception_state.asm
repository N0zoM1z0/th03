; Shared C++ runtime: complete original storage, ABI and literal ordered fields.
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
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Original executable C++ exception runtime region CODE+0..75.
public @__GetPolymorphicDTC$qnvui,@__GetPolymorphicDTCfar$qnvui,@unexpected$qv,@terminate$qv,@set_unexpected$qnqv$v,@set_terminate$qnqv$v,___call_terminate,___call_unexpected
_TEXT ends
_BSS segment word public 'BSS'
public __DestructorCountPtr
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
; Prebind real instruction, frame and RTTI labels before ordinary span emission.
; Every initialized byte is emitted once; metadata pointers remain symbolic.
org 0
@terminate$qv label near
org 10
@set_terminate$qnqv$v label near
org 64
branch_0040 label near
org 76
terminate_unwind_frame label near
org 118
___call_terminate label near
org 190
branch_00be label near
org 218
except_code_00da label near
org 226
branch_00e2 label near
org 100
except_code_0064 label near
org 245
@unexpected$qv label near
org 254
@set_unexpected$qnqv$v label near
org 308
branch_0134 label near
org 320
___call_unexpected label near
org 368
branch_0170 label near
org 399
@__GetPolymorphicDTC$qnvui label near
org 419
branch_01a3 label near
org 477
branch_01dd label near
org 483
@__GetPolymorphicDTCfar$qnvui label near
org 503
branch_01f7 label near
org 565
branch_0235 label near
org 571
__ExceptInit label near

; Original CODE 611..648.
org 611
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

; Original CODE 608..610.
org 608
    mov word ptr DGROUP:___unexpectd_DS, ax

; Original CODE 592..607.
org 592
    mov word ptr ss:[16h],offset DGROUP:___CPPexceptionList
    mov word ptr ss:[1ah], 0feedh
    mov ax, ds

; Original CODE 388..591.
org 388
    call _abort
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
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
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
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
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
    push si
    push di
    mov word ptr ss:[12h], 0
    mov word ptr ss:[10h], 0
    mov word ptr ss:[18h], ds

; Original CODE 234..387.
org 234
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
    push si
    push di
    push cs
    call ___call_terminate
    pop di
    pop si
    retf
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
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
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
    les bx,dword ptr ss:[16h]
    mov ax, word ptr es:[bx + 14h]
    mov word ptr [bp - 2], ax
    push ds
    mov ds, word ptr [bp - 2]
    call dword ptr [bp - 6]
    pop ds

; Original CODE 226..233.
org 226
    call _abort
    push word ptr [bp - 1eh]

; Original CODE 221..225.
org 221
    call @_CatchCleanup$qv

; Original CODE 140..220.
org 140
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
    les bx,dword ptr ss:[16h]
    mov ax, word ptr es:[bx + 12h]
    mov word ptr [bp - 20h], ax
    mov ds, word ptr [bp - 20h]
    call dword ptr [bp - 26h]
    mov ds, word ptr [bp - 22h]
    mov word ptr [bp - 12h], 0
    jmp short branch_00e2
    mov ds, word ptr [bp - 22h]

; Original CODE 132..139.
org 132
    call ___InitExceptBlocks
    mov word ptr [bp - 22h], ds

; Original CODE 129..131.
org 129
    mov bx, offset except_code_0064

; Original CODE 126..128.
org 126
    mov ax, seg @terminate$qv

; Original CODE 110..125.
org 110
    dd terminate_unwind_frame ; far exception unwinder address
    dw 0 ; native unwind descriptor field
    dw 4 ; native unwind descriptor field
    push bp
    mov bp, sp
    sub sp, 26h
    push si
    push di

; Original CODE 80..109.
org 80
    dd except_code_00da ; far exception unwinder address
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 65506 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field
    dw 3 ; native unwind descriptor field

; Original CODE 2..79.
org 2
    call _abort
    pop di
    pop si
    retf
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
    mov dx, word ptr [bp - 2]
    mov ax, word ptr [bp - 4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
    dw 0 ; native unwind descriptor field
    dw 0 ; native unwind descriptor field

; Original CODE 0..1.
org 0
    push si
    push di
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
__DestructorCountPtr:
    dd ? ; original uninitialized far destructor-count pointer
_BSS ends
_TEXT segment byte public 'CODE'
public __ExceptInit
_TEXT ends
end
