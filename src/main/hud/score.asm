; Research source proposal, not compiled, installed or credited.
; Genuine AL/CX/ES glyph interface and writable-CS immediate are intentional.
.386
.model use16 large _TEXT
locals ; enables the accepted include's @@ procedure-local labels
SCORE_DIGITS = 8
PLAYER_COUNT = 2
SCORE_GLYPH_BYTES = 8
ROW_SIZE = 80
SEG_PLANE_B = 0A800h
GC_RMW = 0C0h
V_WHITE = 15
EXTENDS_MAX = 2
EXTENDS_DISABLE = 255
RESIDENT_STORY_LIVES = 34h
BACKGROUND_RECORD_BYTES = 16
BACKGROUND_CLEAR_RECORD = 70
BACKGROUND_CLEAR_FIELD = 2
BACKGROUND_CLEAR_STORES = 14
_DATA segment word public 'DATA' use16
extrn _sSCORE_FONT:byte, _FIVE_DIGIT_POWERS_OF_10:word
_DATA ends
_BSS segment word public 'BSS' use16
extrn _score:byte, _score_p1:byte, _temp_lebcd:byte
extrn _extends_gained:byte, _resident:dword
; An alias to EXISTING DS:39CC storage, never a new allocation.
extrn _background_particles:byte
_BSS ends
DGROUP group _DATA, _BSS
HUD_STAT_TEXT segment byte public 'CODE' use16
extrn @hud_static_story_lives_put$qv:near
HUD_STAT_TEXT ends
main_01 group HUD_STAT_TEXT, PLAYER_M_TEXT
extrn GRCG_SETCOLOR:far, GRCG_OFF:far, SND_SE_PLAY:far
PLAYER_M_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP, es:nothing
public score_glyph_put, score_hud_render, background_overlap_clear
public @HUD_DYNAMIC_5_DIGIT_POINTS_PUT$QIIUIUC
public score_bonus_digits_put, score_credit_digit_set

; Input AL glyph, CX horizontal pixel coordinate, ES destination VRAM.
; Requires DF=0. Preserves SI/DI and CX; AX/flags clobbered.
; Seven visible rows run bottom-to-top from an eight-byte glyph slot.
; The offset carry test is the original loop bound; no clipping is added.
score_glyph_put proc near
 push si
 push di
 mov ah, 0
 mov si, offset _sSCORE_FONT
 shl ax, 3
 add si, ax
 mov ax, cx
 sar ax, 3
 add ax, (SCORE_GLYPH_BYTES-2)*ROW_SIZE
 mov di, ax
score_glyph_row:
 movsb
 sub di, ROW_SIZE+1
 jnc score_glyph_row
 pop di
 pop si
 retn
score_glyph_put endp
 even

; Draw both eight-byte little-endian BCD scores, suppress leading zeroes,
; append implicit tens zero to P2 and mutable credit digit to P1.
; Extend when P1 digit6 exceeds extends_gained, disabling after two awards.
score_hud_render proc near
 push (GC_RMW shl 16)+V_WHITE
 call GRCG_SETCOLOR
 mov ax, SEG_PLANE_B+(9*ROW_SIZE)/16
 mov es, ax
 mov cx, 544
 mov bx, offset _score
 add bx, PLAYER_COUNT*SCORE_DIGITS-1
 mov dh, PLAYER_COUNT*SCORE_DIGITS
score_player_begin:
 xor dl, dl
score_next_digit:
 mov al, [bx]
 or dl, al
 jz short score_skip_leading_zero
 call score_glyph_put
score_skip_leading_zero:
 dec bx
 add cx, 8
 dec dh
 jz short score_credit_instruction
 cmp dh, SCORE_DIGITS
 jnz short score_next_digit
 xor ax, ax
 call score_glyph_put
 mov cx, 224
 jmp short score_player_begin
score_credit_instruction:
 mov al, 80h
 call score_glyph_put
 call GRCG_OFF
 mov al, _score_p1[6]
 cmp _extends_gained, al
 jnb short score_render_done
 push 8
 call SND_SE_PLAY
 les bx, _resident
 inc byte ptr es:[bx+RESIDENT_STORY_LIVES]
 call @hud_static_story_lives_put$qv
 inc _extends_gained
 cmp _extends_gained, EXTENDS_MAX
 jnz short score_render_done
 mov _extends_gained, EXTENDS_DISABLE
