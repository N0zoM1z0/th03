; Original Borland DOS large-model buffered fread, with private read loop.
; First near Pascal helper: FILE far pointer,buffer far pointer,count WORD;
; buffered state, stream errors, bulk-read fallback and fgetc supplier.
; Public far fread takes (buffer, element_size, count, FILE far ptr),
; multiplies element widths via genuine N_LXMUL@ and advances far pointers
; via original N_PADD@ while tracking partial records.
; Original FLAGS/IO stream byte offsets and original unchecked behavior
; are preserved; no output CODE DB arrays or synthetic padding.
.8086
extrn __fgetc:far
extrn __rtl_read:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
extrn N_LXMUL@:near
extrn N_PADD@:near
fread_buffered_core proc near
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    jmp near ptr loop_buffered_request
read_next_buffered_chunk:
    inc word ptr [bp+8]
    les bx, dword ptr [bp+4]
    mov ax, word ptr es:[bx+6]
    cmp ax, word ptr [bp+8]
    jbe short check_stream_remaining
    mov ax, word ptr [bp+8]
    jmp short store_buffered_limit
check_stream_remaining:
    les bx, dword ptr [bp+4]
    mov ax, word ptr es:[bx+6]
store_buffered_limit:
    mov word ptr [bp-2], ax
    les bx, dword ptr [bp+4]
    test byte ptr es:[bx+2], 040h
    jne short test_buffered_stream
    jmp near ptr decrement_buffered_left
test_buffered_stream:
    cmp word ptr es:[bx+6], 0
    jne short try_buffered_bulk
    jmp near ptr decrement_buffered_left
try_buffered_bulk:
    mov ax, word ptr es:[bx+6]
    cmp ax, word ptr [bp+8]
    jae short decrement_buffered_left
    cmp word ptr es:[bx], 0
    jne short decrement_buffered_left
    dec word ptr [bp+8]
    mov word ptr [bp-2], 0
    jmp short check_remaining_buffer
add_buffered_count:
    les bx, dword ptr [bp+4]
    add bx, 6
    mov word ptr [bp-4], bx
    mov ax, word ptr es:[bx]
    add word ptr [bp-2], ax
    sub word ptr [bp+8], ax
check_remaining_buffer:
    les bx, dword ptr [bp+4]
    mov ax, word ptr es:[bx+6]
    cmp ax, word ptr [bp+8]
    jbe short add_buffered_count
    push word ptr [bp-2]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
    call __rtl_read
    add sp, 8
    mov dx, ax
    cmp dx, -1
    jne short record_bulk_progress
    xor dx, dx
    les bx, dword ptr [bp+4]
    or word ptr es:[bx+2], 010h
record_bulk_progress:
    add word ptr [bp+0ah], dx
    cmp dx, word ptr [bp-2]
    je short loop_buffered_request
    mov ax, word ptr [bp-2]
    sub ax, dx
    add word ptr [bp+8], ax
read_at_0af:
    les bx, dword ptr [bp+4]
    or word ptr es:[bx+2], 020h
    jmp short buffered_core_return
copy_single_buffered_byte:
    les bx, dword ptr [bp+0ah]
    mov byte ptr es:[bx], dl
    inc word ptr [bp+0ah]
decrement_buffered_left:
    dec word ptr [bp+8]
    mov ax, word ptr [bp+8]
    or ax, ax
    je short buffered_chunk_finished
    dec word ptr [bp-2]
    je short buffered_chunk_finished
    les bx, dword ptr [bp+4]
    dec word ptr es:[bx]
    jl short get_fresh_stream_character
    mov dx, word ptr es:[bx+0eh]
    mov si, word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov es, dx
    mov al, byte ptr es:[si]
    mov ah, 0
    jmp short check_character_result
get_fresh_stream_character:
    push word ptr [bp+6]
    push word ptr [bp+4]
    call __fgetc
    pop cx
    pop cx
check_character_result:
    mov dx, ax
    cmp ax, 0ffffh
    jne short copy_single_buffered_byte
buffered_chunk_finished:
    cmp dx, -1
    je short read_at_0af
loop_buffered_request:
    cmp word ptr [bp+8], 0
    je short buffered_core_return
    jmp near ptr read_next_buffered_chunk
buffered_core_return:
    mov ax, word ptr [bp+8]
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0ah
fread_buffered_core endp
public _fread
_fread proc far
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    cmp word ptr [bp+0ah], 0
    jne short compute_total_byte_count
    xor ax, ax
    jmp near ptr fread_return
compute_total_byte_count:
    mov bx, word ptr [bp+0ah]
    xor cx, cx
    mov ax, word ptr [bp+0ch]
    xor dx, dx
    call N_LXMUL@
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
    cmp dx, 1
    ja short read_large_total
    jb short short_simple_read
    or ax, ax
    jae short read_large_total
short_simple_read:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-6]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    call fread_buffered_core
    mov dx, word ptr [bp-6]
    sub dx, ax
    push dx
    xor dx, dx
    pop ax
    div word ptr [bp+0ah]
    jmp short fread_return
read_large_total:
    mov ax, word ptr [bp+0ch]
    inc ax
    mov word ptr [bp-2], ax
    jmp short continue_large_record
advance_far_buffer:
    mov bx, word ptr [bp+0ah]
    xor cx, cx
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    call N_PADD@
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
continue_large_record:
    dec word ptr [bp-2]
    mov ax, word ptr [bp-2]
    or ax, ax
    je short large_block_finished
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ah]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    call fread_buffered_core
    or ax, ax
    je short advance_far_buffer
large_block_finished:
    mov ax, word ptr [bp+0ch]
    sub ax, word ptr [bp-2]
fread_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_fread endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
