; TH03 ZUN -4 resident service setters, AH=3..8.
; Included inside the driver's existing use16 _TEXT segment.
; DX is the value. MOV/near RET preserve flags and all general registers.
; The containing driver owns the six WORD state symbols and their layout.
; No allocations, interrupt masking, hardware access, padding, or data here.

public sprite16_set_mono_enabled
sprite16_set_mono_enabled proc near
    mov cs:sprite16_mono_enabled, dx
    retn
sprite16_set_mono_enabled endp

public sprite16_set_mono_color
sprite16_set_mono_color proc near
    mov cs:sprite16_mono_color, dx
    retn
sprite16_set_mono_color endp

public sprite16_set_overlap
sprite16_set_overlap proc near
    mov cs:sprite16_overlap, dx
    retn
sprite16_set_overlap endp

public sprite16_set_access_plane
sprite16_set_access_plane proc near
    mov cs:sprite16_access_plane, dx
    retn
sprite16_set_access_plane endp

public sprite16_set_rop
sprite16_set_rop proc near
    mov cs:sprite16_rop, dx
    retn
sprite16_set_rop endp

public sprite16_set_mask
sprite16_set_mask proc near
    mov cs:sprite16_mask, dx
    retn
sprite16_set_mask endp
