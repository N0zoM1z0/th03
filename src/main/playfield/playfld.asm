; TH03 MAIN complete playfield owner. Symbolic instructions and word
; alignment; no raw instruction bytes or codestrings.
.386
extrn _playfield_fg_shift_x:word
extrn _playfield_clip_negative_radius:word

SUBPIXEL_BITS = 4
PLAYFIELD_W = 288
PLAYFIELD_H = 368
PLAYFIELD_W_BORDERED = 320
PLAYFIELD_LEFT = 16
PLAYFIELD_BORDER = 16

_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS

PLAYFLD_TEXT segment byte public 'CODE' use16
assume cs:PLAYFLD_TEXT, ds:DGROUP

public @PLAYFIELD_FG_X_TO_SCREEN$QII
@PLAYFIELD_FG_X_TO_SCREEN$QII proc far
arg_fg_pid = word ptr 6
arg_fg_x = word ptr 8
 push bp
 mov bp, sp
 mov ax, [bp+arg_fg_x]
 mov bx, [bp+arg_fg_pid]
 sar ax, SUBPIXEL_BITS
 or bx, bx
 jz fg_shift
 add ax, PLAYFIELD_W_BORDERED
 mov bx, 2
fg_shift:
 add ax, _playfield_fg_shift_x[bx]
 add ax, PLAYFIELD_LEFT
 pop bp
 retf 4
@PLAYFIELD_FG_X_TO_SCREEN$QII endp
 even

public @SCREEN_X_TO_PLAYFIELD$QII
@SCREEN_X_TO_PLAYFIELD$QII proc far
arg_screen_pid = word ptr 6
arg_screen_x = word ptr 8
 push bp
 mov bp, sp
 mov bx, sp
 mov dx, [bp+arg_screen_pid]
 or dl, dl
 jz screen_origin_selected
 mov dx, PLAYFIELD_W_BORDERED
screen_origin_selected:
 mov ax, [bp+arg_screen_x]
 sub ax, dx
 add ax, -PLAYFIELD_BORDER
 shl ax, SUBPIXEL_BITS
 pop bp
 retf 4
@SCREEN_X_TO_PLAYFIELD$QII endp
 even

public @PLAYFIELD_CLIP$Q20%SUBPIXELBASE$TI$TI%T1
@PLAYFIELD_CLIP$Q20%SUBPIXELBASE$TI$TI%T1 proc far
arg_clip_y = word ptr 6
arg_clip_x = word ptr 8
 push bp
 mov bp, sp
 xor ax, ax
 mov cx, [bp+arg_clip_x]
 mov dx, [bp+arg_clip_y]
 mov bx, _playfield_clip_negative_radius
 cmp cx, bx
 jle clipped
 neg bx
 add bx, (PLAYFIELD_W shl SUBPIXEL_BITS)
 cmp cx, bx
 jge clipped
 mov bx, _playfield_clip_negative_radius+2
 cmp dx, bx
 jle clipped
 neg bx
 add bx, (PLAYFIELD_H shl SUBPIXEL_BITS)
 cmp dx, bx
 jl clip_result
clipped:
 mov al, 1
clip_result:
 pop bp
 retf 4
@PLAYFIELD_CLIP$Q20%SUBPIXELBASE$TI$TI%T1 endp
 even
PLAYFLD_TEXT ends
end
