; Diagnostic entry to MAINL using the resident installed by GAME.BAT.
bits 16
org 100h

    mov ax, 3d00h
    mov dx, cfg_name
    int 21h
    jc fail
    mov bx, ax
    mov cx, 8
    mov dx, cfg
    mov ah, 3fh
    int 21h
    jc fail
    cmp ax, 8
    jne fail
    mov ah, 3eh
    int 21h
    jc fail
    mov ax, [cfg+5]
    test ax, ax
    jz fail
    mov es, ax
    cmp dword [es:0], 'YUME'
    jne fail
    cmp dword [es:4], 'Conf'
    jne fail
    cmp word [es:8], 'ig'
    jne fail

    mov byte [es:11], 0      ; rank: Easy
    mov word [es:12], 1101h  ; Reimu and Yumemi, unpaletted
    mov word [es:14], 0100h  ; human winner, CPU opponent
    mov dword [es:16], 600   ; deterministic score encryption seed
    mov al, [cfg]
    mov [es:21], al          ; use the original BGM setting
    mov byte [es:23], 0      ; winner
    mov dword [es:24], 05060708h
    mov dword [es:28], 01020304h
    mov byte [es:40], 1      ; Story
    mov byte [es:51], STAGE
    mov byte [es:53], SCORE_ONLY
    mov byte [es:54], 0      ; no continue or optional 1CC scene

    mov ax, cs
    mov es, ax
    mov bx, (program_end - $$ + 100h + 15) / 16
    mov ah, 4ah
    int 21h
    jc fail
    mov ax, cs
    mov [exec_block+4], ax
    mov [exec_block+8], ax
    mov [exec_block+12], ax
    mov bx, exec_block
    mov dx, mainl_name
    mov ax, 4b00h
    int 21h
    jc fail
    mov ax, 4c00h
    int 21h

fail:
    mov dx, failure
    mov ah, 9
    int 21h
    mov ax, 4c01h
    int 21h

cfg_name db 'YUME.CFG', 0
cfg times 8 db 0
mainl_name db 'MAINL.EXE', 0
failure db 'PI fixture: DOS error or invalid YUMEConfig resident', 13, 10, '$'
empty_tail db 0, 13
exec_block dw 0, empty_tail, 0, 5ch, 0, 6ch, 0
program_end:
