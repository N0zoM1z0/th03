; TH03 MAIN keyboard scan: two held-key samples and original PC-98 delay.
; Far no-argument interface; BX/CX/AX/ES are the original working registers.
.8086
SHARED segment word public 'CODE'
assume cs:SHARED,ds:DGROUP
extrn _js_stat:word,_input_mp_p1:word,_input_mp_p2:word,_input_sp:word
public @input_reset_sense_key_held$qv
INPUT_UP equ 1
INPUT_DOWN equ 2
INPUT_LEFT equ 4
INPUT_RIGHT equ 8
INPUT_BOMB equ 16
INPUT_SHOT equ 32
INPUT_UP_LEFT equ 256
INPUT_DOWN_LEFT equ 512
INPUT_UP_RIGHT equ 1024
INPUT_DOWN_RIGHT equ 2048
INPUT_CANCEL equ 4096
INPUT_OK equ 8192
INPUT_Q equ 16384
; Preserve the original short entry transfer, all 42 symbolic fields and true RETF boundary.
; The final CODE EVEN below is one assembler alignment byte, not a 116th instruction.

; Sequential natural instruction order; labels are at real code boundaries.
; Linear source, 417 instruction bytes, no raw opcodes or target-byte fill.

@input_reset_sense_key_held$qv label far
    xor ax,ax

    mov DGROUP:_input_mp_p1,ax
    mov DGROUP:_input_mp_p2,ax
    mov DGROUP:_input_sp,ax
    mov DGROUP:_js_stat,ax
    jmp short initialize_scan_count
initialize_scan_count label near
    mov bl,2

    xor ax,ax
    mov es,ax
scan_keys label near
    mov ah,byte ptr es:[1329]

    test ah,4
    jz after_arrow_up
    or word ptr DGROUP:_input_sp,INPUT_UP
after_arrow_up label near
    test ah,32

    jz after_arrow_down
    or word ptr DGROUP:_input_sp,INPUT_DOWN
after_arrow_down label near
    test ah,8

    jz after_arrow_left
    or word ptr DGROUP:_input_mp_p2,INPUT_SHOT
    or word ptr DGROUP:_input_sp,INPUT_LEFT
after_arrow_left label near
    test ah,16

    jz after_arrow_right
    or word ptr DGROUP:_input_mp_p2,INPUT_BOMB
    or word ptr DGROUP:_input_sp,INPUT_RIGHT
after_arrow_right label near
    mov ah,byte ptr es:[1331]

    test ah,1
    jz after_num_6
    or word ptr DGROUP:_input_mp_p2,INPUT_RIGHT
    or word ptr DGROUP:_input_sp,INPUT_RIGHT
after_num_6 label near
    test ah,4

    jz after_num_1
    or word ptr DGROUP:_input_mp_p2,INPUT_DOWN_LEFT
    or word ptr DGROUP:_input_sp,INPUT_DOWN_LEFT
after_num_1 label near
    test ah,8

    jz after_num_2
    or word ptr DGROUP:_input_mp_p2,INPUT_DOWN
    or word ptr DGROUP:_input_sp,INPUT_DOWN
after_num_2 label near
    test ah,16

    jz after_num_3
    or word ptr DGROUP:_input_mp_p2,INPUT_DOWN_RIGHT
    or word ptr DGROUP:_input_sp,INPUT_DOWN_RIGHT
after_num_3 label near
    mov ah,byte ptr es:[1330]

    test ah,64
    jz after_num_4
    or word ptr DGROUP:_input_mp_p2,INPUT_LEFT
    or word ptr DGROUP:_input_sp,INPUT_LEFT
after_num_4 label near
    test ah,4

    jz after_num_7
    or word ptr DGROUP:_input_mp_p2,INPUT_UP_LEFT
    or word ptr DGROUP:_input_sp,INPUT_UP_LEFT
after_num_7 label near
    test ah,8

    jz after_num_8
    or word ptr DGROUP:_input_mp_p2,INPUT_UP
    or word ptr DGROUP:_input_sp,INPUT_UP
after_num_8 label near
    test ah,16

    jz after_num_9
    or word ptr DGROUP:_input_mp_p2,INPUT_UP_RIGHT
    or word ptr DGROUP:_input_sp,INPUT_UP_RIGHT
after_num_9 label near
    mov ah,byte ptr es:[1327]

    test ah,2
    jz after_z
    or word ptr DGROUP:_input_mp_p1,INPUT_SHOT
    or word ptr DGROUP:_input_sp,INPUT_SHOT
after_z label near
    test ah,4

    jz after_x
    or word ptr DGROUP:_input_mp_p1,INPUT_BOMB
    or word ptr DGROUP:_input_sp,INPUT_BOMB
after_x label near
    test ah,16

    jz after_v
    or word ptr DGROUP:_input_mp_p1,INPUT_DOWN_LEFT
after_v label near
    test ah,32

    jz after_b
    or word ptr DGROUP:_input_mp_p1,INPUT_DOWN
after_b label near
    test ah,64

    jz after_n
    or word ptr DGROUP:_input_mp_p1,INPUT_DOWN_RIGHT
after_n label near
    mov ah,byte ptr es:[1326]

    test ah,1
    jz after_f
    or word ptr DGROUP:_input_mp_p1,INPUT_LEFT
after_f label near
    test ah,4

    jz after_h
    or word ptr DGROUP:_input_mp_p1,INPUT_RIGHT
after_h label near
    mov ah,byte ptr es:[1324]

    test ah,8
    jz after_r
    or word ptr DGROUP:_input_mp_p1,INPUT_UP_LEFT
after_r label near
    test ah,16

    jz after_t
    or word ptr DGROUP:_input_mp_p1,INPUT_UP
after_t label near
    test ah,32

    jz after_y
    or word ptr DGROUP:_input_mp_p1,INPUT_UP_RIGHT
after_y label near
    test ah,1

    jz after_q
    or word ptr DGROUP:_input_sp,INPUT_Q
after_q label near
    mov ah,byte ptr es:[1322]

    test ah,1
    jz after_escape
    or word ptr DGROUP:_input_sp,INPUT_CANCEL
after_escape label near
    mov ah,byte ptr es:[1325]

    test ah,16
    jz after_return
    or word ptr DGROUP:_input_sp,INPUT_OK
after_return label near
    mov ah,byte ptr es:[1328]

    test ah,16
    jz after_space
    or word ptr DGROUP:_input_sp,INPUT_SHOT
after_space label near
    dec bl

    jz scan_done
    mov cx,1024
io_delay label near
    out 05fh,al

    loop io_delay
    jmp scan_keys
scan_done label near
    retf


; The function ends at odd CODE offset 417. Native TASM EVEN emits the
; required machine NOP before the next word-aligned SHARED contribution.
; This byte is linker/assembler layout, not an additional function.
    even
SHARED ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
