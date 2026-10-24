; TH03 ZUNSP (-4) tiny-model driver, UTF-8 LF.
; Nine native CODE contributions reproduce paragraph gaps through TLINK.
; Segment grouping is a proved compatible layout, not unique original source.
; No explicit zero fillers are used between the procedure groups.
.386
.model use16 tiny
include src\zun\driver_hardware.inc

; Paragraph CODE contributions share the actual tiny-model DGROUP.
SPR_MASK segment para public 'CODE' use16
SPR_MASK ends
SPR_PRINT segment para public 'CODE' use16
SPR_PRINT ends
SPR_FMT segment para public 'CODE' use16
SPR_FMT ends
SPR_CMD segment para public 'CODE' use16
SPR_CMD ends
SPR_NUM segment para public 'CODE' use16
SPR_NUM ends
SPR_EGC segment para public 'CODE' use16
SPR_EGC ends
SPR_STR segment para public 'CODE' use16
SPR_STR ends
SPR_DATA segment para public 'CODE' use16
SPR_DATA ends
DGROUP group SPR_MASK,SPR_PRINT,SPR_FMT,SPR_CMD,SPR_NUM,SPR_EGC,SPR_STR,SPR_DATA
_TEXT segment use16
assume cs:DGROUP
org 100h
assume es:nothing, ss:nothing, ds:DGROUP, fs:nothing, gs:nothing
public start
start:
    jmp short sprite16_entry
sprite16_signature db 'SPRITE16',0
sprite16_version db 4
include procs\sprite16_entry.inc
include procs\sprite16_allocate_buffers.inc
include procs\sprite16_set_interrupt_argument.inc
include procs\sprite16_mask_test_command.inc
include procs\sprite16_draw_command.inc
include procs\sprite16_interrupt_dispatch.inc
include procs\sprite16_install.inc
include procs\sprite16_uninstall.inc
include procs\sprite16_set_mono_enabled.inc
include procs\sprite16_set_mono_color.inc
include procs\sprite16_set_overlap.inc
include procs\sprite16_set_access_plane.inc
include procs\sprite16_set_rop.inc
include procs\sprite16_set_mask.inc
include procs\sprite16_draw_clipped.inc
include procs\sprite16_blit_egc.inc
; Preserve the native WORD boundary before the row-copy procedure.
even
include procs\sprite16_copy_rows.inc
_TEXT ends

SPR_MASK segment para public 'CODE' use16
assume cs:DGROUP
include procs\sprite16_prepare_vram.inc
include procs\sprite16_build_mask.inc
include procs\sprite16_accumulate_plane.inc
include procs\sprite16_copy_lower_page.inc
include procs\sprite16_compress_rows.inc
include procs\sprite16_copy_upper_to_lower.inc
include procs\sprite16_clear_upper.inc
SPR_MASK ends

SPR_PRINT segment para public 'CODE' use16
assume cs:DGROUP
include procs\sprite16_format_print.inc
include procs\sprite16_print_string.inc
include procs\sprite16_print_stack_string.inc
include procs\sprite16_is_decimal_digit.inc
include procs\sprite16_is_ascii_lower.inc
include procs\sprite16_ascii_upper.inc
SPR_PRINT ends

SPR_FMT segment para public 'CODE' use16
assume cs:DGROUP
include procs\sprite16_format_into.inc
include procs\sprite16_pad_zeroes.inc
include procs\sprite16_pad_spaces.inc
include procs\sprite16_pad_field.inc
include procs\sprite16_append_string.inc
include procs\sprite16_format_unsigned.inc
; Unsigned formatter indexes this non-NUL-terminated alphabet.
sprite16_hex_digits db '0123456789ABCDEF'
include procs\sprite16_reverse_string.inc
SPR_FMT ends

SPR_CMD segment para public 'CODE' use16
assume cs:DGROUP
include procs\sprite16_tokenize_command.inc
include procs\sprite16_skip_separators.inc
include procs\sprite16_find_token_end.inc
include procs\sprite16_find_quote_end.inc
include procs\sprite16_require_argument.inc
include procs\sprite16_optional_argument.inc
include procs\sprite16_require_number.inc
include procs\sprite16_optional_number_legacy.inc
include procs\sprite16_dispatch_options.inc
SPR_CMD ends

SPR_NUM segment para public 'CODE' use16
assume cs:DGROUP
include procs\sprite16_parse_number.inc
include procs\sprite16_parse_decimal.inc
include procs\sprite16_parse_hex.inc
include procs\sprite16_parse_binary.inc
include procs\sprite16_parse_switch.inc
SPR_NUM ends

SPR_EGC segment para public 'CODE' use16
assume cs:DGROUP
include procs\sprite16_egc_begin.inc
include procs\sprite16_egc_end.inc
SPR_EGC ends

SPR_STR segment para public 'CODE' use16
assume cs:DGROUP
include procs\sprite16_string_length.inc
include procs\sprite16_string_equal_folded.inc
SPR_STR ends

SPR_DATA segment para public 'CODE' use16
assume cs:DGROUP
include src\zun\driver_data.inl
SPR_DATA ends
end start
