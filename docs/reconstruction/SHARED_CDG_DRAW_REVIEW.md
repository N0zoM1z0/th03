# Shared OP/MAINL CDG drawing

Two complete shared assembler carriers are localized under
`src/shared/formats/cdg_put.asm` and `cdg_noalpha.asm`, through three explicit
compatibility forwarders. They contain493 native function bytes and three
separately reviewed natural `EVEN` bytes. One physical object per carrier is
linked into OP and MAINL and absent from MAIN. Each artifact is bound and
reviewed independently; no cross-game or MAINL exactness is inherited.

| Function | Bytes | OP entry | MAINL entry | Return |
| --- | ---: | --- | --- | --- |
| Alpha |179|0BEB:0170|0C7E:01F4|far RET6|
| Horizontal flip |201|0BEB:0224|0C7E:02A8|far RET6|
| No alpha |113|0BEB:0C46|0C7E:0F32|far RET6|

Whole MAP contributions are382 and114 bytes. The separate producer bytes are
OP0223/02ED/0CB7 and MAINL02A7/0371/0FA3. Original source has `EVEN` directives;
no target padding or opaque byte arrays are introduced. Internal EVEN NOPs
remain part of their complete function bodies. The ASM memory model, SHARED
segment, translation/link order, public symbols, imported layout/macros and
far Pascal argument order are preserved. External slot/LUT global storage and
the complete forwarded declarations remain outside source acceptance.

The native functions patch twelve immediate words: five in alpha, six in
hflip and one in noalpha. Every writer and complete MOV immediate destination
is audited. The two alpha routines call one explicit color-setup interface
with `[color0,modeC0]`; original `OUT7C,0` executes after the alpha pass. All
REP/LOOP/XLAT/SMC instructions and native far returns execute unchanged.
No memory-read hook is installed, preserving the separately documented
Unicorn far-return control. The color fixture preserves its ABI and supplies
explicit volatile AX/CX/DX/carry replies; no real GRCG setup body is accepted.

The independent scalar model reads its actual synthetic physical source and
lookup bytes and implements word offset arithmetic, signed SAR3, row stopping,
unsigned plane traversal and code operand patches. Each invocation compares
the complete ordered patch/store/callback/port trace and all physical1MiB
outside64KiB stack. SS/SP/BP/SI/DI/DS frames and saved registers are checked at
original returns; IF/DF and final ES/FS are checked separately. Hflip clobbers
FS and preserves DF; forward routines clear DF. Pixel width/height and plane
size fields are deliberately inconsistent with the precomputed width/bottom
fields actually used. Slots31/32/FFFF, negative/beyond-screen coordinates,
null/shared/DGROUP source aliases, identity/XOR/reversal LUT fixtures and
failure replies are retained as constructed caller contracts.

Do-first-row stopping depends on the sign of the updated destination offset,
without clipping or a height counter. Top-1 traverses five color planes.
A forward dword at offsetFFFF crosses the physical64KiB segment boundary as
one access; hflip's individual bytes wrap their effective offsets separately.
Original widths and strides remain word-sized. No physical GRCG RMW broadcast,
banked pages, pixels, game assets or IRQ-safe reentrancy is proved. The shared
patched CODE is retained without adding guards or locks.

Reentry triples use one emulator: original geometry, replacement geometry,
original geometry again. VRAM and patched CODE persist between calls; only
the explicit metadata fixture is refreshed. The complete resulting memory and
ordered effects must match at each step. Additional mixed-function controls
check FS and DF across hflip/alpha/noalpha/hflip calls.

Width0 alpha reaches a color LOOP starting atCX0; hflip begins an alpha byte
LOOP atCX0. Their independently checked2000-instruction prefixes have391 and327
flat stores respectively. Alpha has emitted GRCG-off; hflip has not. Neither
is reported as a successful return. Width0 noalpha executes empty REP copies
and returns without pixel stores. The source preserves these unchecked paths.

Diagnostic receipt `.analysis/sol-shared-cdg-draw-review-20261006.json`, SHA256
`42623621ef9fee6f4b69cc0cbeabd9c16b7678759963b05fd110bf542ed57ee6`,
guards422 inputs. Per artifact's decoded target/two preceding cold images:
114 records/336 invocations,334 returns/two prefixes, all200 positions,
47672 ordered trace events and45881 graph stores. Whole496 raw bytes and the
two original ordered relocation rows match both cold images independently.
Eleven behavioral/negative controls pass on both bindings; malformed SMC,
lookup/call/EVEN, patch values, physical bytes and SS aliases are rejected.

Two fresh source cold rounds each run42 focused records/120 invocations,
118 returns/two prefixes, all200 positions,12974 trace events and12335 graph
stores per artifact. Both20product/350game-object vectors are deterministic;
all20products equal the preceding shared-loader proof and348 other game objects
are unchanged. All416 OMF hashes are recorded; nine Research benchmark changes
are retained separately without an all-object determinism claim. Each original
ordered nondependency OMF record matches the preceding physical producer,
including empty CDG_PUT_TEXT/DATA segments, SHARED382/114 CODE, public/external
symbols, LEDATA and FIXUPP. Only E8/E9 filename/timestamp dependencies are
separated. Compiler inputs explicitly convert maintained ASM/include LF to
CRLF; repository source and snapshots remain independently guarded.

Source receipt
`.analysis/th03-shared-cdg-draw/sol-shared-cdg-draw-source-20261006/receipt.json`,
SHA256 `3af43ad7435658807c9bab066d99c2e324dda825627d287be37c087e7abca2b9`,
guards432 inputs. OP now has23 reviewed units/10979bytes and16 source-present
extents/10612bytes. MAINL's six existing drawing function/producer rows are
upgraded without duplicate interval credit:145 rows/11 source-present extents,
1089bytes in one shared CPP/two ASM. OP/MAINL exact0. Whole OP6-byte and MAINL
21-byte decoded failures and original whole relocation-order failures remain.
Headers, global DATA/BSS/DGROUP/LUT, devices/resources, CRT, independent pristine
provenance, canonical DIET packing and complete product Oracles remain open.

Replay with `scripts/review_th03_shared_cdg_draw.py --output .analysis/NEW_DRAW.json`
and `scripts/replay_th03_shared_cdg_draw.py --run-id NEW_DRAW`. The older
`MAINL_CDG_PUT_REVIEW.md` remains a separate historical cached/interface proof.
MAIN's accepted exact aggregate is unchanged.

The current interval receipt
`.analysis/sol-current-decoded-coverage-after-shared-cdg-draw-20261006.json`,
SHA256 `a2f148f46bda46f14f1729693832a7422d7fe3921d85462bfae2f496b6cf29be`,
guards447 inputs. OP has100 CODE carriers/55262bytes:10979 reviewed and44283 gaps;
MAINL has108 carriers/58340bytes:28381 reviewed and29959 gaps. Both unions have
zero overlap. MAINL's union is unchanged by upgrading existing rows.

Full CI passes534 tests and all available private headless gates. Receipt
`.analysis/sol-shared-cdg-draw-complete-ci-20261006.log`, SHA256
`e26606cbec69df9f6c0d553273b5f8fe2c030b51d19aa27b092426a2ea25435e`.
Tracking has232 units/2196 evidence/270 knowledge/120 MAIN authored-function rows.
Both successful source rounds and their complete guarded inputs are retained;
this migration generated no failed preparation trees for cleanup.
