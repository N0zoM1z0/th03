; Create resident palette storage with the original DOS allocation strategy.
include src/mainl/root_tail/resident_mcb.inc
func RESPAL_CREATE
	push	SI
	push	DI

	call	RESPAL_EXIST
	or	AX,AX
	mov	AX,2
	jnz	short RSPEXIST_IGNORE
RSPEXIST_CREATE:
	mov	AX,5800h	; アロケーションストラテジを得る
	int	21h
	mov	DX,AX		; 得たストラテジを保存する

	mov	AX,5801h
	mov	BX,1		; 必要最小のアロケーション
	int	21h
	mov	AH,48h		; メモリ割り当て
	mov	BX,4 ; 64/16
	int	21h
	mov	CX,0
	jc	short RSPEXIST_DAME
	mov	BX,CS		; 自分より前ならＯＫ
	cmp	BX,AX
	jnb	short RSPEXIST_ALLOC_OK
		mov	ES,AX		; 自分より後ろだったら
		mov	AH,49h		; 解放する。
		int	21h		;

		mov	AX,5801h	;
		mov	BX,2		; 最上位からのアロケーション
		int	21h

		mov	AH,48h		; メモリ割り当て
		mov	BX,4 ; 64/16
		int	21h
	RSPEXIST_ALLOC_OK:
	mov	CX,AX
	mov	ResPalSeg,AX

	dec	CX			; MCBのownerを書き換える
	mov	ES,CX			;
	mov	AX,-1			;
	mov	ES:[_mcb_owner],AX	;
	inc	CX
	mov	ES,CX
	cld
	xor	DI,DI			; IDの書き込み
	mov	SI,offset ResPalID	;
	mov	CX,IDLEN		;
	rep movsb
	xor	AX,AX
	stosw
	stosw
	stosw
	mov	CX,1

RSPEXIST_DAME:
	mov	AX,5801h	; アロケーションストラテジの復帰
	mov	BX,DX		;
	int	21h		;
	mov	AX,CX

RSPEXIST_IGNORE:
	pop	DI
	pop	SI
	ret
endfunc
