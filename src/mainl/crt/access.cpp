// Original Borland DOS far-cdecl access: delegate pathname/mode to the
// original far DOS __access service without changed errno semantics.
// The C declaration _access produces the original __access import.
extern "C" int far __cdecl _access(const char far *,int);

extern "C" int far __cdecl access(const char far *path,int mode)
{
    return _access(path,mode);
}
