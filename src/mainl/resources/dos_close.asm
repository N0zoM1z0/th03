; Maintained TH03 MAINL resource source.
; DOS_CLOSE and FONTFILE_CLOSE alias the same entry; map DOS error to InvalidData with original carry.
; Original symbolic statements, EVEN directives, macros and aliases are retained.
; DATA/BSS declarations and imported routines remain contextual unless separately owned.
; Native target proof and device models are separate from source token identity.

; superimpose & master library module
;
; Description:
;	ファイルのクローズ
;
; Functions/Procedures:
;	int fontfile_close( int fh ) ;
;	int dos_close( int fh ) ;		(別名)
;
; Parameters:
;	
;
; Returns:
;	
;
; Binding Target:
;	Microsoft-C / Turbo-C / Turbo Pascal
;
; Running Target:
;	PC-9801
;
; Requiring Resources:
;	CPU: 8086
;
; Notes:
;	
;
; Compiler/Assembler:
;	TASM 3.0
;	OPTASM 1.6
;
; Author:
;	Kazumi(奥田  仁)
;	恋塚(恋塚昭彦)
;
; Revision History:
;
;$Id: fntclose.asm 0.03 93/01/15 11:41:01 Kazumi Rel $
;
;	93/ 3/17 Initial: master.lib <- super.lib 0.22b
;

func DOS_CLOSE		; ラベル付け
endfunc
func FONTFILE_CLOSE	; {
	mov	BX,SP
	; 引数
	@@handle	= (RETSIZE+0)*2

	mov	AH,3eh
	mov	BX,SS:[BX+@@handle]
	int	21h			;close handle
	mov	AX,NoError
	jnc	short CLOSE_SUCCESS
	mov	AX,InvalidData
CLOSE_SUCCESS:
	ret	2
endfunc			; }
