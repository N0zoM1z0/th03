; Borland DOS quicksort recursive partition core. A near __pascal routine
; with a 24-byte local frame and callee cleanup RET 6.
; Entrypoint: [BP+4]=element count, [BP+6..9]=far base.
; Stateful BSS: qsort_compare far pointer, qsort_width word.
; Sorting strategy: handle 0..3 elements, median-of-three selection,
; scan the two sides around the pivot, exchange as necessary, place
; the pivot and recurse on the smaller partition (tail loop for larger).
; The original uses 16-bit near N_LXMUL@/N_LDIV@ arithmetic helpers.
qsort_core proc near
    push bp
    mov bp, sp
    sub sp, 018h
    push si
    push di
again_after_tail_recursion:
    cmp word ptr [bp+4], 2
    ja short prepare_middle_and_last
    cmp word ptr [bp+4], 2
    je short handle_two_elements
    jmp near ptr sort_finished
handle_two_elements:
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    add ax, word ptr qsort_width
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
    push dx
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jg short swap_two_elements
    jmp near ptr sort_finished
swap_two_elements:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-6]
    push word ptr [bp-8]
    jmp near ptr swap_last_two
prepare_middle_and_last:
    mov bx, word ptr [bp+4]
    dec bx
    xor cx, cx
    mov ax, word ptr qsort_width
    xor dx, dx
    call N_LXMUL@
    mov dx, word ptr [bp+8]
    add ax, word ptr [bp+6]
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
    mov bx, word ptr [bp+4]
    shr bx, 1
    xor cx, cx
    mov ax, word ptr qsort_width
    xor dx, dx
    call N_LXMUL@
    mov dx, word ptr [bp+8]
    add ax, word ptr [bp+6]
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    push word ptr [bp-6]
    push word ptr [bp-8]
    push dx
    push ax
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jle short compare_first_with_mid
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp-8]
    call qsort_swap
compare_first_with_mid:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jle short compare_first_with_last
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    jmp short core_0119
compare_first_with_last:
    push word ptr [bp-6]
    push word ptr [bp-8]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jle short small_three_done
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-6]
    push word ptr [bp-8]
core_0119:
    call qsort_swap
small_three_done:
    cmp word ptr [bp+4], 3
    jne short setup_partition
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
swap_last_two:
    call qsort_swap
    jmp near ptr sort_finished
setup_partition:
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    add ax, word ptr qsort_width
    mov word ptr [bp-0ah], dx
    mov word ptr [bp-0ch], ax
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    jmp short compare_left_pivot
advance_partition_left:
    cmp word ptr [bp-018h], 0
    jne short compare_partition_bounds
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp-0ah]
    push word ptr [bp-0ch]
    call qsort_swap
    mov ax, word ptr qsort_width
    add word ptr [bp-0ch], ax
compare_partition_bounds:
    mov ax, word ptr [bp-4]
    cmp ax, word ptr [bp-8]
    jae short check_pivot_placement
    mov ax, word ptr qsort_width
    add word ptr [bp-4], ax
compare_left_pivot:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
    call dword ptr qsort_compare
    add sp, 8
    mov word ptr [bp-018h], ax
    or ax, ax
    jle short advance_partition_left
    jmp short compare_right_bound
compare_right_pivot:
    push word ptr [bp-6]
    push word ptr [bp-8]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call dword ptr qsort_compare
    add sp, 8
    mov word ptr [bp-018h], ax
    or ax, ax
    jge short swap_partition_pair
    mov ax, word ptr qsort_width
    sub word ptr [bp-8], ax
    jmp short compare_right_bound
swap_partition_pair:
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp-8]
    call qsort_swap
    cmp word ptr [bp-018h], 0
    je short compare_left_bound
    mov ax, word ptr qsort_width
    add word ptr [bp-4], ax
    sub word ptr [bp-8], ax
    jmp short compare_left_bound
compare_right_bound:
    mov ax, word ptr [bp-4]
    cmp ax, word ptr [bp-8]
    jb short compare_right_pivot
compare_left_bound:
    mov ax, word ptr [bp-4]
    cmp ax, word ptr [bp-8]
    jb short compare_left_pivot
check_pivot_placement:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jg short prepare_sort_halves
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    add ax, word ptr qsort_width
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
prepare_sort_halves:
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    sub ax, word ptr qsort_width
    mov word ptr [bp-012h], dx
    mov word ptr [bp-014h], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-0eh], dx
    mov word ptr [bp-010h], ax
    jmp short check_pivot_relocation
swap_to_restore_pivot:
    push word ptr [bp-0eh]
    push word ptr [bp-010h]
    push word ptr [bp-012h]
    push word ptr [bp-014h]
    call qsort_swap
    mov ax, word ptr qsort_width
    add word ptr [bp-010h], ax
    sub word ptr [bp-014h], ax
check_pivot_relocation:
    mov ax, word ptr [bp-010h]
    cmp ax, word ptr [bp-0ch]
    jae short compute_recursion_counts
    mov ax, word ptr [bp-014h]
    cmp ax, word ptr [bp-0ch]
    jae short swap_to_restore_pivot
compute_recursion_counts:
    xor ax, ax
    push ax
    push word ptr qsort_width
    mov ax, word ptr [bp-4]
    xor dx, dx
    sub ax, word ptr [bp-0ch]
    sbb dx, 0
    push dx
    push ax
    call N_LDIV@
    mov word ptr [bp-016h], ax
    xor ax, ax
    push ax
    push word ptr qsort_width
    mov ax, word ptr [bp+4]
    imul word ptr qsort_width
    mov dx, word ptr [bp+6]
    add dx, ax
    xor ax, ax
    sub dx, word ptr [bp-4]
    sbb ax, 0
    push ax
    push dx
    call N_LDIV@
    mov word ptr [bp+4], ax
    cmp ax, word ptr [bp-016h]
    jae short recurse_smaller_left
    push word ptr [bp-2]
    push word ptr [bp-4]
    push ax
    call qsort_core
    mov ax, word ptr [bp-016h]
    mov word ptr [bp+4], ax
    jmp near ptr again_after_tail_recursion
recurse_smaller_left:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-016h]
    call qsort_core
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
    jmp near ptr again_after_tail_recursion
sort_finished:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 6
qsort_core endp
