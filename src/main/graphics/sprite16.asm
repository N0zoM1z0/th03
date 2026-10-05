; TH03 MAIN complete sprite16 wrapper algorithms with natural word alignment.
.386
extrn SPRITE16_SPRITES_COPY_PAGE:far
extrn _sprite16_clip:word
extrn _sprite16_put_size:word
SPRITE16 = 42h
SPRITE16_GENERATE_ALPHA = 1
SPRITE16_SERVICE_PUT = 2
SPRITE16_RES_Y = 200
PIXELS_PER_WORD = 16
BYTES_PER_WORD = 2
GRAPH_ACCESS_PORT = 0A6h
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
SHARED segment byte public 'CODE' use16
assume cs:SHARED, ds:DGROUP
public SPRITE16_SPRITES_COMMIT
SPRITE16_SPRITES_COMMIT proc far
 push 1
 call SPRITE16_SPRITES_COPY_PAGE
 mov dx, GRAPH_ACCESS_PORT
 mov al, 0
 out dx, al
 mov ah, SPRITE16_GENERATE_ALPHA
 int SPRITE16
 retf
SPRITE16_SPRITES_COMMIT endp
 even
public SPRITE16_PUT
SPRITE16_PUT proc far
arg_so = word ptr 6
arg_top = word ptr 8
arg_left = word ptr 10
 push bp
 mov bp, sp
 push si
 push di
 mov di, [bp+arg_so]
 mov dx, [bp+arg_left]
 mov al, byte ptr _sprite16_put_size+2
 xor bh, bh
 mov bl, al
 shl bx, 4
 add bx, dx
 mov si, _sprite16_clip
 mov cx, _sprite16_clip+2
 cmp bx, cx
 jge put_clip_right
 cmp dx, si
 jl put_clip_left
put_draw:
 mov ah, SPRITE16_SERVICE_PUT
 mov bx, [bp+arg_top]
 sar bx, 1
 mov cx, _sprite16_put_size
 int SPRITE16
 jmp short put_return
put_clip_left:
 cmp bx, si
 jl put_return
put_left_word:
 add dx, PIXELS_PER_WORD
 dec al
 jz put_return
 add di, BYTES_PER_WORD
 cmp dx, si
 jl put_left_word
 jmp short put_draw
put_clip_right:
 cmp dx, cx
 jge put_return
put_right_word:
 sub bx, PIXELS_PER_WORD
 dec al
 jz put_return
 cmp bx, cx
 jge put_right_word
 jmp short put_draw
put_return:
 pop di
 pop si
 pop bp
 retf 6
SPRITE16_PUT endp
 even
public SPRITE16_PUTX
SPRITE16_PUTX proc far
arg_x_func = word ptr 6
arg_x_so = word ptr 8
arg_x_top = word ptr 10
arg_x_left = word ptr 12
 push bp
 mov bp, sp
 push si
 push di
 mov di, [bp+arg_x_so]
 mov dx, [bp+arg_x_left]
 mov al, byte ptr _sprite16_put_size+2
 xor bh, bh
 mov bl, al
 shl bx, 4
 add bx, dx
 mov si, _sprite16_clip
 mov cx, _sprite16_clip+2
 cmp bx, cx
 jge putx_clip_right
 cmp dx, si
 jl putx_clip_left
putx_draw:
 mov ah, SPRITE16_SERVICE_PUT
 mov bx, [bp+arg_x_top]
 sar bx, 1
 mov cx, _sprite16_put_size
putx_column:
 mov si, [bp+arg_x_func]
 int SPRITE16
 dec si
 jz putx_return
 add bx, cx
 cmp bx, SPRITE16_RES_Y
 jge putx_return
 jmp short putx_column
putx_clip_left:
 cmp bx, si
 jl putx_return
putx_left_word:
 add dx, PIXELS_PER_WORD
 dec al
 jz putx_return
 add di, BYTES_PER_WORD
 cmp dx, si
 jl putx_left_word
 jmp short putx_draw
putx_clip_right:
 cmp dx, cx
 jge putx_return
putx_right_word:
 sub bx, PIXELS_PER_WORD
 dec al
 jz putx_return
 cmp bx, cx
 jge putx_right_word
 jmp short putx_draw
putx_return:
 pop di
 pop si
 pop bp
 retf 8
SPRITE16_PUTX endp
 even
public SPRITE16_PUT_NOCLIP
SPRITE16_PUT_NOCLIP proc far
 push bp
 mov bp, sp
 push di
 mov di, [bp+arg_so]
 mov dx, [bp+arg_left]
 ; Preserve the target's read of incoming AL in the discarded right edge.
 xor bh, bh
 mov bl, al
 shl bx, 4
 add bx, dx
 mov ah, SPRITE16_SERVICE_PUT
 mov bx, [bp+arg_top]
 sar bx, 1
 mov al, byte ptr _sprite16_put_size+2
 mov cx, _sprite16_put_size
 int SPRITE16
 pop di
 pop bp
 retf 6
SPRITE16_PUT_NOCLIP endp
 even
SHARED ends
end
