# Japanese MAINL original CRT `calloc` and `puts`

Two complete 97-byte Borland 8086 CRT bodies have been recovered in
`src/mainl/crt/calloc.asm` and `src/mainl/crt/puts.asm` and assembled from real
TASM instructions, not embedded original CODE bytes or patched objects.

- `calloc` is original member160, public `_calloc` at CODE+0, 97 CODE / zero
  DATA/BSS. It preserves 32-bit `N_LXMUL@` size calculation, the original
  16-bit overflow gate, far `_malloc`, far `_setmem` zeroing, and null return
  propagation. All three original relocation sites/targets agree.
- `puts` is original member273, public `_puts` at CODE+0, 97 CODE / zero
  DATA/BSS. It preserves original null-string short-circuit, far `_strlen`,
  near `__FPUTN` bulk output, far `_fputc` newline output and original error
  results. The original `__streams+20` stdout pointer is symbolic, not an
  absolute-address approximation; all five original relocation sites/targets
  agree. TASM requires declaring DGROUP before `push ds` in this module.

Both source-generated complete CODE bodies, original public/import interfaces,
segment sizes, and decoded fixup sites/targets are byte-equivalent to the
selected original members of the **retained 893-member CRT baseline**, not
just standalone vendor object files. The original BCC object serializes the
FIXUPP sites in a different order from TASM; the near `N_LXMUL@` / `__FPUTN`
frame method may likewise differ. Original literal FIXUPP order/frame is
**not** claimed, and neither module is an added formally accepted source unit.

`build_th03_mainl_after62_work.py sprintf-calloc-puts` regenerates both
members alongside the newly recovered `sprintf` from the retained 62-source
working Japanese link, twice. In both independent native TASM/TLIB/TLINK
rounds, the resulting full decoded 67,372-byte EXE and its original MAP
match exactly, including all 677 DOS relocations. Working source CRT rises
to **65 members** and **28,937 original-equal CODE bytes** (additional 194
CODE bytes in this increment, 338 since the 62-source carrier); 828 members
remain unchanged vendor records. All raw outputs and tool phase logs are
retained under `.analysis/work/after62-sprintf-calloc-puts-*`. Reviewer:
`review_th03_mainl_after62_work.py sprintf-calloc-puts`; focused unit tests:
`tests.test_mainl_after62_work`. No full original cold replay was run.

Important rejected assumption: the standalone `setvbuf.obj` and `write.obj`
from the extracted vendor directory are **not** the selected members in the
retained working CRT library. The repository already has independent source
candidates for these; matching standalone CODE alone cannot justify treating
these two as *new* recovered slots. They are intentionally not counted here.
