; TH03 ZUNSP (-4) standalone driver layout, UTF-8 LF.
; All procedures come from maintained logical modules, staged as individual includes.
; Zero spans below are exact source-recorded reserved regions. Their original
; purpose is not established: no inferred ALIGN rule or fitted target padding.
.386
.model use16 tiny
include src\zun\driver_hardware.inc
_TEXT segment use16
assume cs:_TEXT
org 100h
assume es:nothing, ss:nothing, ds:_TEXT, fs:nothing, gs:nothing
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
; Source-recorded interprocedure NOP at 04F7h.
nop
include procs\sprite16_copy_rows.inc
; Source-recorded reserved region 0516h..0520h (end exclusive).
layout_reserved_before_prepare_vram db 10 dup(0)
include procs\sprite16_prepare_vram.inc
include procs\sprite16_build_mask.inc
include procs\sprite16_accumulate_plane.inc
include procs\sprite16_copy_lower_page.inc
include procs\sprite16_compress_rows.inc
include procs\sprite16_copy_upper_to_lower.inc
include procs\sprite16_clear_upper.inc
; Source-recorded reserved region 0631h..0640h (end exclusive).
layout_reserved_before_format_print db 15 dup(0)
include procs\sprite16_format_print.inc
include procs\sprite16_print_string.inc
include procs\sprite16_print_stack_string.inc
include procs\sprite16_is_decimal_digit.inc
include procs\sprite16_is_ascii_lower.inc
include procs\sprite16_ascii_upper.inc
; Source-recorded reserved region 06A5h..06B0h (end exclusive).
layout_reserved_before_format_into db 11 dup(0)
include procs\sprite16_format_into.inc
include procs\sprite16_pad_zeroes.inc
include procs\sprite16_pad_spaces.inc
include procs\sprite16_pad_field.inc
include procs\sprite16_append_string.inc
include procs\sprite16_format_unsigned.inc
; Unsigned formatter indexes this non-NUL-terminated alphabet.
sprite16_hex_digits db '0123456789ABCDEF'
include procs\sprite16_reverse_string.inc
; Source-recorded reserved region 091Ch..0920h (end exclusive).
layout_reserved_before_tokenize_command db 4 dup(0)
include procs\sprite16_tokenize_command.inc
include procs\sprite16_skip_separators.inc
include procs\sprite16_find_token_end.inc
include procs\sprite16_find_quote_end.inc
include procs\sprite16_require_argument.inc
include procs\sprite16_optional_argument.inc
include procs\sprite16_require_number.inc
include procs\sprite16_optional_number_legacy.inc
include procs\sprite16_dispatch_options.inc
; Source-recorded reserved region 0A89h..0A90h (end exclusive).
layout_reserved_before_parse_number db 7 dup(0)
include procs\sprite16_parse_number.inc
include procs\sprite16_parse_decimal.inc
include procs\sprite16_parse_hex.inc
include procs\sprite16_parse_binary.inc
include procs\sprite16_parse_switch.inc
; Source-recorded reserved region 0BC6h..0BD0h (end exclusive).
layout_reserved_before_egc_begin db 10 dup(0)
include procs\sprite16_egc_begin.inc
include procs\sprite16_egc_end.inc
; Source-recorded reserved region 0C3Ch..0C40h (end exclusive).
layout_reserved_before_string_length db 4 dup(0)
include procs\sprite16_string_length.inc
include procs\sprite16_string_equal_folded.inc
; Source-recorded reserved region 0C76h..0C80h.
layout_reserved_before_data db 10 dup(0)
include src\zun\driver_data.inl
_TEXT ends
end start
