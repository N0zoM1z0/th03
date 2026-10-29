; Seventeen cumulative pixel masks in PC-98 little-endian VRAM order.
public EDGES
EDGES label word
edge_bits = 0
REPT 17
    DW ((edge_bits AND 0ffh) SHL 8) OR (edge_bits SHR 8)
    edge_bits = (edge_bits SHR 1) OR 8000h
ENDM
