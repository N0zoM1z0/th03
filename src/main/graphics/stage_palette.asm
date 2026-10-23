; Stage palette snapshots and the two player-color entries, MAIN A378..A3FA.
; Names are inferred. The four entries preserve their actual far ABIs.
.386
.model use16 large _TEXT
PALETTE_BYTES = 16 * 3
RGB_BYTES = 3
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
extrn Palettes:byte, palette_1F2F4:byte, _palette_changed:byte
_BSS ends
DGROUP group _DATA, _BSS
PLAYFLD_TEXT segment word public 'CODE' use16
PLAYFLD_TEXT ends
CFG_LRES_TEXT segment word public 'CODE' use16
CFG_LRES_TEXT ends
main_01 group PLAYFLD_TEXT, CFG_LRES_TEXT, HITCIRC_TEXT
extrn PALETTE_SHOW:far
HITCIRC_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP, es:nothing
public _stage_palette_backup, _stage_palette_show, _round_objects_for_next
public PALETTE_RESTORE_FOR_PID, BOMB_PALETTE_STEP

; DF=0. Copy all 16 RGB entries to the existing snapshot. No new storage.
_stage_palette_backup proc far
 push si
 push di
 mov ax, ds
 mov es, ax
 mov di, offset palette_1F2F4
 mov si, offset Palettes
 mov cx, PALETTE_BYTES / 4
 rep movsd
 pop di
 pop si
 retf
_stage_palette_backup endp
 even

; Restore the snapshot before invoking the existing palette output service.
_round_objects_for_next label far
_stage_palette_show proc far
 push si
 push di
 mov ax, ds
 mov es, ax
 mov di, offset Palettes
 mov si, offset palette_1F2F4
 mov cx, PALETTE_BYTES / 4
 rep movsd
 call far ptr PALETTE_SHOW
 pop di
 pop si
 retf
_stage_palette_show endp

; Far Pascal: byte PID in BP+6 word carrier; nonzero selects RGB entry 1.
PALETTE_RESTORE_FOR_PID proc far
 push bp
 mov bp, sp
 push si
 push di
 mov ax, ds
 mov es, ax
 xor bx, bx
 mov al, [bp+6]
 or al, al
 jz short restore_entry
 mov bl, RGB_BYTES
restore_entry:
 lea di, Palettes[bx]
 lea si, palette_1F2F4[bx]
 movsw
 movsb
 mov _palette_changed, 1
 pop di
 pop si
 pop bp
 retf 2
PALETTE_RESTORE_FOR_PID endp
 even

; Far Pascal: PID BP+6, channel byte BP+8; set all three selected RGB bytes.
BOMB_PALETTE_STEP proc far
 push bp
 mov bp, sp
 push di
 mov cx, RGB_BYTES
 xor bx, bx
 mov al, [bp+6]
 or al, al
 jz short fill_entry
 mov bl, RGB_BYTES
fill_entry:
 lea di, Palettes[bx]
 mov al, [bp+8]
fill_channel:
 mov [di], al
 inc di
 loop fill_channel
 mov _palette_changed, 1
 pop di
 pop bp
 retf 4
BOMB_PALETTE_STEP endp
HITCIRC_TEXT ends
end
