# Eight complete DOS, IBM display, pointer and arithmetic CRT leaves

This increment adds source-backed **eight whole original Japanese CL.LIB
members** to the 332-member MAINL CRT carrier. Seven 8086 `.asm` files are
newly authored; `n_pcmp.asm` already existed in the tracked baseline source
graph and was **left at its original tracked content**, not rewritten or
excluded to evade the active source-hash dependency.

| Original CRT member | Original CODE bytes | Reconstructed behavior |
| --- | ---: | --- |
| `n_pcmp` | 33 | near comparison of normalized far/huge pointers, preserving flags |
| `f_pcmp` | 33 | far pointer comparator with both original public aliases |
| `dosclose` | 26 | INT 21h AH=3Eh close with carry/error helper |
| `doscmmit` | 26 | INT 21h AH=68h commit with original error path |
| `cibmtxmd` | 36 | IBM textmode: optional current-mode read, initialize and write video mode |
| `cibmgtxy` | 24 | IBM BIOS cursor-position service wrapper, far ret 4 |
| `f_lxmul` | 23 | original far 32×32-bit low-product multiply in DX:AX |
| `textknj` | 15 | console Kanji mode setter through original framed global |

`src/mainl/crt/{n_pcmp,f_pcmp,dosclose,doscmmit,cibmtxmd,cibmgtxy,f_lxmul,textknj}.asm`
contain full natural original 16-bit instruction sequences, original CODE
segment lengths and zero DATA/BSS sizes, all PUBDEF aliases and imports,
original DGROUP definitions, and complete import relocation positions,
widths, targets and addends.

`src/mainl/crt/n_pcmp.asm` is a pre-existing tracked source consumed by the
pinned parent cold receipt. A formatting rewrite initially caused a source
hash mismatch in the inherited receipt verifier. Restoring only that local
rewrite made the unchanged original parent evidence valid again. This is a
source-provenance correction, **not** rerunning a full cold build.

## Exact native proof and honest OMF limitations

`scripts/build_th03_mainl_after328_work.py dos-pointer-ibm-leaves` checks
the complete parent 332-source receipt chain, compiles these eight original
CRT member names with TASM and assembles/links all 893 library members with
TLIB/TLINK in two independent native rounds. Both rounds reproduce all
original CODE bytes and the **complete original Japanese decoded MAINL EXE
and MAP**, including all 677 ordered MZ relocations. There are now **340**
complete source-backed CRT programs, **553** contextual original vendor
programs and **111,057 source-compiled original-equal CODE bytes**, an
increase of **216**. All raw OBJ/LIB/EXE/MAP and tool logs remain under
`.analysis/work/after328-*`; the source/driver/parent hashes bind the
receipt and reviewer.

Literal original OMF FIXUPP identity is **not** claimed for all eight. The
original near `__DOSERROR`/`__IBM_VIDEOINT`/`___ibm_crtinit` imports use
Borland TARGET frame5, while TASM emits CODE frame0; their fixup sites and
targets are link-equivalent. `cibmtxmd` uses explicit `DGROUP:` for both
`__video` data reads/writes, which restores the original group-framed
relocations at CODE+12 and CODE+30. `textknj` matches its full single
framed relocation; the three pointer/multiply leaves have no relocations.
All eight original OMF program-record serializations still differ from the
source-produced objects (mostly TASM COMENT and original vendor records).
The per-member literal FIXUPP and original program-record truth values are
retained in each native receipt round and verified by
`tests/test_mainl_after328_work.py` and
`scripts/review_th03_mainl_after328_work.py`.

No full cold replay, packed-product credit or Factory source acceptance is
claimed for this working-source carrier extension.
