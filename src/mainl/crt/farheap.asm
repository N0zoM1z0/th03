; Paragraph-based far heap. Returned user pointers have offset4; block headers
; keep paragraph count and the preceding physical segment. A zero predecessor
; marks a free block, whose circular-list links occupy offsets4/6 and whose
; preceding physical segment is saved at8. All arithmetic is unsigned16.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
extrn __brk:near,__sbrk:near
public ___first,___last,___rover
public _farfree,_free,_malloc,_farmalloc,_realloc,_farrealloc

block_paragraphs equ 0
block_previous equ 2
free_previous equ 4
free_next equ 6
free_physical_previous equ 8
user_offset equ 4

___first dw 0
___last dw 0
___rover dw 0
; Scratch belongs to writable CS, not DGROUP. Keep the original uninitialized
; declarations and global, non-reentrant save/restore contract.
saved_dgroup dw ?
resize_high dw ?
resize_low dw ?

; DX is the last allocated block. Release it and an adjacent preceding free
; block when present, unlinking the latter before committing the new break.
release_top proc near
    cmp dx,cs:___first
    je reset_heap
    mov ds,dx
    mov ds,word ptr ds:[block_previous]
    cmp word ptr ds:[block_previous],0
    je top_previous_free
    mov cs:___last,ds
    jmp short top_restore_dgroup
top_previous_free:
    mov ax,ds
    cmp ax,cs:___first
    je top_release_first
    mov ax,word ptr ds:[free_physical_previous]
    mov cs:___last,ax
    push ds
    xor ax,ax
    push ax
    call unlink_free
    mov ds,cs:saved_dgroup
    jmp short top_set_break
top_release_first:
    mov dx,cs:___first
reset_heap:
    mov cs:___first,0
    mov cs:___last,0
    mov cs:___rover,0
top_restore_dgroup:
    mov ds,cs:saved_dgroup
    push dx
    xor ax,ax
    push ax
top_set_break:
    call __brk
    add sp,4
    ret
release_top endp

; Free an interior block, coalesce preceding/following free neighbors, then
; borrow unlink_free's return when the following free node is removed.
release_inner proc near
    mov ds,dx
    push ds
    mov es,word ptr ds:[block_previous]
    mov word ptr ds:[block_previous],0
    mov word ptr ds:[free_physical_previous],es
    cmp dx,cs:___first
    je inner_insert
    cmp word ptr es:[block_previous],0
    jne inner_insert
    mov ax,word ptr ds:[block_paragraphs]
    pop bx
    push es
    add word ptr es:[block_paragraphs],ax
    mov cx,es
    add dx,ax
    mov es,dx
    cmp word ptr es:[block_previous],0
    jne inner_next_allocated
    mov word ptr es:[free_physical_previous],cx
    jmp short inner_merge_next
inner_next_allocated:
    mov word ptr es:[block_previous],cx
    jmp short inner_merge_next
inner_insert:
    call insert_free
inner_merge_next:
    pop es
    mov ax,es
    add ax,word ptr es:[block_paragraphs]
    mov ds,ax
    cmp word ptr ds:[block_previous],0
    je inner_next_free
    ret
inner_next_free:
    mov ax,word ptr ds:[block_paragraphs]
    add word ptr es:[block_paragraphs],ax
    mov ax,es
    mov bx,ds
    add bx,word ptr ds:[block_paragraphs]
    mov es,bx
    mov word ptr es:[block_previous],ax
release_inner endp

; DS names a free-list node. Preserve DS while unlinking it; rover moves to
; its predecessor, or becomes zero when the sole ring element is removed.
unlink_free proc near
    mov bx,ds
    cmp bx,word ptr ds:[free_next]
    je unlink_single
    mov es,word ptr ds:[free_next]
    mov ds,word ptr ds:[free_previous]
    mov word ptr ds:[free_next],es
    mov word ptr es:[free_previous],ds
    mov cs:___rover,ds
    mov ds,bx
    ret
unlink_single:
    mov cs:___rover,0
    ret
unlink_free endp

; Insert DS into the free ring. The original code temporarily addresses the
; rover through SS under CLI, restoring SS before touching the real stack.
insert_free proc near
    mov ax,cs:___rover
    or ax,ax
    je insert_first
    mov bx,ss
    pushf
    cli
    mov ss,ax
    mov es,word ptr ss:[free_next]
    mov word ptr ss:[free_next],ds
    mov word ptr ds:[free_previous],ss
    mov ss,bx
    popf
    mov word ptr es:[free_previous],ds
    mov word ptr ds:[free_next],es
    ret
insert_first:
    mov cs:___rover,ds
    mov word ptr ds:[free_previous],ds
    mov word ptr ds:[free_next],ds
    ret
insert_free endp

