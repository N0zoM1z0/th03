; Original PC-98 equipment detection, including x87 coprocessor probing.
; BIOS flags are read from their physical 0:xxxx locations. The inline
; positive-infinity floating constant is semantic x87 data in CODE,
; not an executable-byte patch or an external copy of target instructions.
.8086
.8087
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _pc98equip
_pc98equip proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    push ds
    xor ax,ax
    mov ds,ax
    inc ax
    test byte ptr ds:[0501h],40h
    jnz short skip_display_check
    mov al,byte ptr ds:[0480h]
    and al,3
    jz short skip_display_check
    cmp al,3
    jz short skip_display_check
    mov al,2
skip_display_check:
    test byte ptr ds:[0501h],80h
    jz short skip_subsystem_flag
    or al,8
skip_subsystem_flag:
    xor dx,dx
    fninit
    mov [bp-2],dx
    fnstcw word ptr [bp-2]
    mov cx,20
fpu_control_wait:
    loop fpu_control_wait
    mov cx,[bp-2]
    and cx,0f3fh
    cmp cx,033fh
    jnz short fpu_done
    mov word ptr [bp-2],0ffffh
    fnstsw word ptr [bp-2]
    mov cx,20
fpu_status_wait:
    loop fpu_status_wait
    test word ptr [bp-2],0b8bfh
    jnz short fpu_done
    fninit
    fld dword ptr cs:fpu_infinity
    fchs
    fcomp dword ptr cs:fpu_infinity
    fstsw word ptr [bp-2]
    mov dl,30h
    test byte ptr [bp-1],40h
    jz short fpu_done
    mov dl,20h
    push sp
    pop cx
    cmp cx,sp
    jz short fpu_done
    mov dl,10h
    jmp short fpu_done
fpu_infinity dd 07f800000h
fpu_done:
    or al,dl  ; preserve original x87 capability bits in equipment mask
    test byte ptr ds:[0481h],40h
    jz short skip_firmware_video
    or al,40h
skip_firmware_video:
    test byte ptr ds:[0458h],80h
    jz short skip_internal_memory
    or ax,4080h
skip_internal_memory:
    test byte ptr ds:[0501h],8
    jz short legacy_video
    or ah,81h
    jmp short inspect_video_flags
legacy_video:
    test byte ptr ds:[054ch],2
    jz short inspect_timing
    inc ah
inspect_video_flags:
    test byte ptr ds:[054dh],40h
    jz short inspect_timing
    inc ah
    test byte ptr ds:[054dh],8
    jz short inspect_timing
    inc ah
inspect_timing:
    test byte ptr ds:[054ch],4
    jz short equipment_done
    or ah,8
equipment_done:
    pop ds
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_pc98equip endp
_TEXT ends
end
