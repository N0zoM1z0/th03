; master.lib PFSTART/PFEND state in BSS. Keep the original unchecked filename
; copy into its real128-byte buffer; no new bounds check or zero initializer.
parfilename db 128 dup(?)
pfint21_pf dw ?
pfint21_handle dw ?
if GAME ge 3
pfint21_entries dw ?
endif
