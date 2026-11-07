# TH03 MAIN two small but ABI-sensitive source owners: Extra Attack and Gauge — after753

The current maintained `src/main/player/exatt.cpp` and
`src/main/player/gauge.cpp` are **distinct original physical Turbo C++
translation units**. The callback leaf `p_exatt` has **41 original CODE
bytes, 2 ordered OMF FIXUPPs and one PUBLIC**. It copies two
`SubpixelBase` wrapper parameters into original 16-bit local words and
uses the original per-character far/Pascal Extra Attack function pointers.
The Gauge leaf `p_gauge` has **55 CODE bytes, one ordered native fixup and
one PUBLIC**; it refuses gauge charge in Hyper mode or at maximum and
saturates a 16-bit gauge after its original additive update.

## Actual original-native C++ recovery and negative evidence

The extra-attack dispatcher now naturally accesses the underlying
original **signed 16-bit subpixel fields** directly:

    subpixel_t center_x = center_x_.v;
    subpixel_t center_y = center_y_.v;

Both independent near local copies remain; the original 2-player
character callback selection `if(!pid)` and 16-bit far function pointer
ABI are unchanged. This is a current-source C++ representation of the
historical layout, not an unsafe pointer reinterpretation.

The first two-owner actual Turbo C++ trial `af753b` also challenged
`p.gauge_avail += charge` by writing the equivalent explicit assignment
`p.gauge_avail = p.gauge_avail + charge`. **The real Gauge CODE differed**
so this version is rejected, not reported as byte-equal.
`af753c` restored the original compound memory update, retained the
explicit Extra Attack subpixel fields, and passed all original native
object, fixup and whole-normal-MAIN link checks in two rounds.
`af753d` subsequently added the explanatory codegen notes and again
compiled the *final live current source* twice, with exact native output.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af753d --units p_exatt,p_gauge
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af753d

Both rounds match **all 96 original CODE bytes, three literal ordered
native FIXUPP fields, two PUBLICs and complete segment declarations**.
Full normal 99-project-object MAIN EXE and path-normalized MAP, original
Japanese 124,642-byte loaded program and all 1,553 ordered relocations
are exact. Independent standard MZ serialization reproduces every byte
of the original 130,882-byte Japanese MAIN.EXE. The other 97 original
project objects and CRT were **reused**, not cold rebuilt. The failed
Gauge trial remains separately retained in the native writer evidence;
no target-byte patch or synthetic OMF CODE was used.

Current source-bound proof `.analysis/work/exatt-layout-af753d/report.json`,
SHA-256 `87f36820bf005488834895d4e78a63cc1cc7942b0c76d972bcdec52be7af5604`.
These already source-owned original bytes are **not** new canonical Factory
packed-file accepted credit, historical vendor raw OMF identity or proof
of complete game source ownership.
