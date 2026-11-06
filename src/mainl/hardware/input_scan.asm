; MAINL PC-98 keyboard scan: two held-key samples with the original delay.
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
; No trailing NOP or alignment byte belongs to this instruction scope.
org 0
@input_reset_sense_key_held$qv label far
org 16
initialize_scan_count label near
org 22
scan_keys label near
org 37
after_arrow_up label near
org 47
after_arrow_down label near
org 62
after_arrow_left label near
org 77
after_arrow_right label near
org 97
after_num_6 label near
org 114
after_num_1 label near
org 129
after_num_2 label near
org 146
after_num_3 label near
org 166
after_num_4 label near
org 183
after_num_7 label near
org 198
after_num_8 label near
org 215
after_num_9 label near
org 235
after_z label near
org 250
after_x label near
org 261
after_v label near
org 271
after_b label near
org 282
after_n label near
org 297
after_f label near
org 307
after_h label near
org 323
after_r label near
org 333
after_t label near
org 344
after_y label near
org 355
after_q label near
org 371
after_escape label near
org 387
after_return label near
org 402
after_space label near
org 409
io_delay label near
org 416
scan_done label near

; Original instruction bytes 0..1.
org 0
    xor ax,ax

; Original instruction bytes 397..416.
org 397
    or word ptr DGROUP:_input_sp,INPUT_SHOT
    dec bl
    jz scan_done
    mov cx,1024
    out 05fh,al
    loop io_delay
    jmp scan_keys
    retf

; Original instruction bytes 381..396.
org 381
    or word ptr DGROUP:_input_sp,INPUT_OK
    mov ah,byte ptr es:[1328]
    test ah,16
    jz after_space

; Original instruction bytes 365..380.
org 365
    or word ptr DGROUP:_input_sp,INPUT_CANCEL
    mov ah,byte ptr es:[1325]
    test ah,16
    jz after_return

; Original instruction bytes 349..364.
org 349
    or word ptr DGROUP:_input_sp,INPUT_Q
    mov ah,byte ptr es:[1322]
    test ah,1
    jz after_escape

; Original instruction bytes 338..348.
org 338
    or word ptr DGROUP:_input_mp_p1,INPUT_UP_RIGHT
    test ah,1
    jz after_q

; Original instruction bytes 328..337.
org 328
    or word ptr DGROUP:_input_mp_p1,INPUT_UP
    test ah,32
    jz after_y

; Original instruction bytes 317..327.
org 317
    or word ptr DGROUP:_input_mp_p1,INPUT_UP_LEFT
    test ah,16
    jz after_t

; Original instruction bytes 302..316.
org 302
    or word ptr DGROUP:_input_mp_p1,INPUT_RIGHT
    mov ah,byte ptr es:[1324]
    test ah,8
    jz after_r

; Original instruction bytes 292..301.
org 292
    or word ptr DGROUP:_input_mp_p1,INPUT_LEFT
    test ah,4
    jz after_h

; Original instruction bytes 276..291.
org 276
    or word ptr DGROUP:_input_mp_p1,INPUT_DOWN_RIGHT
    mov ah,byte ptr es:[1326]
    test ah,1
    jz after_f

; Original instruction bytes 266..275.
org 266
    or word ptr DGROUP:_input_mp_p1,INPUT_DOWN
    test ah,64
    jz after_n

; Original instruction bytes 255..265.
org 255
    or word ptr DGROUP:_input_mp_p1,INPUT_DOWN_LEFT
    test ah,32
    jz after_b

; Original instruction bytes 245..254.
org 245
    or word ptr DGROUP:_input_sp,INPUT_BOMB
    test ah,16
    jz after_v

; Original instruction bytes 240..244.
org 240
    or word ptr DGROUP:_input_mp_p1,INPUT_BOMB

; Original instruction bytes 230..239.
org 230
    or word ptr DGROUP:_input_sp,INPUT_SHOT
    test ah,4
    jz after_x

; Original instruction bytes 225..229.
org 225
    or word ptr DGROUP:_input_mp_p1,INPUT_SHOT

