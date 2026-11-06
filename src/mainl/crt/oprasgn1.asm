; Original Japanese Borland TSubString string assignment with original clone and splice.
; Preserve both native CODE segments, control metadata, far ABI and literal fields.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @string@clone$qv:far
extrn @TStringRef@splice$quiuinxcui:far
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
public @TSubString@$basg$qmx6string
; Native statement chunks preserve complete original ordered FIXUPPs.

org 164
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 145
    call @TStringRef@splice$quiuinxcui
    add sp, 0eh
substring_assignment_done:
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    push dx
    push ax
    push word ptr [bp-01eh]

org 51
    call @string@clone$qv
    pop cx
    pop cx
    jmp short substring_storage_ready
substring_storage_ready:
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    mov dx, es
    mov cx, bx
    push word ptr es:[bx+6]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    mov ax, word ptr es:[bx+6]
    les bx, dword ptr [bp+6]
    sub ax, word ptr es:[bx+4]
    mov word ptr [bp-020h], ax
    mov ax, word ptr es:[bx+6]
    cmp ax, word ptr [bp-020h]
    jae short substring_use_available
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    add ax, 6
    jmp short substring_count_ready
substring_use_available:
    mov dx, ss
    lea ax, [bp-020h]
substring_count_ready:
    mov bx, ax
    mov es, dx
    push word ptr es:[bx]
    les bx, dword ptr [bp+6]
    push word ptr es:[bx+4]
    les bx, dword ptr es:[bx]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 14
    call ___InitExceptBlocks
    les bx, dword ptr [bp+6]
    cmp word ptr es:[bx+4], -1
    je short substring_assignment_done
    les bx, dword ptr es:[bx]
    les bx, dword ptr es:[bx]
    cmp word ptr es:[bx], 1
    jbe short substring_storage_ready
    les bx, dword ptr [bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@TSubString@$basg$qmx6string proc far
    push bp
    mov bp, sp
    sub sp, 020h
    push si
    push di
@TSubString@$basg$qmx6string endp
_TEXTC ends
end
