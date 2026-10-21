; Maintained TH03 MAINL resource source.
; Paragraph rounding retains carry via RCR; release moves EndMark, not heap free; failure flags preserved.
; Original symbolic statements, EVEN directives, macros and aliases are retained.
; DATA/BSS declarations and imported routines remain contextual unless separately owned.
; Native target proof and device models are separate from source token identity.

; master library - MS-DOS
;
; Description:
;	高速メモリ取得で得たメモリの開放
;
; Functions:
;	void smem_release( unsigned memseg ) ;
;
; Parameters:
;	memseg	開放する[smem_wget,smem_lgetのどちらかで得た]セグメントアドレス
;
; Returns:
;	none
;
; Notes:
;	レジスタは全て保存します。
;
; Revision History:
;	93/ 3/20 Initial
;

	; void smem_release( unsigned memseg ) ;
func SMEM_RELEASE
	push	BX
	mov	BX,SP
	; 引数
	memseg	= (RETSIZE+1)*2
	mov	BX,SS:[BX+memseg]
	mov	mem_EndMark,BX
	pop	BX
	ret	2
endfunc
