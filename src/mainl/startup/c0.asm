; DOS large-model startup specialized from the installed Borland C0.ASM.
; C/C++ Run Time Library 6.02; Copyright (c) 1987, 1993 Borland International.
; All Rights Reserved. Supplier-derived source; no authored-game credit.
; Preserve the 17-segment ordering, separate stack, SE priorities and ABI.
.8086
DIST equ FAR
dPtrSize equ 4
cPtrSize equ 4
MMODEL equ 0C004h
_TEXT segment byte public 'CODE'
_TEXT ends
_FARDATA segment para public 'FAR_DATA'
_FARDATA ends
_FARBSS segment para public 'FAR_BSS'
_FARBSS ends
_OVERLAY_ segment para public 'OVRINFO'
_OVERLAY_ ends
_1STUB_ segment para public 'STUBSEG'
_1STUB_ ends
_DATA segment para public 'DATA'
_DATA ends
_CONST segment word public 'CONST'
_CONST ends
_CVTSEG segment word public 'DATA'
_CVTSEG ends
_SCNSEG segment word public 'DATA'
_SCNSEG ends
_INIT_ segment word public 'INITDATA'
InitStart label byte
_INIT_ ends
_INITEND_ segment byte public 'INITDATA'
InitEnd label byte
_INITEND_ ends
_EXIT_ segment word public 'EXITDATA'
ExitStart label byte
_EXIT_ ends
_EXITEND_ segment byte public 'EXITDATA'
ExitEnd label byte
_EXITEND_ ends
_BSS segment word public 'BSS'
_BSS ends
_COMDEF_ segment word public 'BSS'
_COMDEF_ ends
_BSSEND segment byte public 'BSS'
_BSSEND ends
_STACK segment stack 'STACK'
_STACK ends
DGROUP group _DATA,_CONST,_CVTSEG,_SCNSEG,_INIT_,_INITEND_,_EXIT_,_EXITEND_,_BSS,_COMDEF_,_BSSEND

locals
ASSUME  CS:_TEXT, DS:DGROUP
extrn       _main:DIST
extrn       _exit:DIST
extrn       __exit:DIST
extrn       __abort:DIST
extrn       ___ErrorMessage:DIST
extrn       __nfile:word
extrn       __stklen:word
extrn       __ExceptInit:DIST
PSPHigh         equ     00002h
PSPEnv          equ     0002ch
PSPCmd          equ     00080h
public  __AHINCR
public  __AHSHIFT
__AHINCR        equ     1000h
__AHSHIFT       equ     12
MINSTACK        equ     256
_TEXT           SEGMENT

; Entry DS/ES are the PSP. Cache DGROUP before using the runtime globals.
STARTX          PROC    NEAR
    mov     dx, DGROUP
    mov     cs:DGROUP@@, dx
    mov     ah, 30h
    int     21h
    mov     bp, ds:[PSPHigh]
    mov     bx, ds:[PSPEnv]
    mov     ds, dx
    mov     _version@, ax
    mov     _psp@, es
    mov     _envseg@, bx
    mov     word ptr _heaptop@ + 2, bp
    call    SaveVectors
    mov     ax, _envseg@
    mov     es, ax
    xor     ax, ax
    mov     bx, ax
    mov     di, ax
    mov     cx, 07FFFh
    cld
@@EnvLoop:
    repnz   scasb
    jcxz    InitFailed
    inc     bx
    cmp     es:[di], al
    jne     @@EnvLoop
    or      ch, 10000000b
    neg     cx
    mov     _envLng@, cx
    mov     cx, dPtrSize / 2
    shl     bx, cl
    add     bx, dPtrSize * 4
    and     bx, not ((dPtrSize * 4) - 1)
    mov     _envSize@, bx
    mov     dx, ss
    sub     bp, dx
    mov     di, seg __stklen
    mov     es, di
    mov     di, es:__stklen
    cmp     di, 2*MINSTACK
    jae     AskedStackOK
    mov     di, 2*MINSTACK
    mov     es:__stklen, di

; Keep at least 512 stack bytes; return excess paragraphs before changing SS:SP.
AskedStackOK    label   near
    mov     cl, 4
    shr     di, cl
    inc     di
    cmp     bp, di
    jnb     ExcessOfMemory
InitFailed      label   near
    call    __abort

