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
MAIN's accepted exact aggregate remains separate.

Two independent fresh frozen archives with all preceding OP overlays and the
new shared TU pass. Each artifact per round runs82 focused cases/all219 native
positions,829 entries,7014 ordered stores,3895 foreign events and980 explicit
input bytes. All593 raw bytes and original ordered relocations pass, as do
five MAP public entries. Both complete20product/350game-object vectors are
deterministic and equal the preceding Select products;349 other game objects
are unchanged. All416 normalized OMF hashes are recorded. Nine Research
benchmark objects differ from the preceding build because their DATA embeds
build time; those differences remain separate, without a416-object determinism
claim. The initial overstrict all-object gate and a corrected Pascal MAP-name
guard failure remain as diagnostic transcripts, without target defect credit.

Source receipt
`.analysis/th03-shared-cdg-load/sol-shared-cdg-load-source-20261006-c/receipt.json`,
SHA256 `3a299bf3d442ba49e4856f6226ad0ecda5b71ae7760cbf3d6ec6d97ca9a11a99`,
guards378 inputs. OP is now10116 source-present bytes in14 extents and10483
reviewed bytes in21 units. MAINL's five existing593-byte rows become
source-present; there are still145 rows and no duplicate interval ownership.
The MAINL candidate index stays diagnostic with source/exact acceptance false;
independent source-presence records require compiler/runtime/reproducibility
evidence and a cold replay command. Interval accounting preserves source
migration coverage. OP and MAINL exact0; complete OP6-byte and MAINL21-byte
decoded failures and whole original relocation-order failures remain.

An original-order OMF audit compares all normalized nondependency producer
records in both rounds against the preceding physical producer: CODE593,
DATA0/BSS0, PUBDEF/EXTDEF/LNAMES/GRPDEF/LEDATA/FIXUPP and other producer comments
match. E8/E9 dependency filenames/timestamps are separated explicitly; no
target relocation rows or code/data bytes are normalized away. Receipt
`.analysis/sol-shared-cdg-omf-ownership-20261006.json`, SHA256
`84102a64a896dc24699f16c39de46385481da6dc8d32d1516a4204c3e0d547f5`,
guards382 inputs, including the replayable private audit recipe.

Fresh interval receipt
`.analysis/sol-current-decoded-coverage-after-shared-cdg-20261006.json`,
SHA256 `60b44792f7dd0bb016d8621094dbbfbf889baedf64aaaddf5a140dcf55383ede`,
guards393 inputs, including current units and both current MAPs. OP100 CODE
carriers have10483 reviewed/44779 gap bytes; MAINL108 carriers have28381
reviewed/29959 gaps. Both have zero overlap. Gaps are interval accounting,
not unknown-semantic counts or whole-file progress. Replay with
`scripts/review_th03_current_decoded_coverage.py`, the source receipt path and
its SHA256, and a new `--output`. Historical shifted MAP coverage is retained.

After both successful rounds, two unreferenced failed preparations were
removed:4962 files/61841191 bytes (about59MiB). All1723 retained private input
path states stayed unchanged. First failure and complete cold transcripts,
the successful proof tree, archives, targets, toolchain and Ghidra remain.
Cleanup receipt `.analysis/sol-shared-cdg-load-temporary-cleanup-20261006.json`,
SHA256 `3bb5b89e62d752348f237c736972e0e1cc2c4aa1572983f662395ca1af414bf3`.
Full523-test CI and all available private headless gates pass in
`.analysis/sol-shared-cdg-load-complete-ci-20261006.log`, SHA256
`dec63f6d8f4c8b63631afacc5053c74ddf9c927a9f16d1a58c44776201a3b2e9`.
