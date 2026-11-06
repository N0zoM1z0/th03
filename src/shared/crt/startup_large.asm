; Shared large-model startup: supplier-derived code with original ordered fields.
; C/C++ Run Time Library 6.02; Copyright (c) 1987, 1993 Borland International.
; All Rights Reserved. Supplier-derived source; no authored-game credit.
; Preserve the 17-segment ordering, separate stack, SE priorities and ABI.
.8086
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

ASSUME  CS:_TEXT, DS:DGROUP
extrn       _main:far
extrn       _exit:far
extrn       __exit:far
extrn       __abort:far
extrn       ___ErrorMessage:far
extrn       __nfile:word
extrn       __stklen:word
extrn       __ExceptInit:far
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
PUBLIC  __cleanup
PUBLIC  __checknull
PUBLIC  __terminate
PUBLIC  __restorezero
PNEAR           EQU     0
PFAR            EQU     1
NOTUSED         EQU     0ffh
SE              STRUC
calltype        db      ?
priority        db      ?
addrlow         dw      ?
addrhigh        dw      ?
SE              ENDS
public DGROUP@
DGROUP@@ equ DGROUP@
public __MMODEL
; Real code labels are bound before ordinary native instruction spans.
; Preserve original CODE621/622 cache holes and the separately reserved STACK.
org 0
STARTX label near
org 55
STARTX_EnvLoop label near
org 117
AskedStackOK label near
org 126
InitFailed label near
org 131
ExcessOfMemory label near
org 215
STARTX_DoChange label near
org 267
STARTX_BadInit label near
org 272
STARTX_NoChange label near
org 326
__cleanup label far
org 345
__checknull label far
org 346
__terminate label far
org 355
ZeroDivision label far
org 376
SaveVectors label near
org 443
__restorezero label far
org 488
Initialize label near
org 488
Initialize_Start label near
org 495
Initialize_TopOfTable label near
org 519
Initialize_Next label near
org 524
Initialize_EndOfTable label near
org 541
Initialize_FarCall label near
org 548
Initialize_NearCall label near
org 555
Initialize_Done label near
org 556
Cleanup label near
org 556
Cleanup_Start label near
org 562
Cleanup_TopOfTable label near
org 584
Cleanup_Next label near
org 589
Cleanup_EndOfTable label near
org 606
Cleanup_FarCall label near
org 613
Cleanup_NearCall label near
org 620
Cleanup_Done label near
org 621
DGROUP@ label word
org 623
__MMODEL label word

; Original CODE 3..21.
org 3
    mov     cs:DGROUP@@, dx
    mov     ah, 30h
    int     21h
    mov     bp, ds:[PSPHigh]
    mov     bx, ds:[PSPEnv]
    mov     ds, dx

; Original CODE 22..24.
org 22
    mov     _version@, ax

; Original CODE 25..28.
org 25
    mov     _psp@, es

; Original CODE 29..32.
org 29
    mov     _envseg@, bx

; Original CODE 33..39.
org 33
    mov     word ptr _heaptop@ + 2, bp
    call    SaveVectors

; Original CODE 40..69.
org 40
    mov     ax, _envseg@
    mov     es, ax
    xor     ax, ax
    mov     bx, ax
    mov     di, ax
    mov     cx, 07FFFh
    cld
    repnz   scasb
    jcxz    InitFailed
    inc     bx
    cmp     es:[di], al
    jne     STARTX_EnvLoop
    or      ch, 10000000b
    neg     cx

; Original CODE 70..84.
org 70
    mov     _envLng@, cx
    mov     cx, dPtrSize / 2
    shl     bx, cl
    add     bx, dPtrSize * 4
    and     bx, not ((dPtrSize * 4) - 1)

; Original CODE 85..92.
org 85
    mov     _envSize@, bx
    mov     dx, ss
    sub     bp, dx

; Original CODE 135..138.
org 135
    mov     word ptr _heapbase@ + 2, bx

; Original CODE 139..142.
org 139
    mov     word ptr _brklvl@ + 2, bx

; Original CODE 143..163.
org 143
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

