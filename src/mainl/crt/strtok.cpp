// Original Borland DOS large-model strtok source reconstruction.
// Two delimiter scans share a persistent BSS far pointer. BCC 4.5
// otherwise reloads next_token after comparing the byte in ES:BX;
// the typed pseudo-register pointer retains the original ES:BX access.
#include <dos.h>
static char far *next_token;
extern "C" char far * far __cdecl strtok(char far *text,char far *delimiter)
{
    char far *delim;
    char far *saved;
    if(text)
        next_token=text;
    while(*next_token) {
        for(delim=delimiter;*delim;++delim) {
            if(*delim == *next_token)
                break;
        }
        if(!*delim)
            break;
        ++next_token;
    }
    if(!*next_token)
        return 0;
    saved=next_token;
    while(*next_token) {
        for(delim=delimiter;*delim;++delim) {
            if(*delim == *next_token) {
                *(char far *)MK_FP(_ES,_BX)=0;
                ++next_token;
                goto token_done;
            }
        }
        ++next_token;
    }
token_done:
    return saved;
}