; Original instruction bytes 209..224.
org 209
    or word ptr DGROUP:_input_sp,INPUT_UP_RIGHT
    mov ah,byte ptr es:[1327]
    test ah,2
    jz after_z

; Original instruction bytes 203..208.
org 203
    or word ptr DGROUP:_input_mp_p2,INPUT_UP_RIGHT

; Original instruction bytes 193..202.
org 193
    or word ptr DGROUP:_input_sp,INPUT_UP
    test ah,16
    jz after_num_9

; Original instruction bytes 188..192.
org 188
    or word ptr DGROUP:_input_mp_p2,INPUT_UP

; Original instruction bytes 177..187.
org 177
    or word ptr DGROUP:_input_sp,INPUT_UP_LEFT
    test ah,8
    jz after_num_8

; Original instruction bytes 171..176.
org 171
    or word ptr DGROUP:_input_mp_p2,INPUT_UP_LEFT

; Original instruction bytes 161..170.
org 161
    or word ptr DGROUP:_input_sp,INPUT_LEFT
    test ah,4
    jz after_num_7

; Original instruction bytes 156..160.
org 156
    or word ptr DGROUP:_input_mp_p2,INPUT_LEFT

; Original instruction bytes 140..155.
org 140
    or word ptr DGROUP:_input_sp,INPUT_DOWN_RIGHT
    mov ah,byte ptr es:[1330]
    test ah,64
    jz after_num_4

; Original instruction bytes 134..139.
org 134
    or word ptr DGROUP:_input_mp_p2,INPUT_DOWN_RIGHT

; Original instruction bytes 124..133.
org 124
    or word ptr DGROUP:_input_sp,INPUT_DOWN
    test ah,16
    jz after_num_3

; Original instruction bytes 119..123.
org 119
    or word ptr DGROUP:_input_mp_p2,INPUT_DOWN

; Original instruction bytes 108..118.
org 108
    or word ptr DGROUP:_input_sp,INPUT_DOWN_LEFT
    test ah,8
    jz after_num_2

; Original instruction bytes 102..107.
org 102
    or word ptr DGROUP:_input_mp_p2,INPUT_DOWN_LEFT

; Original instruction bytes 92..101.
org 92
    or word ptr DGROUP:_input_sp,INPUT_RIGHT
    test ah,4
    jz after_num_1

; Original instruction bytes 87..91.
org 87
    or word ptr DGROUP:_input_mp_p2,INPUT_RIGHT

; Original instruction bytes 72..86.
org 72
    or word ptr DGROUP:_input_sp,INPUT_RIGHT
    mov ah,byte ptr es:[1331]
    test ah,1
    jz after_num_6

; Original instruction bytes 67..71.
org 67
    or word ptr DGROUP:_input_mp_p2,INPUT_BOMB

; Original instruction bytes 57..66.
org 57
    or word ptr DGROUP:_input_sp,INPUT_LEFT
    test ah,16
    jz after_arrow_right

; Original instruction bytes 52..56.
org 52
    or word ptr DGROUP:_input_mp_p2,INPUT_SHOT

; Original instruction bytes 42..51.
org 42
    or word ptr DGROUP:_input_sp,INPUT_DOWN
    test ah,8
    jz after_arrow_left

; Original instruction bytes 32..41.
org 32
    or word ptr DGROUP:_input_sp,INPUT_UP
    test ah,32
    jz after_arrow_down

; Original instruction bytes 11..31.
org 11
    mov DGROUP:_js_stat,ax
    jmp short initialize_scan_count
    mov bl,2
    xor ax,ax
    mov es,ax
    mov ah,byte ptr es:[1329]
    test ah,4
    jz after_arrow_up

; Original instruction bytes 8..10.
org 8
    mov DGROUP:_input_sp,ax

; Original instruction bytes 5..7.
org 5
    mov DGROUP:_input_mp_p2,ax

; Original instruction bytes 2..4.
org 2
    mov DGROUP:_input_mp_p1,ax
SHARED ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
