; Bounded per-TU exception registration without a local exception class.
; Five unwind instructions bytes and ten actual control bytes in _TEXT.
; Each original owner is separate; descending fields preserve FIXUPP order.
org 9
string_exception_frame:
    dd string_exception_header
    dw -30 ; registration remains BP-1Eh even with larger local frames

org 5
string_exception_header:
    dd 0 ; original null exception-class list

org 0
string_exception_unwind:
    push si
    push di
    pop di
    pop si
    retf
