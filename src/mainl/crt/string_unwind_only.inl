; Proved five-byte local unwind owner in find2 and resize.
; No exception registration table is present in these original members.
org 0
string_exception_unwind:
    push si
    push di
    pop di
    pop si
    retf
