; Shared buffer size, archive error and legacy XOR key.
; The containing native DATA module uses WORD alignment; no source filler.
public bbufsiz, _bbufsiz
_bbufsiz label word
bbufsiz dw BBUFSIZE
public pferrno, _pferrno
_pferrno label word
pferrno dw PFEZERO
public pfkey, _pfkey
_pfkey label byte
pfkey db 0