score_render_done:
 retn
score_hud_render endp
 even

; Observed overlapping-word clear, NOT a score-array clear.
; Clears 15 distinct bytes by 14 stores. Intent/storage lifetime still open.
background_overlap_clear proc far
 xor ax, ax
 mov bx, offset _background_particles+BACKGROUND_CLEAR_RECORD*BACKGROUND_RECORD_BYTES+BACKGROUND_CLEAR_FIELD
 mov cx, BACKGROUND_CLEAR_STORES
background_clear_byte_stride:
 mov [bx], ax
 inc bx
 loop background_clear_byte_stride
 retf
background_overlap_clear endp
 even

; Existing accepted 88B owner: include unchanged, no new credit.
include src/main/player/score_add.inl
 even

; Far Pascal (left,top,unsigned points,byte color in word slot), RETF8.
; Draws up to five digits plus implicit trailing zero, always units and zero.
@HUD_DYNAMIC_5_DIGIT_POINTS_PUT$QIIUIUC proc far
 push bp
 mov bp, sp
 push si
 push di
 push GC_RMW
 mov al, [bp+6]
 mov ah, 0
 push ax
 call GRCG_SETCOLOR
 mov ax, [bp+10]
 mov dx, ax
 shl ax, 2
 add ax, dx
 add ax, SEG_PLANE_B+ROW_SIZE/16
 mov es, ax
 mov cx, [bp+12]
 mov si, offset _FIVE_DIGIT_POWERS_OF_10
 mov di, [bp+8]
 mov bl, 0
 even
points_next_digit:
 mov ax, di
 xor dx, dx
 div word ptr [si]
 mov di, dx
 or bl, al
 jz short points_skip_leading_zero
 call score_glyph_put
points_skip_leading_zero:
 add cx, 8
 add si, 2
 cmp word ptr [si], 1
 ja short points_next_digit
 mov ax, di
 call score_glyph_put
 add cx, 8
 xor ax, ax
 call score_glyph_put
 call GRCG_OFF
 pop di
 pop si
 pop bp
 retf 8
@HUD_DYNAMIC_5_DIGIT_POINTS_PUT$QIIUIUC endp
 even

; Same real far Pascal ABI. Zero remains blank; no implicit trailing zero.
; Deliberately leaves GRCG active: callers must own the subsequent cleanup.
score_bonus_digits_put proc far
 push bp
 mov bp, sp
 push si
 push di
 push GC_RMW
 mov al, [bp+6]
 mov ah, 0
 push ax
 call GRCG_SETCOLOR
 mov ax, [bp+10]
 mov dx, ax
 shl ax, 2
 add ax, dx
 add ax, SEG_PLANE_B+ROW_SIZE/16
 mov es, ax
 mov cx, [bp+12]
 mov si, offset _FIVE_DIGIT_POWERS_OF_10
 mov di, [bp+8]
 mov bl, 0
 even
bonus_next_digit:
 mov ax, di
 xor dx, dx
 div word ptr [si]
 mov di, dx
 or bl, al
 jz short bonus_skip_leading_zero
 call score_glyph_put
bonus_skip_leading_zero:
 add cx, 8
 add si, 2
 cmp word ptr [si], 1
 ja short bonus_next_digit
 mov ax, di
 or bl, al
 jz short bonus_done
 call score_glyph_put
bonus_done:
 pop di
 pop si
 pop bp
 retf 8
score_bonus_digits_put endp
 even

; Real writable-code contract: points at operand byte of MOV AL,imm8 above.
; Input remaining credits; low-byte subtraction wraps, as in the original.
score_credit_digit_set proc far
 push bp
 mov bp, sp
 mov al, [bp+6]
 mov ah, 3
 sub ah, al
 mov byte ptr cs:score_credit_instruction+1, ah
 pop bp
 retf 2
score_credit_digit_set endp
 even
PLAYER_M_TEXT ends
end
