; Complete TH03 getter macro definitions, expanded three times in MAIN.
; The root/context carrier chain and all CODE expansions are reviewed.
; Turbo C++ emits Pascal-mangled external names in uppercase. Keep the PROC
; spelling uppercase as well so TASM exports the historical OMF public name;
; this changes no generated instructions or final linked bytes.
RANDRING_NEXT_DEF_NOMOD macro instance, dist
	public @randring&instance&_next16$qv
	@randring&instance&_next16$qv proc dist
		xor	bh, bh
		mov	bl, _randring_p
		add	bx, offset _randring
		inc	_randring_p
		mov	ax, [bx]
		ret
	@randring&instance&_next16$qv endp
		even

	public @RANDRING&instance&_NEXT16_AND$QUI
	@RANDRING&instance&_NEXT16_AND$QUI proc dist
		arg @@mask:word

		push	bp
		mov	bp, sp
		xor	bh, bh
		mov	bl, _randring_p
		add	bx, offset _randring
		inc	_randring_p
		mov	ax, [bx]
		and	ax, @@mask
		pop	bp
		ret	2
	@RANDRING&instance&_NEXT16_AND$QUI endp
endm

RANDRING_NEXT_DEF macro instance, dist
	RANDRING_NEXT_DEF_NOMOD instance, dist

	public @RANDRING&INSTANCE&_NEXT16_MOD$QUI
	@RANDRING&instance&_NEXT16_MOD$QUI proc dist
		arg @@n:word

		push	bp
		mov	bp, sp
		xor	bh, bh
		mov	bl, _randring_p
		add	bx, offset _randring
		inc	_randring_p
		mov	ax, [bx]
		xor	dx, dx
		div	@@n
		mov	ax, dx
		pop	bp
		ret	2
	@RANDRING&instance&_NEXT16_MOD$QUI endp
endm
