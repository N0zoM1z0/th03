; Original Borland DOS high-address large-model quicksort recursive core.
; Private near Pascal routine: 24-byte local frame, RET 6.
; This variant retains 32-bit far address carries in real near math
; helpers N_PADD@/N_PADA@/N_PSUB@/N_PSBP@/N_PCMP@, plus
; N_LXMUL@/N_LDIV@ for partition element-count arithmetic.
; Scans first/middle/last, orders the pivot, partitions through the
; genuine original indirect far comparator and real near qsort_swap.
; Recurse on the smaller partition, tail loop on remaining larger.
hqsort_core proc near
    push bp
    mov bp, sp
    sub sp, 018h
    push si
    push di
sort_next_partition:
    cmp word ptr [bp+4], 2
    ja short compute_middle_and_last
    cmp word ptr [bp+4], 2
    je short handle_two_elements
    jmp near ptr sort_finished
handle_two_elements:
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    call N_PADD@
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
    push dx
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jg short sort_two_swap
    jmp near ptr sort_finished
sort_two_swap:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-6]
    push word ptr [bp-8]
    jmp near ptr swap_third_element
compute_middle_and_last:
    mov bx, word ptr [bp+4]
    dec bx
    xor cx, cx
    mov ax, word ptr qsort_width
    xor dx, dx
    call N_LXMUL@
    push ax
    push dx
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop cx
    pop bx
    call N_PADD@
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
    mov bx, word ptr [bp+4]
    shr bx, 1
    xor cx, cx
    mov ax, word ptr qsort_width
    xor dx, dx
    call N_LXMUL@
    push ax
    push dx
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop cx
    pop bx
    call N_PADD@
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    push word ptr [bp-6]
    push word ptr [bp-8]
    push dx
    push ax
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jle short compare_first_mid
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp-8]
    call qsort_swap
compare_first_mid:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jle short compare_first_last
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    jmp short swap_original_pair
compare_first_last:
    push word ptr [bp-6]
    push word ptr [bp-8]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jle short check_three_case
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-6]
    push word ptr [bp-8]
swap_original_pair:
    call qsort_swap
check_three_case:
    cmp word ptr [bp+4], 3
    jne short start_partition
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
swap_third_element:
    call qsort_swap
    jmp near ptr sort_finished
start_partition:
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    call N_PADD@
    mov word ptr [bp-0ah], dx
    mov word ptr [bp-0ch], ax
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    jmp short partition_compare_left
advance_low:
    cmp word ptr [bp-018h], 0
    jne short compare_partition_ranges
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp-0ah]
    push word ptr [bp-0ch]
    call qsort_swap
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, ss
    lea ax, [bp-0ch]
    call N_PADA@
compare_partition_ranges:
    mov cx, word ptr [bp-6]
    mov bx, word ptr [bp-8]
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    call N_PCMP@
    jb short begin_partition
    jmp near ptr partition_done
begin_partition:
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, ss
    lea ax, [bp-4]
    call N_PADA@
partition_compare_left:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
    call dword ptr qsort_compare
    add sp, 8
    mov word ptr [bp-018h], ax
    or ax, ax
    jle short advance_low
    jmp short check_partition_crossing
partition_compare_right:
    push word ptr [bp-6]
    push word ptr [bp-8]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call dword ptr qsort_compare
    add sp, 8
    mov word ptr [bp-018h], ax
    or ax, ax
    jge short exchange_partition_values
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, ss
    lea ax, [bp-8]
    call N_PSBA@
    jmp short check_partition_crossing
exchange_partition_values:
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp-8]
    call qsort_swap
    cmp word ptr [bp-018h], 0
    je short partition_next
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, ss
    lea ax, [bp-4]
    call N_PADA@
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, ss
    lea ax, [bp-8]
    call N_PSBA@
    jmp short partition_next
check_partition_crossing:
    mov cx, word ptr [bp-6]
    mov bx, word ptr [bp-8]
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    call N_PCMP@
    jb short partition_compare_right
partition_next:
    mov cx, word ptr [bp-6]
    mov bx, word ptr [bp-8]
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    call N_PCMP@
    jae short partition_done
    jmp near ptr partition_compare_left
partition_done:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
    call dword ptr qsort_compare
    add sp, 8
    or ax, ax
    jg short recompute_partition_head
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    call N_PADD@
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
recompute_partition_head:
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    call N_PSUB@
    mov word ptr [bp-012h], dx
    mov word ptr [bp-014h], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-0eh], dx
    mov word ptr [bp-010h], ax
    jmp short prepare_recursion
find_second_partition:
    push word ptr [bp-0eh]
    push word ptr [bp-010h]
    push word ptr [bp-012h]
    push word ptr [bp-014h]
    call qsort_swap
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, ss
    lea ax, [bp-010h]
    call N_PADA@
    mov bx, word ptr qsort_width
    xor cx, cx
    mov dx, ss
    lea ax, [bp-014h]
    call N_PSBA@
prepare_recursion:
    mov cx, word ptr [bp-0ah]
    mov bx, word ptr [bp-0ch]
    mov dx, word ptr [bp-0eh]
    mov ax, word ptr [bp-010h]
    call N_PCMP@
    jae short reorder_pivot
    mov cx, word ptr [bp-0ah]
    mov bx, word ptr [bp-0ch]
    mov dx, word ptr [bp-012h]
    mov ax, word ptr [bp-014h]
    call N_PCMP@
    jae short find_second_partition
reorder_pivot:
    xor ax, ax
    push ax
    push word ptr qsort_width
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    mov cx, word ptr [bp-0ah]
    mov bx, word ptr [bp-0ch]
    call N_PSBP@
    push dx
    push ax
    call N_LDIV@
    mov word ptr [bp-016h], ax
    xor ax, ax
    push ax
    push word ptr qsort_width
    mov ax, word ptr [bp+4]
    imul word ptr qsort_width
    xor cx, cx
    mov dx, word ptr [bp+8]
    push ax
    mov ax, word ptr [bp+6]
    pop bx
    call N_PADD@
    mov cx, word ptr [bp-2]
    mov bx, word ptr [bp-4]
    call N_PSBP@
    push dx
    push ax
    call N_LDIV@
    mov word ptr [bp+4], ax
    cmp ax, word ptr [bp-016h]
    jae short sort_remaining_left
    push word ptr [bp-2]
    push word ptr [bp-4]
    push ax
    call hqsort_core
    mov ax, word ptr [bp-016h]
    mov word ptr [bp+4], ax
    jmp near ptr sort_next_partition
sort_remaining_left:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-016h]
    call hqsort_core
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
    jmp near ptr sort_next_partition
sort_finished:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 6
hqsort_core endp
