; Original Japanese Borland TSubString text equality with original empty-text constant.
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
_DATA segment word public 'DATA'
empty_text db 0 ; the original one-byte empty string literal
_DATA ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @TSubString@$beql$xqnxc
; Native statement chunks preserve complete original ordered FIXUPPs.

org 169
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 152
    call _strnicmp
substring_compare_finish:
    add sp, 0ah
    neg ax
    sbb ax, ax
    inc ax
substring_result_ready:
    push ax
    push word ptr [bp-01eh]

org 106
    call _strncmp
    jmp short substring_compare_finish
substring_ignore_case:
    les bx, dword ptr [bp+6]
    push word ptr es:[bx+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+2]
    push bx
    push es
    les bx, dword ptr [bp+6]
    add ax, word ptr es:[bx+4]
    pop es
    pop bx
    push word ptr es:[bx+4]
    push ax

org 60
substring_compare:
    cmp word ptr DGROUP:@string@case_sensitive, 0
    je short substring_ignore_case
    les bx, dword ptr [bp+6]
    push word ptr es:[bx+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+2]
    push bx
    push es
    les bx, dword ptr [bp+6]
    add ax, word ptr es:[bx+4]
    pop es
    pop bx
    push word ptr es:[bx+4]
    push ax

org 30
    mov word ptr [bp+0ah],offset DGROUP:empty_text
substring_input_ready:
    les bx, dword ptr [bp+6]
    cmp word ptr es:[bx+4], -1
    jne short substring_valid
    mov ax, 1
    jmp short substring_validity_ready
substring_valid:
    xor ax, ax
substring_validity_ready:
    or ax, ax
    je short substring_compare
    xor ax, ax
    jmp short substring_result_ready

org 14
    call ___InitExceptBlocks
    mov ax, word ptr [bp+0ah]
    or ax, word ptr [bp+0ch]
    jne short substring_input_ready
    mov word ptr [bp+0ch], ds

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@TSubString@$beql$xqnxc proc far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
@TSubString@$beql$xqnxc endp
_TEXTC ends
end
