; Resident messages, startup stack, packed state and command tables.
; Japanese literals are encoded to Shift-JIS by the maintained stager.
; Defaults and ordering are recovered source facts, not a target-byte blob.
; State words after the interrupt byte deliberately remain unaligned.
sprite16_resize_failed_message	db 'メモリ縮小に失敗しました。',0Dh,0Ah,0
sprite16_already_installed_message	db 'すでに常駐しています。',0Dh,0Ah,0
sprite16_environment_free_failed_message	db '環境領域解放失敗',0Dh,0Ah,0
sprite16_mask_free_failed_message	db 'マスクデータ領域解放失敗',0Dh,0Ah,0
sprite16_solid_free_failed_message	db 'ベタデータ領域解放失敗',0Dh,0Ah,0
sprite16_code_free_failed_message	db 'コード領域解放失敗',0Dh,0Ah,0
sprite16_removed_message		db '解放しました。',0Dh,0Ah,0
sprite16_not_installed_message	db '常駐していません。',0Dh,0Ah,0
; Startup sets SP to the following state boundary: this is a 512-byte stack.
sprite16_startup_stack db 200h dup(0)
sprite16_startup_stack_top label byte
sprite16_previous_vector_segment	dw 0
sprite16_previous_vector_offset	dw 0
sprite16_mask_buffer_segment	dw 0
sprite16_solid_buffer_segment	dw 0
sprite16_int40_signature_found	dw 0
sprite16_interrupt_number	db 42h
sprite16_resident_paragraphs	dw 0
sprite16_dispatch_target	dw 0
sprite16_memory_failed_message	db 'メモリが足りません。',0Dh,0Ah,0
sprite16_installed_message	db '常駐しました。(int %02Xh)',0Dh,0Ah,0
sprite16_banner	label byte


	db 'ZUNSP.COM    Version 1.00 Copyright(C) 1997 ZUN           ',0Dh,0Ah
	db 0Dh,0Ah,0
sprite16_usage 	label byte
	db 'Usage: ZUNSP    -z (常駐)',0Dh,0Ah


	db '                -r (解放)',0Dh,0Ah,0
sprite16_option_install		db '/Z',0
sprite16_option_remove		db '/R',0
sprite16_option_vector		db '/V',0
sprite16_option_masktest	db 'MASKTEST',0
sprite16_option_pressy		db 'PRESSY',0
sprite16_option_copyul		db 'COPYUL',0
sprite16_option_clsu		db 'CLSU',0
sprite16_option_sprite		db 'SPRITE',0
sprite16_option_table	dw offset sprite16_option_install, offset sprite16_install
		dw offset sprite16_option_remove, offset sprite16_uninstall
		dw offset sprite16_option_vector, offset sprite16_set_interrupt_argument
		dw offset sprite16_option_masktest, offset sprite16_mask_test_command
		dw offset sprite16_option_pressy, offset sprite16_compress_rows
		dw offset sprite16_option_copyul, offset sprite16_copy_lower_page
		dw offset sprite16_option_clsu, offset	sprite16_clear_upper
		dw offset sprite16_option_sprite, offset sprite16_draw_command
		dw 0
sprite16_service_table	dw offset sprite16_prepare_vram
		dw offset sprite16_build_mask
		dw offset sprite16_draw_clipped
		dw offset sprite16_set_mono_enabled
		dw offset sprite16_set_mono_color
		dw offset sprite16_set_overlap
		dw offset sprite16_set_access_plane
		dw offset sprite16_set_rop
		dw offset sprite16_set_mask
sprite16_bit_shift	dw 0
sprite16_has_shift	dw 0
sprite16_clipped_rows	dw 0
sprite16_row_skip_bytes	dw 0
sprite16_row_words	dw 0
sprite16_draw_x	dw 0
sprite16_draw_y	dw 0
sprite16_draw_source_offset	dw 0
sprite16_draw_width	dw 0
sprite16_draw_height	dw 0
sprite16_mono_enabled	dw 0
sprite16_mono_color	dw 0Fh
sprite16_overlap	dw 1
sprite16_rop	dw 28FCh
sprite16_mask	dw 0FFFFh
sprite16_access_plane	dw 0FFF0h
sprite16_argument_count	dw 0
; 64 near token pointers; recovered parser has no capacity check.
sprite16_argument_vector dw 64 dup(0)
sprite16_argument_cursor	dw 0
sprite16_missing_quote_message	db '対になる " が見つかりません。',0Dh,0Ah,0
sprite16_missing_argument_message		db '引数が足りません。',0Dh,0Ah
		db 0Dh,0Ah,0
sprite16_invalid_number_message	db '数値では無い値が指定されています。',0Dh,0Ah
		db 0Dh,0Ah,0
sprite16_invalid_option_message	db 'オプションが無効です。',0Dh,0Ah
		db 0Dh,0Ah,0
; Source-recorded reserved bytes, purpose unknown.
sprite16_reserved_before_switches db 3 dup(0)
sprite16_switch_on		db 'ON',0
sprite16_switch_off		db 'OFF',0
; Source-recorded terminal reserved bytes, purpose unknown.
sprite16_reserved_tail db 9 dup(0)
