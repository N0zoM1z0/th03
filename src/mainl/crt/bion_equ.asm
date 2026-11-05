; Complete original Japanese PC-98 BIOS equipment/memory/time helper.
; Queries the 8087, DOS mouse driver vector, physical NEC memory/option
; words and the original INT 1Ch service. Retains the original copyright
; signature in initialized DATA for the DOS 2.x mouse-driver comparison.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __necpc_bios_equiplist,__necpc_bios_memsize,__necpc_bios_timeofday
__necpc_bios_equiplist proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    push ds
    xor dx,dx
    fninit
    mov word ptr [bp-2],0
    fnstcw word ptr [bp-2]
    mov cx,5
fpu_cw_delay:
    loop fpu_cw_delay
    mov ax,[bp-2]
    and ax,0f3fh
    cmp ax,033fh
    jnz short skip_fpu_bit
    fnstsw word ptr [bp-2]
    mov cx,5
fpu_sw_delay:
    loop fpu_sw_delay
    test word ptr [bp-2],0b8bfh
    jnz short skip_fpu_bit
    or dx,2
skip_fpu_bit:
    xor ax,ax
    mov es,ax
    mov si,055ch
    mov ax,word ptr es:[si]
    xor cx,cx
count_equipment_bits:
    shr ax,1
    jnc short count_next
    pushf
    inc cx
    popf
count_next:
    jnz short count_equipment_bits
    shl cx,1
    shl cx,1
    shl cx,1
    or dx,cx
    mov ax,3533h
    int 21h
    mov ax,es
    or ax,bx
    jz short mouse_done
    mov ah,30h
    int 21h
    cmp al,3
    jnc short call_mouse
    sub bx,40
    mov si,offset DGROUP:microsoft_signature
    cld
signature_next:
    lodsb
    or al,al
    jz short call_mouse
    cmp al,byte ptr es:[bx]
    jnz short mouse_done
    inc bx
    jmp short signature_next
call_mouse:
    xor ax,ax
    int 33h
    or ax,ax
    jz short mouse_done
    or dx,0100h
mouse_done:
    mov ax,0a000h
    mov es,ax
    mov si,03feeh
    mov ax,word ptr es:[si]
    test al,20h
    jz short equipment_other
    or dx,1000h
equipment_other:
    test al,8
    jz short extra_memory
    or dx,2000h
extra_memory:
    mov ah,1
    test al,10h
    jz short memory_units_ready
    mov ax,0d000h
    mov es,ax
    mov si,0800h
    mov al,byte ptr es:[si]
    mov ah,1
    cmp al,0ffh
    jz short memory_units_ready
    add ah,al
memory_units_ready:
    and ax,0700h
    shl ax,1
    or dx,ax
    or dx,4000h
    mov ax,dx
    pop ds
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__necpc_bios_equiplist endp

__necpc_bios_memsize proc far
    push si
    push di
    mov ax,0a000h
    mov es,ax
    mov bx,03feah
    mov al,byte ptr es:[bx]
    and ax,7
    inc ax
    mov cl,7
    shl ax,cl
    pop di
    pop si
    retf
__necpc_bios_memsize endp

__necpc_bios_timeofday proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+8]
    mov ax,[bp+6]
    xchg ah,al
    cmp ah,1
    jna short bios_time_call
    mov ax,0ffffh
    jmp short bios_time_done
bios_time_call:
    int 1ch
    xor ax,ax
bios_time_done:
    pop di
    pop si
    pop bp
    retf
__necpc_bios_timeofday endp
_TEXT ends
_DATA segment word public 'DATA'
microsoft_signature db '*** This is Copyright 1983 Microsoft ***',0
_DATA ends
end
