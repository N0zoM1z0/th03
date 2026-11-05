; Original Borland locale-aware strcoll with per-level weight comparisons.
; __strcoll establishes locale state, calls the shared _LevelCollate
; state machine and sign-extends its collation result. Character-weight
; iteration, deferred strength differences and expansion ordering are
; retained with the original short and near control-flow boundaries.
.8086
extrn _GetNextKeyWeight:near
extrn _GetSubstituteString:near
extrn _GetCompressLevelWeight:near
extrn _GetNextAuxChar:near
extrn _GetExpansionString:near
extrn _GetNextExpansionWeight:near
extrn __pLocale:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_STRCOLL_TEXT segment word public 'CODE'
_STRCOLL_TEXT ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __strcoll
public _LevelCollate
__strcoll proc far
    push bp
    mov bp,sp
    sub sp,24h
    push ds
    push es
    push di
    push si
    lds bx,dword ptr __pLocale
    mov [bp-24h],bx
    mov [bp-22h],ds
    mov ax,[bx+184h]
    mov [bp-1eh],ax
    lds si,dword ptr [bx+190h]
    inc si
    mov [bp-18h],si
    mov [bp-16h],ds
    mov word ptr [bp-1ah],0
    mov word ptr [bp-1ch],0
    lds si,dword ptr [bp+6]
    les di,dword ptr [bp+0ah]
    call _LevelCollate
    cbw
    pop si
    pop di
    pop es
    pop ds
    mov sp,bp
    pop bp
    retf
__strcoll endp

_LevelCollate proc near
next_collation_level:
    mov word ptr [bp-12h],0
    mov word ptr [bp-14h],0
    mov word ptr [bp-8],0
    mov word ptr [bp-10h],0
    push ds
    lds bx,dword ptr [bp-24h]
    mov cx,[bp-1ah]
    add bx,cx
    mov al,[bx+186h]
    add word ptr [bp-1ch],101h
    mov ch,al
    pop ds
    xor dx,dx
next_weight:
    lea bx,[bp-8]
    call _GetNextKeyWeight
    mov cl,al
    xchg dl,dh
    lea bx,[bp-10h]
    push ds
    push si
    push es
    push di
    pop si
    pop ds
    call _GetNextKeyWeight
    push ds
    push si
    pop di
    pop es
    pop si
    pop ds
    mov ah,cl
    xchg dl,dh
    test dx,8080h
    jnz short weight_termination
    test ch,10h
    jnz short compare_secondary_weights
    sub ah,al
    jz short next_weight
    xor al,al
    xchg al,ah
    test ch,2
    jnz short record_weight
    ret
record_secondary:
    mov [bp-14h],bx
record_weight:
    mov [bp-12h],ax
    jmp short next_weight

compare_secondary_weights:
    push ax
    mov bx,[bp-8]
    mov ax,[bp-10h]
    sub bx,ax
    jz short secondary_weights_equal
    pop ax
    test ch,2
    jnz short record_secondary
    mov ax,bx
    ret
secondary_weights_equal:
    pop ax
    sub ah,al
    xor al,al
    xchg al,ah
    test al,al
    jz short next_weight
    test ch,2
    jnz short record_secondary
    ret

weight_termination:
    test ax,ax
    jz short choose_deferred_comparison
    mov ax,7f7fh
    test dh,80h
    jnz short done_level
    neg ax
done_level:
    ret
choose_deferred_comparison:
    mov ax,[bp-14h]
    test ax,ax
    jz short choose_saved_weight
    ret
choose_saved_weight:
    mov ax,[bp-12h]
    test ax,ax
    jz short advance_level
    ret
advance_level:
    inc word ptr [bp-1ah]
    mov cx,[bp-1eh]
    cmp word ptr [bp-1ah],cx
    jl short restart_from_origins
    xor ax,ax
    ret
restart_from_origins:
    lds si,dword ptr [bp+6]
    les di,dword ptr [bp+0ah]
    jmp near ptr next_collation_level
_LevelCollate endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_STRCOLL_TEXT segment word public 'CODE'
_STRCOLL_TEXT ends
end
