; The real near CALL crosses the five externally owned COM payloads.
; PAYLOAD_BYTES is supplied from the complete staged input lengths.
.8086
.model tiny
.code
org 100h
start:
 call $ + 3 + PAYLOAD_BYTES
END start
