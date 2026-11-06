// C/ASM filename ABI: these existing assembler symbols have no C underscore.
// The exported table spelling matches PIC_FN in the ordinary C++ callers.
#pragma option -u- -zC_TEXT

extern const char near a00sl_cd2[];
extern const char near a02sl_cd2[];
extern const char near a04sl_cd2[];
extern const char near a06sl_cd2[];
extern const char near a08sl_cd2[];
extern const char near a10sl_cd2[];
extern const char near a12sl_cd2[];
extern const char near a14sl_cd2[];
extern const char near a16sl_cd2[];

const char near *_PIC_FN[9] = {
    a00sl_cd2, a02sl_cd2, a04sl_cd2,
    a06sl_cd2, a08sl_cd2, a10sl_cd2,
    a12sl_cd2, a14sl_cd2, a16sl_cd2
};