; Original CODE 176..180.
org 176
    mov     es, cs:DGROUP@@

; Original CODE 181..183.
org 181
    mov     di, offset DGROUP: bdata@

; Original CODE 184..191.
org 184
    mov     cx, offset DGROUP: edata@
    sub     cx, di
    cld
    rep     stosb

; Original CODE 199..207.
org 199
    cmp     _osmajor@, 3
    jb      STARTX_NoChange
    ja      STARTX_DoChange

; Original CODE 208..226.
org 208
    cmp     _osminor@, 1Eh
    jb      STARTX_NoChange
    mov     ax, 5801h
    mov     bx, 2
    int     21h
    jc      STARTX_BadInit
    mov     ah, 67h

; Original CODE 245..266.
org 245
    mov     word ptr _heaptop@ + 2, ax
    dec     ax
    mov     es, ax
    mov     ah, 49h
    int     21h
    jc      STARTX_BadInit
    mov     ax, 5801h
    mov     bx, 0
    int     21h
    jnc     STARTX_NoChange

; Original CODE 281..285.
org 281
    mov     es, cs:DGROUP@@

; Original CODE 295..298.
org 295
    push    word ptr __C0environ+2

; Original CODE 299..302.
org 299
    push    word ptr __C0environ

; Original CODE 303..306.
org 303
    push    word ptr __C0argv+2

; Original CODE 307..310.
org 307
    push    word ptr __C0argv

; Original CODE 0..2.
org 0
    mov     dx, DGROUP

; Original CODE 93..97.
org 93
    mov     di, seg __stklen
    mov     es, di

; Original CODE 98..111.
org 98
    mov     di, es:__stklen
    cmp     di, 2*MINSTACK
    jae     AskedStackOK
    mov     di, 2*MINSTACK

; Original CODE 112..125.
org 112
    mov     es:__stklen, di
    mov     cl, 4
    shr     di, cl
    inc     di
    cmp     bp, di
    jnb     ExcessOfMemory

; Original CODE 126..134.
org 126
    call    __abort
    mov     bx, di
    add     bx, dx

; Original CODE 164..168.
org 164
    mov     ax, seg __stklen
    mov     es, ax

; Original CODE 169..175.
org 169
    mov     es:__stklen, di
    xor     ax, ax

; Original CODE 192..198.
org 192
    cmp     __nfile, 20
    jbe     STARTX_NoChange

; Original CODE 227..244.
org 227
    mov     bx, __nfile
    int     21h
    jc      STARTX_BadInit
    mov     ah, 48h
    mov     bx, 1
    int     21h
    jc      STARTX_BadInit
    inc     ax

; Original CODE 267..274.
org 267
    call    __abort
    xor     bp,bp
    push    bp

; Original CODE 275..280.
org 275
    call    __ExceptInit
    pop     ax

; Original CODE 286..288.
org 286
    mov     si,offset DGROUP:InitStart

; Original CODE 289..294.
org 289
    mov     di,offset DGROUP:InitEnd
    call    Initialize

; Original CODE 315..320.
org 315
    call    _main
    push    ax

; Original CODE 321..325.
org 321
    call    _exit

; Original CODE 333..335.
org 333
    mov     si,offset DGROUP:ExitStart

; Original CODE 336..354.
org 336
    mov     di,offset DGROUP:ExitEnd
    call    Cleanup
    pop     di
    pop     si
    retf
    retf
    mov     bp,sp
    mov     ah,4Ch
    mov     al,[bp+cPtrSize]
    int     21h

; Original CODE 360..370.
org 360
    call    ___ErrorMessage
    pop     dx
    pop ds
    mov     ax, 3
    push    ax

; Original CODE 371..381.
org 371
    call    __exit
    push    ds
    mov     ax, 3500h
    int     021h

; Original CODE 436..446.
org 436
    mov     dx, offset ZeroDivision
    int     21h
    pop     ds
    ret
    push    ds
    mov     ax, 2500h

; Original CODE 311..314.
org 311
    push    __C0argc

; Original CODE 326..332.
org 326
    mov     es, cs:DGROUP@@
    push    si
    push    di

