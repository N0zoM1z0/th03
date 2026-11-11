/* Borland C/C++ Run Time Library, Version 6.0.
 * Copyright (c) 1987, 1993 Borland International. All Rights Reserved.
 * Supplier-derived SETVBUF.C; preserve its register parameter and unchecked ABI.
 */
#include <stdio.h>
#include <stdlib.h>

extern void (*_exitbuf)();
extern void _xfflush();

static int _stdinStarted = 0;
static int _stdoutStarted = 0;

int _FARFUNC setvbuf(register FILE *fp, char *buf, int type, size_t size)
{
    if (fp->token != (short)fp || _IONBF < type || 0x7fff < size)
        return EOF;

    if (!_stdoutStarted && (short)fp == (short)stdout)
        _stdoutStarted = 1;
    else if (!_stdinStarted && (short)fp == (short)stdin)
        _stdinStarted = 1;

    /* fseek flushes and preserves the position before changing the buffer. */
    if (fp->level)
        fseek(fp, 0L, SEEK_CUR);
    if (fp->flags & _F_BUF)
        free(fp->buffer);

    fp->flags &= ~(_F_BUF | _F_LBUF);
    fp->bsize = 0;
    fp->curp = fp->buffer = &fp->hold;

    if (_IONBF != type && size > 0) {
        _exitbuf = _xfflush;
        if (NULL == buf) {
            if ((buf = malloc(size)) != NULL)
                fp->flags |= _F_BUF;
            else
                return EOF;
        }
        fp->buffer = fp->curp = (unsigned char *)buf;
        fp->bsize = size;
        if (_IOLBF == type)
            fp->flags |= _F_LBUF;
    }
    return 0;
}
