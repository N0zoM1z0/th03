; Original Japanese Borland crtinit: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn ___nec_c0crtinit:near
extrn ___nec_get_screen_height:far
extrn ___nec_get_windowy2:far
extrn ___ibm_c0crtinit:near
extrn ___ibm_get_screen_height:far
extrn ___ibm_get_windowy2:far
extrn ___conio_type:word
extrn ___conio_type_init:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _DATA,_BSS
_DATA segment word public 'DATA'
public __video
public __directvideo
__video label byte
video_window_left db 0
video_window_top db 0
video_window_right db 0
video_window_bottom db 0
video_saved_word4 dw 0
video_saved_word6 dw 0
video_mode db 0
video_height db 0
video_width db 0
video_graphics db 0
video_state_word12 dw 0
video_hardware_flags dw 0
video_vram dd 0
__directvideo dw 1
_DATA ends
_INIT_ segment word public 'INITDATA'
; Native far startup record: kind, priority, offset and segment.
db 0,16
dd __c0crtinit
_INIT_ ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __c0crtinit
public ___get_screen_height
public ___get_windowy2
; Complete disjoint instruction chunks follow original OMF field chronology.

org 2
    call ___conio_type_init

org 5
    cmp word ptr DGROUP:___conio_type, 2
    jne short initialize_ibm

org 12
    call ___nec_c0crtinit
    jmp short initialize_return

org 17
initialize_ibm:
    cmp word ptr DGROUP:___conio_type, 1
    jne short initialize_return

org 24
    call ___ibm_c0crtinit
initialize_return:
    pop di
    pop si
    ret
___get_screen_height label far
    push si
    push di

org 32
    cmp word ptr DGROUP:___conio_type, 2
    jne short height_ibm

org 39
    call ___nec_get_screen_height
    jmp short height_return

org 46
height_ibm:
    cmp word ptr DGROUP:___conio_type, 1
    jne short height_cached

org 53
    call ___ibm_get_screen_height
    jmp short height_return

org 70
    cmp word ptr DGROUP:___conio_type, 2
    jne short window_ibm

org 77
    call ___nec_get_windowy2
    jmp short window_return

org 84
window_ibm:
    cmp word ptr DGROUP:___conio_type, 1
    jne short window_cached

org 91
    call ___ibm_get_windowy2
    jmp short window_return

org 60
height_cached:
    mov al, byte ptr DGROUP:video_height
    mov ah, 0
height_return:
    pop di
    pop si
    retf
___get_windowy2 label far
    push si
    push di

org 98
window_cached:
    mov al, byte ptr DGROUP:video_window_bottom
    mov ah, 0
window_return:
    pop di
    pop si
    retf

org 0
__c0crtinit label near
    push si
    push di
_TEXT ends
end
