// Original Borland DOS far-cdecl ftime delegating to native far __ftime.
// The C source name _ftime acquires the actual double-underscore
// external __ftime under Borland's historical C naming convention.
extern "C" void far __cdecl _ftime(void far *);

extern "C" void far __cdecl ftime(void far *time_data)
{
    _ftime(time_data);
}
