; Complete TH03 MRS loading, blitting and horizontal reversal algorithms.
.386
extrn FILE_ROPEN:far, HMEM_ALLOCBYTE:far, FILE_READ:far, FILE_CLOSE:far
extrn HMEM_FREE:far, GRCG_SETCOLOR:far
extrn _mrs_images:dword, _hflip_lut:byte
MRS_W = 288
MRS_H = 184
BYTE_DOTS = 8
MRS_BYTE_W = MRS_W / BYTE_DOTS
MRS_DWORD_W = MRS_BYTE_W / 4
MRS_PLANE_BYTES = MRS_BYTE_W * MRS_H
MRS_BYTES = MRS_PLANE_BYTES * 5
ROW_SIZE = 80
SEG_PLANE_B = 0A800h
SEG_PLANE_DIST_BRG = 0800h
SEG_PLANE_DIST_E = 2800h
GC_RMW = 0C0h
GRCG_MODE_PORT = 7Ch
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
SHARED segment byte public 'CODE' use16
assume cs:SHARED, ds:DGROUP
public @MRS_LOAD$QINXC
@MRS_LOAD$QINXC proc far
 push bp
 mov bp, sp
 push dword ptr [bp+6]
 call FILE_ROPEN
 push MRS_BYTES
 call HMEM_ALLOCBYTE
 mov bx, [bp+10]
 shl bx, 2
 mov word ptr _mrs_images+2[bx], ax
 mov word ptr _mrs_images[bx], 0
 push dword ptr _mrs_images[bx]
 push MRS_BYTES
 call FILE_READ
 call FILE_CLOSE
 pop bp
 retf 6
@MRS_LOAD$QINXC endp
 even
public @MRS_FREE$QI
@MRS_FREE$QI proc far
 push bp
 mov bp, sp
 mov bx, [bp+6]
 shl bx, 2
 mov ax, word ptr _mrs_images+2[bx]
 ; Preserve the read of incoming DX and the OR-produced zero flag.
 or dx, word ptr _mrs_images[bx]
 or dx, ax
 jz free_return
 push ax
 call HMEM_FREE
 xor ax, ax
 mov word ptr _mrs_images+2[bx], ax
 mov word ptr _mrs_images[bx], ax
free_return:
 pop bp
 retf 2
@MRS_FREE$QI endp
 even
public @MRS_PUT_8$QIUII
@MRS_PUT_8$QIUII proc far
 push bp
 mov bp, sp
 push si
 push di
 push GC_RMW
 push 0
 call GRCG_SETCOLOR
 mov ax, [bp+10]
 sar ax, 3
 add ax, (MRS_H-1)*ROW_SIZE
 mov di, ax
 mov ax, [bp+8]
 shr ax, 1
 mov dx, ax
 shl ax, 2
 add ax, dx
 add ax, SEG_PLANE_B
 mov es, ax
 add ax, SEG_PLANE_DIST_BRG
 mov fs, ax
 add ax, SEG_PLANE_DIST_BRG
 mov gs, ax
 push ds
 mov bx, [bp+6]
 shl bx, 2
 lds si, _mrs_images[bx]
 mov dx, MRS_DWORD_W
 ; Word-align the alpha clearing loop with the assembler's normal directive.
 even
clear_alpha_rows:
 mov cx, dx
 rep movsd
 sub di, ROW_SIZE+MRS_BYTE_W
 jnc clear_alpha_rows
 xor al, al
 out GRCG_MODE_PORT, al
 xor si, si
 add di, MRS_H*ROW_SIZE
 mov ax, gs
 add ax, SEG_PLANE_DIST_E
 mov bx, ax
 mov dx, MRS_DWORD_W
put_alpha_rows:
 mov cx, dx
put_alpha_dword:
 mov eax, dword ptr [si]
 or eax, eax
 jz advance_alpha_dword
 mov eax, dword ptr [si+MRS_PLANE_BYTES]
 or es:[di], eax
 mov eax, dword ptr [si+MRS_PLANE_BYTES*2]
 or fs:[di], eax
 mov eax, dword ptr [si+MRS_PLANE_BYTES*3]
 or gs:[di], eax
 mov gs, bx
 mov eax, dword ptr [si+MRS_PLANE_BYTES*4]
 or gs:[di], eax
 mov ax, bx
 sub ax, SEG_PLANE_DIST_E
 mov gs, ax