; Preserve the original DOS resize call and interrupt-protected stack switch.
ExcessOfMemory  label   near
    mov     bx, di
    add     bx, dx
    mov     word ptr _heapbase@ + 2, bx
    mov     word ptr _brklvl@ + 2, bx
    mov     ax, _psp@
    sub     bx, ax
    mov     es, ax
    mov     ah, 04Ah
    push    di
    int     021h
    pop     di
    shl     di, cl
    cli
    mov     ss, dx
    mov     sp, di
    sti
    mov     ax, seg __stklen
    mov     es, ax
    mov     es:__stklen, di
    xor     ax, ax
    mov     es, cs:DGROUP@@
    mov     di, offset DGROUP: bdata@
    mov     cx, offset DGROUP: edata@
    sub     cx, di
    cld
    rep     stosb
    cmp     __nfile, 20
    jbe     @@NoChange
    cmp     _osmajor@, 3
    jb      @@NoChange
    ja      @@DoChange
    cmp     _osminor@, 1Eh
    jb      @@NoChange
@@DoChange:
    mov     ax, 5801h
    mov     bx, 2
    int     21h
    jc      @@BadInit
    mov     ah, 67h
    mov     bx, __nfile
    int     21h
    jc      @@BadInit
    mov     ah, 48h
    mov     bx, 1
    int     21h
    jc      @@BadInit
    inc     ax
    mov     word ptr _heaptop@ + 2, ax
    dec     ax
    mov     es, ax
    mov     ah, 49h
    int     21h
    jc      @@BadInit
    mov     ax, 5801h
    mov     bx, 0
    int     21h
    jnc     @@NoChange
@@BadInit:      call    __abort
@@NoChange:
    xor     bp,bp
    push    bp
    call    __ExceptInit
    pop     ax
    mov     es, cs:DGROUP@@
    mov     si,offset DGROUP:InitStart
    mov     di,offset DGROUP:InitEnd
    call    Initialize
    push    word ptr __C0environ+2
    push    word ptr __C0environ
    push    word ptr __C0argv+2
    push    word ptr __C0argv
    push    __C0argc
    call    _main
    push    ax
    call    _exit
__cleanup       PROC    DIST
PUBLIC  __cleanup
    mov     es, cs:DGROUP@@
    push    si
    push    di
    mov     si,offset DGROUP:ExitStart
    mov     di,offset DGROUP:ExitEnd
    call    Cleanup
    pop     di
    pop     si
    ret
__cleanup       ENDP
__checknull     PROC    DIST
PUBLIC  __checknull
    ret
__checknull     ENDP
__terminate     PROC    DIST
PUBLIC  __terminate
    mov     bp,sp
    mov     ah,4Ch
    mov     al,[bp+cPtrSize]
    int     21h
__terminate     ENDP
STARTX          ENDP

; The default INT 0 handler reports the error and exits with status 3.
ZeroDivision    PROC    FAR
    mov     dx, offset DGROUP:ZeroDivMSG
    push ds
    push    dx
    call    ___ErrorMessage
    pop     dx
    pop ds
    mov     ax, 3
    push    ax
    call    __exit

; The default INT 0 handler reports the error and exits with status 3.
ZeroDivision    ENDP

; Save INT 0/4/5/6 before installing the default divide handler.
SaveVectors     PROC    NEAR
    push    ds
    mov     ax, 3500h
    int     021h
    mov     word ptr _Int0Vector@, bx
    mov     word ptr _Int0Vector@+2, es
    mov     ax, 3504h
    int     021h
    mov     word ptr _Int4Vector@, bx
    mov     word ptr _Int4Vector@+2, es
    mov     ax, 3505h
    int     021h
    mov     word ptr _Int5Vector@, bx
    mov     word ptr _Int5Vector@+2, es
    mov     ax, 3506h
    int     021h
    mov     word ptr _Int6Vector@, bx
    mov     word ptr _Int6Vector@+2, es
    mov     ax, 2500h
    mov     dx, cs
    mov     ds, dx
    mov     dx, offset ZeroDivision
    int     21h
    pop     ds
    ret

; Save INT 0/4/5/6 before installing the default divide handler.
SaveVectors     ENDP

; Restore the four saved vectors while preserving the caller data segment.
__restorezero   PROC    DIST
PUBLIC  __restorezero
    push    ds
    mov     ax, 2500h
    lds     dx, _Int0Vector@
    int     21h
    pop     ds
    push    ds
    mov     ax, 2504h
    lds     dx, _Int4Vector@
    int     21h
    pop     ds
    push    ds
    mov     ax, 2505h
    lds     dx, _Int5Vector@
    int     21h
    pop     ds
    push    ds
    mov     ax, 2506h
    lds     dx, _Int6Vector@
    int     21h
    pop     ds
    ret
ENDP
PNEAR           EQU     0
PFAR            EQU     1
NOTUSED         EQU     0ffh
SE              STRUC
calltype        db      ?
priority        db      ?
addrlow         dw      ?
addrhigh        dw      ?
SE              ENDS

; Ascending priority; equal priorities retain the first table entry.
Initialize      proc near
@@Start:        mov     ax,100h
    mov     dx,di
    mov     bx,si
