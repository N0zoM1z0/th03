; Bounded per-TU exception owner: 82 executable bytes and 14 control bytes.
; Included inside _TEXT by the four string/TSubString exception wrappers.
; Descending source chunks preserve the original native FIXUPP chronology;
; all CODE+0..95 is materialized exactly once, with no padding or holes.
org 79
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short xmsg_cleanup_done
xmsg_cleanup_keep_storage:
    jmp short xmsg_cleanup_done
xmsg_cleanup_null:
    xor ax,ax
xmsg_cleanup_done:
    pop di
    pop si
    pop bp
    retf

org 59
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],1
    je short xmsg_cleanup_keep_storage
    push word ptr [bp+8]
    push word ptr [bp+6]

org 32
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 13
string_exception_frame:
    dd string_exception_header
    dw -30 ; registration frame at BP-1Eh
xmsg_cleanup:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    je short xmsg_cleanup_null

org 5
string_exception_header:
    dd rtti_throw
    dw 0,0 ; original exception control fields

org 0
string_exception_unwind:
    push si
    push di
    pop di
    pop si
    retf
