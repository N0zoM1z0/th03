; Original Japanese Borland string substring comparison with original case-sensitive selection.
; Preserve both native CODE segments, control metadata, far ABI and literal fields.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strncmp:far
extrn _strnicmp:far
extrn @string@case_sensitive:word
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
include string_empty_unwind.inl
_TEXT ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@compare$xqmx6stringuiui
; Native statement chunks preserve complete original ordered FIXUPPs.

org 188
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 176
    call _strnicmp
compare_finish:
    add sp, 0ah
    push ax
    push word ptr [bp-01eh]

org 137
    call _strncmp
    jmp short compare_finish
compare_ignore_case:
    push dx
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+2]
    add ax, cx
    push word ptr es:[bx+4]
    push ax
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

org 98
    cmp word ptr DGROUP:@string@case_sensitive, 0
    je short compare_ignore_case
    push dx
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+2]
    add ax, cx
    push word ptr es:[bx+4]
    push ax
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

org 14
    call ___InitExceptBlocks
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+6]
    mov word ptr [bp-020h], ax
    mov ax, word ptr [bp+0eh]
    cmp ax, word ptr [bp-020h]
    jae short compare_use_other_length
    mov dx, ss
    lea ax, [bp+0eh]
    jmp short compare_start_ready
compare_use_other_length:
    mov dx, ss
    lea ax, [bp-020h]
compare_start_ready:
    mov bx, ax
    mov es, dx
    mov cx, word ptr es:[bx]
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+6]
    sub ax, cx
    mov word ptr [bp-022h], ax
    cmp ax, word ptr [bp+010h]
    jae short compare_use_requested_count
    mov dx, ss
    lea ax, [bp-022h]
    jmp short compare_count_ready
compare_use_requested_count:
    mov dx, ss
    lea ax, [bp+010h]
compare_count_ready:
    mov bx, ax
    mov es, dx
    mov dx, word ptr es:[bx]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@string@compare$xqmx6stringuiui proc far
    push bp
    mov bp, sp
    sub sp, 022h
    push si
    push di
@string@compare$xqmx6stringuiui endp
_TEXTC ends
end
