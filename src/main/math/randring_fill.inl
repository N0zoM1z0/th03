; Bounded MAIN CODE include; assembled in the frozen th03_main.asm carrier.
; Ambient symbol/layout contracts are reviewed in MAIN_BOUNDED_ASM_REVIEW.md.
public @randring_fill$qv
@randring_fill$qv proc near
	push	si
	mov	si, RANDRING_SIZE - 1

@@loop:
	call	IRand
	mov	_randring[si], al
	dec	si
	jge	short @@loop
if GAME ge 4
	mov	_randring_p, 0
endif
	pop	si
	ret
@randring_fill$qv endp
