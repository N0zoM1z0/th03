#ifndef TH03_MAIN_FORMATS_PI_LOAD_HPP
#define TH03_MAIN_FORMATS_PI_LOAD_HPP

struct PiHeader {
    unsigned char opaque[0x48];
};

extern "C" {
extern PiHeader pi_headers[6];
extern void far *pi_buffers[6];

int far pascal graph_pi_load_pack(
    const char far *filename,
    PiHeader far *header,
    void far * far *bufptr
);
void far pascal graph_pi_free(
    PiHeader far *header,
    const void far *image
);
}

int far pascal pi_load(int slot, const char far *fn);

#endif
