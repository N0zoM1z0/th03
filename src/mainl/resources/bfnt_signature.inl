; BFNT signature and the original trailing NUL; readers compare five bytes.
public BFNT_ID, _BFNT_ID
_BFNT_ID label byte
BFNT_ID db 'BFNT', 01ah
        db 0
