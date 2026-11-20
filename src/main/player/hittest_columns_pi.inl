	// PI build only. A negative starting column has to use a signed stride.
	// With an unsigned byte product, the subsequent near pointer wraps into
	// unrelated DGROUP data even though the negative column itself is skipped.
	initial_mask_ready:
		mov al, dl;
		cbw;
		push dx;
		mov bx, COLLMAP_H;
		imul bx;
		pop dx;
		mov bx, offset collmap;
		add bx, ax;
		cmp byte ptr pid.current, 1;
		jne bitmap_selected;
		add bx, COLLMAP_SIZE;
	bitmap_selected:
		add bx, tile_top;
		mov dh, tile_bottom;
		mov ax, tile_top;
	column_scan:
		cmp dl, COLLMAP_MEMORY_W;
		jge collision_done;
		// The skip path also advances by one complete column.
		mov cl, COLLMAP_H;
		or dl, dl;
		jl next_column;
		mov ah, al;