; Far cdecl free ignores the offset word and uses the supplied segment.
_free proc far
_farfree label far
    push bp
    mov bp,sp
    push si
    push di
    mov cs:saved_dgroup,ds
    mov dx,[bp+8]
    or dx,dx
    je free_done
    cmp dx,cs:___last
    jne free_interior
    call release_top
    jmp short free_done
free_interior:
    call release_inner
free_done:
    mov ds,cs:saved_dgroup
    pop di
    pop si
    pop bp
    retf
_free endp

; AX paragraphs starts a heap after aligning the existing break. Keep each
; original sbrk call and the AX-only FFFF failure test.
start_heap proc near
    push ax
    mov ds,cs:saved_dgroup
    xor ax,ax
    push ax
    push ax
    call __sbrk
    add sp,4
    and ax,15
    je start_aligned
    mov dx,16
    sub dx,ax
    xor ax,ax
    mov ds,cs:saved_dgroup
    push ax
    push dx
    call __sbrk
    add sp,4
start_aligned:
    pop ax
    push ax
    xor bx,bx
    mov bl,ah
    mov cl,4
    shr bx,cl
    shl ax,cl
    mov ds,cs:saved_dgroup
    push bx
    push ax
    call __sbrk
    add sp,4
    pop bx
    cmp ax,-1
    je start_failed
    mov cs:___first,dx
    mov cs:___last,dx
    mov ds,dx
    mov word ptr ds:[block_paragraphs],bx
    mov word ptr ds:[block_previous],dx
    mov ax,user_offset
    ret
start_failed:
    xor ax,ax
    cwd
    ret
start_heap endp

; Extend an existing heap. The second alignment request and its unchecked
; earlier allocations are intentional; do not add rollback or error guards.
extend_heap proc near
    push ax
    mov ds,cs:saved_dgroup
    xor ax,ax
    push ax
    push ax
    call __sbrk
    pop bx
    pop bx
    and ax,15
    je extend_aligned
    mov dx,16
    sub dx,ax
    xor ax,ax
    mov ds,cs:saved_dgroup
    push ax
    push dx
    call __sbrk
    add sp,4
extend_aligned:
    pop ax
    push ax
    xor bx,bx
    mov bl,ah
    mov cl,4
    shr bx,cl
    shl ax,cl
    mov ds,cs:saved_dgroup
    push bx
    push ax
    call __sbrk
    add sp,4
    pop bx
    cmp ax,-1
    je extend_failed
    and ax,15
    jne extend_realign
extend_commit:
    mov cx,cs:___last
    mov cs:___last,dx
    mov ds,dx
    mov word ptr ds:[block_paragraphs],bx
    mov word ptr ds:[block_previous],cx
    mov ax,user_offset
    ret
extend_realign:
    push bx
    push dx
    neg ax
    add ax,16
    xor bx,bx
    push bx
    push ax
    call __sbrk
    add sp,4
    pop dx
    pop bx
    cmp ax,-1
    je extend_failed
    inc dx
    jmp short extend_commit
extend_failed:
    xor ax,ax
    cwd
    ret
extend_heap endp

; Allocate AX paragraphs from the tail of the free block at DS:DX.
take_free_tail proc near
    mov bx,dx
    sub word ptr ds:[block_paragraphs],ax
    add dx,word ptr ds:[block_paragraphs]
    mov ds,dx
    mov word ptr ds:[block_paragraphs],ax
    mov word ptr ds:[block_previous],bx
    mov bx,dx
    add bx,word ptr ds:[block_paragraphs]
    mov ds,bx
    mov word ptr ds:[block_previous],dx
    mov ax,user_offset
    ret
take_free_tail endp

; Far cdecl word/long byte-count entries share the paragraph allocation body.
_malloc proc far
    push bp
    mov bp,sp
    xor dx,dx
    mov ax,[bp+6]
    jmp short allocation_request
_malloc endp
_farmalloc proc far
    push bp
    mov bp,sp
    mov dx,[bp+8]
    mov ax,[bp+6]
allocation_request:
    mov cx,ax
    or cx,dx
    push si
    push di
    mov cs:saved_dgroup,ds
    je allocation_done
    add ax,19
    adc dx,0
    jc allocation_failed
    test dx,0fff0h
    jne allocation_failed
    mov cl,4
    shr ax,cl
    shl dx,cl
    or ah,dl
    mov dx,cs:___first
    or dx,dx
    je allocation_start
    mov dx,cs:___rover
    or dx,dx
    je allocation_extend
    mov bx,dx
allocation_scan:
    mov ds,dx
    cmp word ptr ds:[block_paragraphs],ax
    jae allocation_found
    mov dx,word ptr ds:[free_next]
    cmp dx,bx
    jne allocation_scan
allocation_extend:
    call extend_heap
    jmp short allocation_done
allocation_start:
    call start_heap
    jmp short allocation_done
