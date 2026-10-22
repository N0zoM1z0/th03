// Complete TH03 OP B-plane restoration, included in the original music TU.
// The incoming direction flag is deliberately preserved: REP MOVSW is not CLD.
void near nopoly_B_put(void)
{
    enum { COPY_WORDS = PLANE_SIZE / sizeof(dots16_t) };
    // nopoly_B is a segment-only pointer, not a four-byte far pointer.
    // TC4 owns BP/SI/DI preservation and the ordinary near C return.
    asm {
        push ds;
        mov ax, SEG_PLANE_B;
        mov es, ax;
        mov ax, nopoly_B;
        mov ds, ax;
        xor di, di;
        xor si, si;
        mov cx, COPY_WORDS;
        rep movsw;
        pop ds;
    }
}
