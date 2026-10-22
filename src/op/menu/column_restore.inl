// Complete TH03 OP column restoration, included in the original title TU.
void pascal near box_column16_unput(uscreen_x_t left)
{
    enum {
        PIXELS_PER_BYTE_SHIFT = 3,
        LAST_ROW_OFFSET = (BOX_BOTTOM - 1) * ROW_SIZE,
        BOX_SEGMENT_OFFSET = BOX_TOP * ROW_SIZE / 16,
        BOX_BLUE_SEGMENT = SEG_PLANE_B + BOX_SEGMENT_OFFSET,
        BOX_RED_SEGMENT = SEG_PLANE_R + BOX_SEGMENT_OFFSET,
        BOX_GREEN_SEGMENT = SEG_PLANE_G + BOX_SEGMENT_OFFSET,
        BOX_EXTRA_SEGMENT = SEG_PLANE_E + BOX_SEGMENT_OFFSET,
        GRAPH_ACCESS_PORT = 0xA6,
    };
    // Keep the original bottom-coordinate loop bound, rather than fixing it to
    // BOX_H. This intentionally reaches beyond VRAM into adjacent memory.
    // DX/CX/BX/SI retain the blue/red/green/extra plane words across page changes.
    // TC4 owns BP/SI/DI preservation, the real left argument, and near RET 2.
    asm {
        mov ax, left;
        shr ax, PIXELS_PER_BYTE_SHIFT;
        mov di, LAST_ROW_OFFSET;
        add di, ax;
        mov ax, BOX_BLUE_SEGMENT;
        mov es, ax;
    restore_row:
        mov al, 1;
        out GRAPH_ACCESS_PORT, al;
        mov dx, es:[di];
        mov ax, BOX_RED_SEGMENT;
        mov es, ax;
        mov cx, es:[di];
        mov ax, BOX_GREEN_SEGMENT;
        mov es, ax;
        mov bx, es:[di];
        mov ax, BOX_EXTRA_SEGMENT;
        mov es, ax;
        mov si, es:[di];
        xor al, al;
        out GRAPH_ACCESS_PORT, al;
        mov es:[di], si;
        mov ax, BOX_GREEN_SEGMENT;
        mov es, ax;
        mov es:[di], bx;
        mov ax, BOX_RED_SEGMENT;
        mov es, ax;
        mov es:[di], cx;
        mov ax, BOX_BLUE_SEGMENT;
        mov es, ax;
        mov es:[di], dx;
        sub di, ROW_SIZE;
        jnc restore_row;
    }
}