advance_alpha_dword:
 add si, 4
 add di, 4
 loop put_alpha_dword
 sub di, ROW_SIZE+MRS_BYTE_W
 jnc put_alpha_rows
 pop ds
 pop di
 pop si
 pop bp
 retf 6
@MRS_PUT_8$QIUII endp
 even
public @MRS_PUT_NOALPHA_8$QIUIIUC
@MRS_PUT_NOALPHA_8$QIUIIUC proc far
 push bp
 mov bp, sp
 push si
 push di
 push ds
 mov ax, [bp+12]
 sar ax, 3
 add ax, (MRS_H-1)*ROW_SIZE
 mov di, ax
 mov ax, [bp+10]
 shr ax, 1
 mov dx, ax
 shl ax, 2
 add ax, dx
 mov bx, [bp+8]
 shl bx, 2
 lds si, _mrs_images[bx]
 mov si, MRS_PLANE_BYTES*3
 add ax, SEG_PLANE_B
 mov fs, ax
 add ax, SEG_PLANE_DIST_BRG
 mov gs, ax
 add ax, SEG_PLANE_DIST_BRG
 mov es, ax
 add ax, SEG_PLANE_DIST_E
 mov bx, ax
 mov dx, di
 cmp byte ptr [bp+6], 0
 jz put_regular_rows
put_altered_rows:
 mov cx, MRS_DWORD_W
put_altered_dword:
 mov eax, dword ptr [si-MRS_PLANE_BYTES*3]
 not eax
 or eax, dword ptr [si-MRS_PLANE_BYTES*2]
 mov fs:[di], eax
 mov eax, dword ptr [si-MRS_PLANE_BYTES]
 mov gs:[di], eax
 movsd
 loop put_altered_dword
 sub di, ROW_SIZE+MRS_BYTE_W
 jnc put_altered_rows
 mov di, dx
 mov es, bx
put_altered_e_rows:
 mov cx, MRS_DWORD_W
 rep movsd
 sub di, ROW_SIZE+MRS_BYTE_W
 jnc put_altered_e_rows
 jmp short put_noalpha_return
put_regular_rows:
 mov cx, MRS_DWORD_W
put_regular_dword:
 mov eax, dword ptr [si-MRS_PLANE_BYTES*2]
 mov fs:[di], eax
 mov eax, dword ptr [si-MRS_PLANE_BYTES]
 mov gs:[di], eax
 movsd
 loop put_regular_dword
 sub di, ROW_SIZE+MRS_BYTE_W
 jnc put_regular_rows
 mov di, dx
 mov es, bx
put_regular_e_rows:
 mov cx, MRS_DWORD_W
 rep movsd
 sub di, ROW_SIZE+MRS_BYTE_W
 jnc put_regular_e_rows
put_noalpha_return:
 pop ds
 pop di
 pop si
 pop bp
 retf 8
@MRS_PUT_NOALPHA_8$QIUIIUC endp
 even
public @MRS_HFLIP$QI
@MRS_HFLIP$QI proc far
 push bp
 mov bp, sp
 push si
 push di
 mov cx, MRS_BYTES
 mov bx, [bp+6]
 shl bx, 2
 les di, _mrs_images[bx]
 mov bx, offset _hflip_lut
flip_dots:
 mov al, es:[di]
 xlat
 mov es:[di], al
 inc di
 loop flip_dots
 mov cx, MRS_BYTES/MRS_BYTE_W
 xor bx, bx
flip_rows:
 xor di, di
 mov si, MRS_BYTE_W-1
flip_row_bytes:
 mov al, es:[bx+di]
 mov dl, es:[bx+si]
 mov es:[bx+si], al
 mov es:[bx+di], dl
 dec si
 inc di
 cmp di, (MRS_BYTE_W/2)-1
 jbe flip_row_bytes
 add bx, MRS_BYTE_W
 loop flip_rows
 pop di
 pop si
 pop bp
 retf 2
@MRS_HFLIP$QI endp
 even
SHARED ends
end
