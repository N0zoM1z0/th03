; Eight successive right-shift masks for BYTE-wide pixel operations.
public BYTE_MASK
BYTE_MASK label byte
byte_mask_bits = 0ffh
REPT 8
    DB byte_mask_bits
    byte_mask_bits = byte_mask_bits SHR 1
ENDM
