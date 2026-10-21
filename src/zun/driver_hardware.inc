; Only hardware definitions consumed by the maintained ZUN driver.
; Preserve register-write order and unconditional CLI/STI behavior in callers.
outw macro port:req, value:rest
    mov dx, port
    mov ax, value
    out dx, ax
endm
GRCG_SETMODE_VIA_MOV macro value_reg:req, mode:req
    mov value_reg, mode
    out 7Ch, value_reg
endm
GRCG_OFF_VIA_XOR macro value_reg:req
    xor value_reg, value_reg
    out 7Ch, value_reg
endm
graph_mode_change macro enable_or_disable:req
    mov al, (6 + enable_or_disable)
    out 6Ah, al
endm
graph_mode_egc macro enable_or_disable:req
    mov al, (4 + enable_or_disable)
    out 6Ah, al
endm
graph_egc macro enable_or_disable:req
    graph_mode_change 1
    graph_mode_egc enable_or_disable
    graph_mode_change 0
endm
GC_TDW equ 080h
EGC_ACTIVEPLANEREG equ 04A0h
EGC_READPLANEREG equ 04A2h
EGC_MODE_ROP_REG equ 04A4h
EGC_FGCOLORREG equ 04A6h
EGC_MASKREG equ 04A8h
; Keep the historical spelling because maintained procedure operands use it.
EGC_ADDRRESSREG equ 04ACh
EGC_BITLENGTHREG equ 04AEh
EGC_COMPAREREAD equ 02000h
EGC_WS_ROP equ 00800h
EGC_SHIFT_CPU equ 00400h
