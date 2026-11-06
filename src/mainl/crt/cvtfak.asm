; Typed near vectors in separate DATA segments select printf/scanf diagnostics.
; Original Japanese Borland cvtfak: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn __abort:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_CVTSEG segment word public 'DATA'
_CVTSEG ends
_SCNSEG segment word public 'DATA'
_SCNSEG ends
DGROUP group _DATA
_DATA segment word public 'DATA'
print_prefix db 'print'
scan_prefix db ' scan'
unlinked_float_suffix db 'f : floating point formats not linked',13,10
_DATA ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
; Complete disjoint instruction chunks preserve original native field order.

org 0
formatting_unlinked:
    mov dx,offset DGROUP:print_prefix
    jmp short report_unlinked_float_formats

org 5
scanning_unlinked:
    mov dx,offset DGROUP:scan_prefix
report_unlinked_float_formats:
    mov cx, 5
    mov ah, 040h
    mov bx, 2
    int 021h
    mov cx, 027h

org 21
    mov dx,offset DGROUP:unlinked_float_suffix
    mov ah, 040h
    int 021h

org 28
    jmp near ptr __abort
_TEXT ends
_CVTSEG segment word public 'DATA'
; Original near printf conversion fallback vector.
dw offset formatting_unlinked
_CVTSEG ends
_SCNSEG segment word public 'DATA'
; Original three near scanf conversion fallback vectors.
dw offset scanning_unlinked,offset scanning_unlinked,offset scanning_unlinked
_SCNSEG ends
end
