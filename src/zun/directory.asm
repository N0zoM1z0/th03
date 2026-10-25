; ZUN's fixed 32-slot COM directory, reconstructed as semantic DATA records.
; This is a maintained producer, not attested original assembler source.
; Native command-line definitions supply actual linked module/payload lengths.
; Unused names and entry slots belong to the directory ABI, not CODE padding.
.8086
.model tiny
.code
org 100h

DIRECTORY_CAPACITY equ 32
PROCEDURE_COUNT equ 5
public directory_count, directory_names, directory_entries, directory_end

directory_count dw PROCEDURE_COUNT
directory_names label byte
    db '-1      ', '-2      ', '-3      ', '-4      ', '-5      '
    db (DIRECTORY_CAPACITY-PROCEDURE_COUNT)*8 dup(' ')
directory_entries label word
    dw first_payload
    dw first_payload + ONGCHK_BYTES
    dw first_payload + ONGCHK_BYTES + INIT_BYTES
    dw first_payload + ONGCHK_BYTES + INIT_BYTES + ZUNSOFT_BYTES
    dw first_payload + ONGCHK_BYTES + INIT_BYTES + ZUNSOFT_BYTES + DRIVER_BYTES
    dw first_payload + ONGCHK_BYTES + INIT_BYTES + ZUNSOFT_BYTES + DRIVER_BYTES + RES_YUME_BYTES
    dw (DIRECTORY_CAPACITY-PROCEDURE_COUNT) dup(0)
directory_end label byte

first_payload equ (100h + STUB_BYTES + (directory_end-directory_count) + CALL_BYTES)
END directory_count
