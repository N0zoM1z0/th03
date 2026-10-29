; Search the DOS MCB chain for the resident palette signature.
include src/mainl/root_tail/resident_mcb.inc
func RESPAL_EXIST
	push	SI
	push	DI

	; 常駐パレットの捜索
	mov	AH, 52h
	int	21h
	CLD
	mov	BX, ES:[BX-2]
RSPEXIST_FIND:
		mov	ES,BX
		inc	BX
		mov	AX,ES:[_mcb_owner]
		or	AX,AX
		je	short RSPEXIST_SKIP
			mov	DI,10h ; MCBの次
			mov	CX,IDLEN
			mov	SI,offset ResPalID
			repe cmpsb
			je	short RSPEXIST_FOUND
		RSPEXIST_SKIP:
		mov	AX,ES:[_mcb_size]
		add	BX,AX
	mov	AL,ES:[_mcb_flg]
	cmp	AL,'M'
	je	short RSPEXIST_FIND
RSPEXIST_NOTFOUND:
	mov	BX,0
RSPEXIST_FOUND:
	mov	AX,BX
	mov	ResPalSeg,AX

	pop	DI
	pop	SI
	ret
	EVEN
endfunc
