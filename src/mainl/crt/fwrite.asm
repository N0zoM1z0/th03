; Original DOS Borland far-cdecl fwrite: write complete counted records.
; Multiplies requested sizes using real near N_LXMUL@, writes with actual
; near __FPUTN and advances segment-aware destination via N_PADD@.
; Short total performs one buffered chunk; large total writes records
; in a loop. Retain original 16-bit carry/overflow and partial-count ABI.
; No target CODE arrays, binary patches or artificial padding.
.8086
extrn __FPUTN:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
extrn N_LXMUL@:near
extrn N_PADD@:near
public _fwrite
_fwrite proc far
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    cmp word ptr [bp+0ah], 0
    jne short compute_write_bytes
    jmp near ptr return_original_count
compute_write_bytes:
    mov bx, word ptr [bp+0ah]
    xor cx, cx
    mov ax, word ptr [bp+0ch]
    xor dx, dx
    call N_LXMUL@
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
    cmp dx, 1
    ja short write_large_total
    jb short write_short_block
    or ax, ax
    jae short write_large_total
write_short_block:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-6]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    call __FPUTN
    xor dx, dx
    div word ptr [bp+0ah]
    jmp short return_records_written
write_large_total:
    mov word ptr [bp-2], 0
    jmp short loop_record_write
write_next_record:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ah]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    call __FPUTN
    xor dx, dx
    or dx, dx
    jne short partial_write_exit
    cmp ax, word ptr [bp+0ah]
    je short advance_far_write_pointer
partial_write_exit:
    mov ax, word ptr [bp-2]
    jmp short return_records_written
advance_far_write_pointer:
    mov bx, word ptr [bp+0ah]
    xor cx, cx
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    call N_PADD@
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
    inc word ptr [bp-2]
loop_record_write:
    mov ax, word ptr [bp-2]
    cmp ax, word ptr [bp+0ch]
    jb short write_next_record
return_original_count:
    mov ax, word ptr [bp+0ch]
return_records_written:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_fwrite endp
_TEXT ends
end