allocation_split:
    call take_free_tail
    jmp short allocation_done
allocation_failed:
    xor ax,ax
    cwd
    jmp short allocation_done
allocation_found:
    ja allocation_split
    call unlink_free
    mov bx,word ptr ds:[free_physical_previous]
    mov word ptr ds:[block_previous],bx
    mov ax,user_offset
allocation_done:
    mov ds,cs:saved_dgroup
    pop di
    pop si
    pop bp
    retf
_farmalloc endp

; Grow by allocating elsewhere, copy the old payload in 64-KiB pieces and
; free the old block. The old block size bounds the copy, not the new request.
move_growing_block proc near
    push bx
    mov si,cs:resize_high
    push si
    mov si,cs:resize_low
    push si
    call _farmalloc
    add sp,4
    or dx,dx
    jne move_copy
    pop bx
    ret
move_copy:
    pop ds
    mov es,dx
    push es
    push ds
    push bx
    mov dx,word ptr ds:[block_paragraphs]
    cld
    dec dx
    mov di,user_offset
    mov si,di
    mov cx,6
    rep movsw
    or dx,dx
    je move_free_old
    mov ax,es
    inc ax
    mov es,ax
    mov ax,ds
    inc ax
    mov ds,ax
move_chunk:
    xor di,di
    mov si,di
    mov cx,dx
    cmp cx,1000h
    jbe move_chunk_count
    mov cx,1000h
move_chunk_count:
    shl cx,1
    shl cx,1
    shl cx,1
    rep movsw
    sub dx,1000h
    jbe move_free_old
    mov ax,es
    add ax,1000h
    mov es,ax
    mov ax,ds
    add ax,1000h
    mov ds,ax
    jmp short move_chunk
move_free_old:
    mov ds,cs:saved_dgroup
    call _free
    add sp,4
    pop dx
    mov ax,user_offset
    ret
move_growing_block endp

; AX requested paragraphs, BX block segment, CX old paragraphs. Interior
; shrink creates a remainder and borrows free's merge logic; top shrink brks.
shrink_block proc near
    cmp bx,cs:___last
    je shrink_top
    mov di,bx
    add di,ax
    mov es,di
    mov si,cx
    sub si,ax
    mov word ptr es:[block_paragraphs],si
    mov word ptr es:[block_previous],bx
    push es
    push ax
    mov es,bx
    mov word ptr es:[block_paragraphs],ax
    mov dx,bx
    add dx,cx
    mov es,dx
    cmp word ptr es:[block_previous],0
    je shrink_next_free
    mov word ptr es:[block_previous],di
    jmp short shrink_free_remainder
shrink_next_free:
    mov word ptr es:[free_physical_previous],di
shrink_free_remainder:
    mov si,bx
    call _free
    add sp,4
    mov dx,si
    mov ax,user_offset
    ret
shrink_top:
    push bx
    mov es,bx
    mov word ptr es:[block_paragraphs],ax
    add bx,ax
    push bx
    xor ax,ax
    push ax
    call __brk
    add sp,4
    pop dx
    mov ax,user_offset
    ret
shrink_block endp

; Both cdecl resize entries ignore the original pointer offset. A null
; segment allocates; zero requested size frees. Keep the global CS scratch.
_realloc proc far
    push bp
    mov bp,sp
    xor dx,dx
    jmp short reallocation_request
_realloc endp
_farrealloc proc far
    push bp
    mov bp,sp
    mov dx,[bp+12]
reallocation_request:
    mov ax,[bp+10]
    mov bx,[bp+8]
    push si
    push di
    mov cs:saved_dgroup,ds
    mov cs:resize_high,dx
    mov cs:resize_low,ax
    or bx,bx
    je reallocate_null
    mov cx,ax
    or cx,dx
    je reallocate_zero
    add ax,19
    adc dx,0
    jc reallocate_failed
    test dx,0fff0h
    jne reallocate_failed
    mov cl,4
    shr ax,cl
    shl dx,cl
    or ah,dl
    mov es,bx
    mov cx,word ptr es:[block_paragraphs]
    cmp cx,ax
    jb reallocate_grow
    ja reallocate_shrink
    mov dx,bx
    mov ax,user_offset
    jmp short reallocate_done
reallocate_shrink:
    call shrink_block
    jmp short reallocate_done
reallocate_grow:
    call move_growing_block
    jmp short reallocate_done
reallocate_null:
    push dx
    push ax
    call _farmalloc
    add sp,4
    jmp short reallocate_done
reallocate_zero:
    push bx
    push ax
    call _free
    add sp,4
reallocate_failed:
    xor ax,ax
    cwd
reallocate_done:
    mov ds,cs:saved_dgroup
    pop di
    pop si
    pop bp
    retf
_farrealloc endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
end
