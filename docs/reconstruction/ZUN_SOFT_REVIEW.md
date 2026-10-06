# Complete ZUN -3 logo root candidate review

The complete frozen `th01/zunsoft.cpp` root has been reviewed, including all
ten procedures, initialized data, BSS declarations, inlined page/hardware and
polar operations, direct calls, exits and near/Pascal ABI. Its 1299 CODE bytes
form one cached compiler contribution. No maintained source or exact owner
is added. Graphics/BFNT libraries, startup/remaining CRT, asset ownership and
the complete -3 product remain open.

```sh
python3 scripts/review_th03_zunsoft.py --output .analysis/NEW_LOGO_REVIEW.json
python3 -m unittest discover -s tests -p test_zunsoft_review.py -v
```

The reviewed receipt is `.analysis/sol-zunsoft-review-20261006.json`.
Both pinned cached -3 outputs equal all 10096 decoded payload bytes, including
their unreviewed library/runtime areas. This is a cached raw diagnostic; it
does not prove fresh maintained compilation or whole-image ownership.

## Target lineage and source/compiler association

The frozen revision is `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
Root SHA-256 is
`a2fd32b9213f89dbf582c36d48390f216666ca533f60cf2b3daa42d3d9984d98`.
Payload SHA-256 is
`beeb86dc055c585a32f4500c9eabb2e6cb1e0537bcdbc5f3763ebefa4308e297`.
Decoded outer file `0B32–32A1` holds -3, with outer runtime origin `0C32`.
The wrapper copies it to `CS:0100`; all offsets below use this inner namespace.
Canonical stored-file offsets are deliberately absent. Stored-target identity
and DIET restoration receipts are guarded; no packed database observation is
used. Provenance remains candidate-local-attested, independent pristine unknown.

The frozen Tupfile selects the TH01 tiny-model logo executable as TH03 option
-3. Cached response files link `c0t.obj`, the root, masters/emulation/math/C
runtime libraries using TLINK `-c -s -t`. MAP attributes root CODE `0367/0513`,
initialized DATA `21CE/000F` and BSS `2870/0125`. All nine consulted frozen
root/provider files match both cached source trees byte-for-byte. Both root
OMF objects pass framing/checksums, record TC86 Borland C++ 4.02 and agree after
dependency timestamp normalization. Additional dependencies remain visible
in OMF and require separate header/library review. Source `#pragma option
-2 -d-`, link model and ordering must survive localization; cache association
is not a fresh toolchain gate or source acceptance.

## Complete procedure boundaries

| Inner address | Size | Candidate procedure |
| --- | ---: | --- |
| `0367` | 29 | `graph_clear_both` |
| `0384` | 76 | `zunsoft_init` |
| `03D0` | 20 | `zunsoft_exit` |
| `03E4` | 85 | `zunsoft_vector2` |
| `0439` | 201 | `objects_setup` |
| `0502` | 180 | `circles_render_and_update` |
| `05B6` | 205 | `stars_render_and_update` |
| `0683` | 21 | `wait` |
| `0698` | 309 | `logo_render_and_update` |
| `07CD` | 173 | `main` |

All bodies completely decode and terminate at the reviewed near returns.
Their sizes sum to 1299 with no unexplained internal gaps. Direct branches
hit instruction boundaries; calls hit root entries, two explicitly executed
compiler arithmetic entries, or explicit modeled imports. Cached coordinates
are provisional target associations rather than automatic authored progress.

The vector function is near Pascal, consumes eight argument bytes with RET 8
and writes through two near reference pointers. Other root entries use near
RET without callee argument cleanup. Long multiplication uses actual
`N_LXMUL@` at `188C`; arithmetic shift uses `N_LXRSH@` at `17D8`. The latter
converts the near return frame to a far frame with POP/PUSH CS/PUSH and RETF.
It remains a compiler producer, not authored logo code. Real instructions of
both helpers execute in the probe; no arithmetic substitute is used.

The target reads signed word sine/cosine tables at `22E8/2368`, uses an 8-bit
angle, a signed 16-bit length, a signed 32-bit product and an arithmetic right
shift by eight before retaining the word result. For angle 32 and length 37,
the observed vector is `(26,26)`; angle 160 gives `(-27,-27)`. Negative floor
rounding and overflow widths must be preserved. Do not replace this with
floating-point trigonometry or symmetric truncation. Table provenance and
whole library data ownership still require review.

## Initialized data, BSS and source behavior

The root's fifteen initialized bytes hold `touhou.dat` with NUL and four
circle colors `4,3,2,1`. The filename is an interface to private BFNT content,
not authorization to commit that resource. Its 293-byte BSS contribution is:

| Inner range | Root declaration |
| --- | --- |
| `2870–2871` | byte back/front pages |
| `2872–2877` | tone, pattern, wave length/phase/amplitude/padding bytes |
| `2878–2887` | four word x/y circle positions |
| `2888–294F` | fifty word x/y star positions |
| `2950–2951` | signed word frame |
| `2952–2961` | four word x speeds and four word y speeds |
| `2962` | byte star angle |
| `2963–2994` | fifty byte star speeds |

The probe constructs zero BSS instead of executing CRT initialization. Page,
frame, tone and object setup assignments are actual root instructions. The
padding byte remains a declaration/layout slot; it is not counted as invented
CODE padding. `irand` is a substituted signed-word interface with deterministic
values within 0–32767. Its generator/seed behavior is not executed or accepted.

Initialization calls memory/graphics/text/key/EGC setup, clears both pages,
sets back/front to 0/1 and clipping rectangle `(96,100,543,299)`, hides graph,
requests BFNT load, displays palette, sets tone to zero, and shows graph.
The BFNT result is not checked: a modeled negative return still proceeds.
This root observation does not establish how a real loader/blitter behaves
when the resource is absent. Exit frees sprites, clears pages, unassigns
memory, clears text and calls EGC start again. Beep/systemline/cursor restoration
is not present in this exit source; do not invent cleanup behavior.

Setup gives circle positions `(128,320),(256,240),(384,160),(512,80)`, speeds
`(-8,+8)`, frame/tone/pattern/phase/amplitude zero, wave length 23, star angle
`40h`, and fifty random positions/speeds. Circles render in reverse index
order, radius 96, before advancing coordinates. X speed reverses for a new
position `<=32` or `>607`; Y speed reverses for `<=32` or `>367`. Coordinates
are not clamped. Constructed boundary results at 32/33/607/608 and 32/33/367/368
are preserved by the replay.

Stars render then advance using the current vector; each coordinate receives
at most one 640/400 wrap adjustment. Angle increments once per update with
byte wrap. This order, signed word coordinates and byte speeds must survive
any future source migration; broader out-of-range contracts remain unproved.

Logo phases are `<50`: none; `50–89`: ordinary pair; `90–109`: wave pair with
length decreasing and amplitude increasing; `110–129`: wave pair with length
increasing and amplitude decreasing; `130–169`: ordinary pair; `>=170`: none.
Pattern advances by two at frames 55/60/65, 110, 155/160/165. Both wave calls
use the pre-update byte values. Phase changes by four and retains byte wrap;
the compiler sign-extends signed char values when promoting them to word
arguments. A constructed phase `FAh` is passed as word `FFFAh`, then becomes
`FEh`. No unsigned reinterpretation or saturation is added.

Main tests low-memory `045C` bit 40h. When set, it writes `7,20h,6` to port
6Ah and clears bit 80h at `054D`. It initializes the root, then updates tone
and objects, renders the logo, waits twice, flips pages and scans all eight
key groups. A nonzero key aggregate exits without incrementing frame. Normal
fade-out starts after frame 180 and exits once tone is nonpositive. Wait polls
port A0h bit 20h until clear then set, with port 5Fh writes on each poll; no
timeout exists. Page display/access writes use ports A4h/A6h.

## Bounded observations and remaining Oracles

Each of target and two cached images runs three complete modeled root flows:
natural fade-out, first-frame key exit with the low-memory hardware branch,
and natural fade-out with a negative modeled asset result. Natural runs render
231 frames, return with frame 231/tone 0, perform 1848 key calls and 1848
modeled VSync reads, and call sprite free once. Early exit renders one frame,
returns with frame 0/tone 2 and still queries all eight key groups. Low-memory
byte `054D` changes FF→7F only for the hardware branch. Stack/SI/DI/BP/DS
returns are checked. Event and OUT traces are hashed, with compact counts and
palette checkpoints retained in the receipt.

Each image also runs 1280 complete vector calls (256 angles for five signed
lengths), one circle-boundary call and sixteen isolated logo-stage cases.
Combined scope is **3900 root CPU/model calls** across the three images.
The vectors use real compiler math helpers and the actual table bytes. Import
models provide only Pascal cleanup, deterministic random/keyboard/BFNT returns
and call traces. They do not execute graphics/EGC/BFNT/memory libraries or
prove pixel rendering, resource validity, real input, VSync timing or device
restoration. CRT startup/argv/exit are bypassed. No game resource is loaded or
changed; comparisons do not supply independent hardware/runtime Oracles.

Six synthetic tests reject invalid size/returns/cleanup, data branches,
interior calls, unexpected indirect edges and unmodeled interrupts. Callback
errors are captured and raised outside ctypes. The ten root ledger entries
are boundary-reviewed with blank canonical offsets and no maintained source.
Cold maintained builds, localization/encoding, complete library/data/asset/
startup review, layout/packaging and full Oracles remain required. Current
Wine/Ghidra execution failures and read-only Git prevent cold verification
and commits; exact counts remain unchanged and the 505-file goal stays open.
