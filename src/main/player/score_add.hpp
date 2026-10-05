#ifndef TH03_MAIN_SCORE_ADD_HPP
#define TH03_MAIN_SCORE_ADD_HPP

// Both Pascal arguments occupy word slots; pid uses only its low byte.
void far pascal score_add(unsigned int score, unsigned char pid);

#endif