@@TopOfTable:   cmp     bx,di
    je      @@EndOfTable
    cmp     es:[bx.calltype],NOTUSED
    je      @@Next
    mov     cl, es:[bx.priority]
    xor     ch, ch
    cmp     cx,ax
    jae     @@Next
    mov     ax,cx
    mov     dx,bx
@@Next:         add     bx,SIZE SE
    jmp     @@TopOfTable
@@EndOfTable:   cmp     dx,di
    je      @@Done
    mov     bx,dx
    cmp     es:[bx.calltype],PNEAR
    mov     es:[bx.calltype],NOTUSED
    push    es
    je      @@NearCall
@@FarCall:      call    DWORD PTR es:[bx.addrlow]
    pop     es
    jmp     short @@Start
@@NearCall:     call    WORD PTR es:[bx.addrlow]
    pop     es
    jmp     short @@Start
@@Done:         ret
endp

; Descending priority; equal priorities select the last table entry.
Cleanup         proc near
@@Start:        mov     ah,0
    mov     dx,di
    mov     bx,si
@@TopOfTable:   cmp     bx,di
    je      @@EndOfTable
    cmp     es:[bx.calltype],NOTUSED
    je      @@Next
    cmp     es:[bx.priority],ah
    jb      @@Next
    mov     ah,es:[bx.priority]
    mov     dx,bx
@@Next:         add     bx,SIZE SE
    jmp     @@TopOfTable
@@EndOfTable:   cmp     dx,di
    je      @@Done
    mov     bx,dx
    cmp     es:[bx.calltype],PNEAR
    mov     es:[bx.calltype],NOTUSED
    push    es
    je      @@NearCall
@@FarCall:      call    DWORD PTR es:[bx.addrlow]
    pop     es
    jmp     short @@Start
@@NearCall:     call    WORD PTR es:[bx.addrlow]
    pop     es
    jmp     short @@Start
@@Done:         ret
endp
public DGROUP@

; Written by the entry code: this two-byte CODE cache is genuinely uninitialized.
DGROUP@ dw    ?
DGROUP@@ equ DGROUP@
public __MMODEL
__MMODEL        dw      MMODEL
_TEXT           ENDS

; Runtime DATA layout includes the null-check header, vector saves and heap bounds.
_DATA           SEGMENT
public DATASEG@
DATASEG@        label   byte
NULL            db       4 dup(0)
CheckStr        db      'NULL CHECK'
db       2 dup (0)
db       4 dup (0)
db       2 dup (0)
db       4 dup (0)
db       6 dup (0)
CopyRight       db      'Borland C++ - Copyright 1993 Borland Intl.',0
ZeroDivMSG      db      'Divide error', 13, 10, 0
public __Int0Vector
__Int0Vector dd     0
_Int0Vector@ equ __Int0Vector
public __Int4Vector
__Int4Vector dd     0
_Int4Vector@ equ __Int4Vector
public __Int5Vector
__Int5Vector dd     0
_Int5Vector@ equ __Int5Vector
public __Int6Vector
__Int6Vector dd     0
_Int6Vector@ equ __Int6Vector
public __C0argc
__C0argc dw     0
_C0argc@ equ __C0argc
public __C0argv
__C0argv dd 0
_C0argv@ equ __C0argv
public __C0environ
__C0environ dd 0
_C0environ@ equ __C0environ
public __envLng
__envLng dw     0
_envLng@ equ __envLng
public __envseg
__envseg dw     0
_envseg@ equ __envseg
public __envSize
__envSize dw     0
_envSize@ equ __envSize
public __psp
__psp dw     0
_psp@ equ __psp
public __version
__version label word
_version@ equ __version
public __osversion
__osversion label word
_osversion@ equ __osversion
public __osmajor
__osmajor db     0
_osmajor@ equ __osmajor
public __osminor
__osminor db     0
_osminor@ equ __osminor
public _errno
_errno dw     0
errno@ equ _errno
public __Exception_list
__Exception_list dw    -1
_Exception_list@ equ __Exception_list
public ___brklvl
___brklvl dw   DGROUP:edata@
__brklvl@ equ ___brklvl
public __heapbase
__heapbase dd   0
_heapbase@ equ __heapbase
public __brklvl
__brklvl dd   0
_brklvl@ equ __brklvl
public __heaptop
__heaptop dd   0
_heaptop@ equ __heaptop
_DATA           ENDS
_CVTSEG         SEGMENT
public __RealCvtVector
__RealCvtVector label  word
_RealCvtVector@ equ __RealCvtVector
ENDS
_SCNSEG         SEGMENT
public __ScanTodVector
__ScanTodVector label word
_ScanTodVector@ equ __ScanTodVector
ENDS
_BSS            SEGMENT
bdata@          label   byte
ENDS
_BSSEND         SEGMENT
edata@          label   byte
ENDS
_STACK          SEGMENT
db      128 dup(?)
ENDS
END     STARTX
