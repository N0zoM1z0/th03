// Private far type comparison from the original DOS xx.cpp TU.
#include "xx_abi.h"

static int far sameTypeID(xx_type_ptr left,xx_type_ptr right)
{
    const char far *left_name;
    const char far *right_name;
    int left_char;
    int right_char;

    if(left == right)
        return 1;
    if(left->mask != right->mask || left->size != right->size ||
        ((left->mask | right->mask) & 0x80))
        return 0;
    left_name = (char far *)left + left->name_offset;
    right_name = (char far *)right + right->name_offset;
    do {
        left_char = *left_name++;
        right_char = *right_name++;
        if(left_char != right_char)
            return 0;
    } while(left_char);
    return 1;
}