; Original CODE 355..359.
org 355
    mov     dx, offset DGROUP:ZeroDivMSG
    push ds
    push    dx

; Original CODE 382..385.
org 382
    mov     word ptr _Int0Vector@, bx

; Original CODE 386..394.
org 386
    mov     word ptr _Int0Vector@+2, es
    mov     ax, 3504h
    int     021h

; Original CODE 395..398.
org 395
    mov     word ptr _Int4Vector@, bx

; Original CODE 399..407.
org 399
    mov     word ptr _Int4Vector@+2, es
    mov     ax, 3505h
    int     021h

; Original CODE 408..411.
org 408
    mov     word ptr _Int5Vector@, bx

; Original CODE 412..420.
org 412
    mov     word ptr _Int5Vector@+2, es
    mov     ax, 3506h
    int     021h

; Original CODE 421..424.
org 421
    mov     word ptr _Int6Vector@, bx

; Original CODE 425..435.
org 425
    mov     word ptr _Int6Vector@+2, es
    mov     ax, 2500h
    mov     dx, cs
    mov     ds, dx

; Original CODE 447..457.
org 447
    lds     dx, _Int0Vector@
    int     21h
    pop     ds
    push    ds
    mov     ax, 2504h

; Original CODE 458..468.
org 458
    lds     dx, _Int4Vector@
    int     21h
    pop     ds
    push    ds
    mov     ax, 2505h

; Original CODE 469..479.
org 469
    lds     dx, _Int5Vector@
    int     21h
    pop     ds
    push    ds
    mov     ax, 2506h

; Original CODE 480..624.
org 480
    lds     dx, _Int6Vector@
    int     21h
    pop     ds
    retf
    mov     ax,100h
    mov     dx,di
    mov     bx,si
    cmp     bx,di
    je      Initialize_EndOfTable
    cmp     byte ptr es:[bx.calltype],NOTUSED
    je      Initialize_Next
    mov     cl, es:[bx.priority]
    xor     ch, ch
    cmp     cx,ax
    jae     Initialize_Next
    mov     ax,cx
    mov     dx,bx
    add     bx,SIZE SE
    jmp     Initialize_TopOfTable
    cmp     dx,di
    je      Initialize_Done
    mov     bx,dx
    cmp     byte ptr es:[bx.calltype],PNEAR
    mov     byte ptr es:[bx.calltype],NOTUSED
    push    es
    je      Initialize_NearCall
    call    DWORD PTR es:[bx.addrlow]
    pop     es
    jmp     short Initialize_Start
    call    WORD PTR es:[bx.addrlow]
    pop     es
    jmp     short Initialize_Start
    ret
    mov     ah,0
    mov     dx,di
    mov     bx,si
    cmp     bx,di
    je      Cleanup_EndOfTable
    cmp     byte ptr es:[bx.calltype],NOTUSED
    je      Cleanup_Next
    cmp     byte ptr es:[bx.priority],ah
    jb      Cleanup_Next
    mov     ah,es:[bx.priority]
    mov     dx,bx
    add     bx,SIZE SE
    jmp     Cleanup_TopOfTable
    cmp     dx,di
    je      Cleanup_Done
    mov     bx,dx
    cmp     byte ptr es:[bx.calltype],PNEAR
    mov     byte ptr es:[bx.calltype],NOTUSED
    push    es
    je      Cleanup_NearCall
    call    DWORD PTR es:[bx.addrlow]
    pop     es
    jmp     short Cleanup_Start
    call    WORD PTR es:[bx.addrlow]
    pop     es
    jmp     short Cleanup_Start
    ret
    dw ?
    dw MMODEL
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
_CVTSEG ends
_SCNSEG         SEGMENT
public __ScanTodVector
__ScanTodVector label word
_ScanTodVector@ equ __ScanTodVector
_SCNSEG ends
_BSS            SEGMENT
bdata@          label   byte
_BSS ends
_BSSEND         SEGMENT
edata@          label   byte
_BSSEND ends
_STACK          SEGMENT
db      128 dup(?)
_STACK ends
END     STARTX
