#ifndef TH03_MAIN_RANDRING_GETTERS_HPP
#define TH03_MAIN_RANDRING_GETTERS_HPP

// All entries consume the same byte index; words at index 255 cross into it.
unsigned int near randring1_next16(void);
unsigned int near pascal randring1_next16_and(unsigned int mask);
unsigned int near randring2_next16(void);
unsigned int near pascal randring2_next16_and(unsigned int mask);
unsigned int near pascal randring2_next16_mod(unsigned int divisor);
unsigned int far randring_far_next16(void);
unsigned int far pascal randring_far_next16_and(unsigned int mask);
unsigned int far pascal randring_far_next16_mod(unsigned int divisor);

#endif
