/* MAINL break management, reconstructed from observable CRT behavior.
 * 16-bit unsigned arithmetic and signed-long overflow comparison are part of
 * the ABI. Do not replace this by a modern allocator or linear uintptr_t test.
 */
/* Explicit segmented operations avoid importing DOS.H's model-dependent
 * setblock declaration: this module uses near code and a far DOS wrapper. */
#define FP_SEG(p) ((unsigned)(void __seg *)(void far *)(p))
#define FP_OFF(p) ((unsigned)(p))
#define MK_FP(s,o) ((void __seg *)(s) + (void near *)(o))

typedef char huge *heap_pointer;
extern unsigned _psp;
extern heap_pointer _heapbase, _brklvl, _heaptop;
extern int far cdecl setblock(unsigned segment, unsigned paragraphs);

/* Number of 1024-byte granules last successfully requested from DOS. */
static unsigned granule_count = 0;

/* Internal near Pascal function: callee removes the four-byte pointer. */
static int near pascal grow_break(heap_pointer desired)
{
    unsigned paragraphs;
    unsigned available;

    paragraphs = FP_SEG(desired) + 1;
    paragraphs -= _psp;
    paragraphs = (paragraphs + 63) >> 6;
    if (paragraphs != granule_count) {
        paragraphs <<= 6;
        available = FP_SEG(_heaptop);
        if ((unsigned)(paragraphs + _psp) > available)
            paragraphs = available - _psp;
        available = setblock(_psp, paragraphs);
        if (available == (unsigned)-1)
            granule_count = paragraphs >> 6;
        else {
            /* DOS failure revises the top even though the break is unchanged. */
            _heaptop = (heap_pointer)MK_FP(_psp + available, 0);
            return 0;
        }
    }
    _brklvl = desired;
    return 1;
}

int near cdecl _brk(heap_pointer desired)
{
    if (desired < _heapbase || desired > _heaptop || !grow_break(desired))
        return -1;
    return 0;
}

heap_pointer near cdecl _sbrk(long increment)
{
    heap_pointer desired;
    heap_pointer previous;
    /* The signed test deliberately allows negative physical sums. Huge
     * pointer arithmetic wraps them modulo 1 MiB before the range checks. */
    if (((long)FP_SEG(_brklvl) << 4) + FP_OFF(_brklvl) + increment > 0xFFFFFL)
        return (heap_pointer)-1L;
    desired = _brklvl + increment;
    if (desired < _heapbase || desired > _heaptop)
        return (heap_pointer)-1L;
    previous = _brklvl;
    if (!grow_break(desired))
        return (heap_pointer)-1L;
    return previous;
}
