# Shared OP/MAINL CDG loading

The complete CDG loading carrier has five functions and593 decoded CODE bytes.
It is independently bound to Japanese OP and MAINL. One frozen
`obj/th03/cdg_load.obj` SHARED producer is linked to both products and absent
from MAIN. No DATA/BSS is defined in this TU. The maintained candidate is
`src/shared/formats/cdg_load.cpp`, with two explicit compatibility imports.
Source presence is separate from exact or whole-product acceptance.

| Function | Bytes | OP entry | MAINL entry | Far Pascal cleanup |
| --- | ---: | --- | --- | ---: |
| single |138|0BEB:05DA|0C7E:073E|8|
| single_noalpha |134|0BEB:0664|0C7E:07C8|8|
| all |230|0BEB:06EA|0C7E:084E|6|
| all_noalpha |28|0BEB:07D0|0C7E:0934|6|
| free |63|0BEB:07EC|0C7E:0950|2|

All bodies, branch destinations, public entries, external calls and five
internal near-call bridges are reviewed. Original `PUSH CS` instructions
precede those near calls; all far returns execute unchanged. Each artifact
uses its own code/data segments, slot address, flag address and six foreign
bindings. OP and MAINL observations are independent; neither borrows the
other artifact's acceptance. Targets remain candidate-local-attested, with
independent pristine-dump provenance unknown. DIET decoded coordinates grant
no canonical stored offsets or packing equality.

Native metadata accesses agree with five word fields at0/2/4/6/8, count and
layout bytes at10/11, and alpha/color segment words at12/14. These observed
accesses do not accept the complete forwarded header or global DATA/BSS
ownership. The bitplane size multiplied by5 wraps to16 bits before unsigned
32-bit promotion; the signed16 image index is sign-extended before the
32-bit displacement multiplication. Color allocation/read size wraps16 after
multiplication by4. Later-game CDG enum/layout claims are not inherited.

Single loading frees before opening; all-image loading opens before freeing.
All-image loading copies five word fields and the count byte, forces layout0,
and rereads the first count and the global noalpha flag each iteration.
`all_noalpha` sets the flag to1 and then0, without restoring an old nonzero
value. Open/read/seek replies and carry are unchecked. Null allocation replies
still cause read requests to segment0. Free independently requests release
for each nonzero handle and clears its word; equal handles cause two requests,
while metadata remains. A count0 header can retain malformed segment words
until a later free. These hazards remain in the source.

`scripts/review_th03_shared_cdg_load.py` compares independent scalar contracts
with original native execution over three images per artifact: decoded target
and the two preceding Select cold builds. Each image has328 cases covering
all219 native instruction positions,3316 native entries,28040 ordered native
stores,14958 foreign events and3904 explicitly injected bytes. Follow-up free
is included. Complete SS/SP/BP/SI/DI/DS caller frames, IF/DF, ordered stores,
foreign arguments, fixture writes and physical1MiB outside64KiB stack are
checked. Fixtures include word-size/index overflow, zero and failed replies,
short/absent headers, count255, duplicate handles, wrapped/out-of-table slots,
flag overlap and physical segment aliases. Synthetic header/payload writes
are bounded by each request; allocation replies name flat synthetic buffers.
No real files, game assets, DOS behavior or allocator implementation is proved.
No memory-read hook is installed: the separately reproduced Unicorn far-return
regression remains documented in `scripts/probe_th03_unicorn_far_return.py`.

Diagnostic receipt `.analysis/sol-shared-cdg-load-review-20261006.json`,
SHA256 `b75857090b1a86d8ceb80a558247609b3bc6a99f2293f905b5df760393de6c9a`,
guards372 inputs. Both preceding cold images per artifact match all593 raw
bytes and all24 original ordered carrier relocation rows, including each
complete function's rows. Nothing is sorted or waived. Thirteen behavioral
and negative controls pass on both bindings, including wrong bridge,
destination, far cleanup, SS, ordered store trace and physical byte changes.

The earlier OP coverage report used a different cold MAP: init0570/CDG05D9.
Its one-byte intersection with the reviewed init extent gives no CDG credit.
The current producer has init0571/105 and CDG05DA/593. Coverage must use the
current source proof's MAP and retain the older report as historical evidence.

Replay diagnostics with
`python3 scripts/review_th03_shared_cdg_load.py --output .analysis/NEW_SHARED_CDG.json`.
Replay maintained compilation with
`python3 scripts/replay_th03_shared_cdg_load.py --run-id NEW_SHARED_CDG`.
Cold source verification and cleanup receipts are recorded below after the
two fresh rounds finish. MAIN's accepted exact aggregate remains separate.
