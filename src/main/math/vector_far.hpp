#ifndef TH03_MAIN_MATH_VECTOR_FAR_HPP
#define TH03_MAIN_MATH_VECTOR_FAR_HPP

#include "platform.h"

extern "C" {

void pascal vector2(
	int &ret_x,
	int &ret_y,
	unsigned char angle,
	int length
);

void pascal vector2_between_plus(
	int x1,
	int y1,
	int x2,
	int y2,
	unsigned char plus_angle,
	int &ret_x,
	int &ret_y,
	int length
);

}

#endif
