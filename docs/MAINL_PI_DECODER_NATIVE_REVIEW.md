# Complete MAINL packed PI decoder

The current root producer owns the complete decoded0000:1038..162B range:
1524 library CODE bytes. Source statements match the original master.lib
provider attributed to SuCa. The ledger's former authored classification is
corrected to library; no game-authored byte credit is added.

The same lineage check identifies six previously accepted bodies as unmodified
master.lib source: keyclear6,setcolor41,off5,random42,string compare56 and PI
free76. Their226 bytes are reclassified without changing any native boundary,
ABI,hash or relocation. Current MAINL source totals therefore comprise16136
authored bytes and1750 library bytes; only the decoder's1524 bytes are new credit.

| Part | Offset | Bytes | ABI |
| --- | --- | --- | --- |
| Shared error exit | 1038 | 11 | Borrows loader BP/SI/DI frame; RETF12 |
| Ordinary outer EVEN | 1043 | 1 | Assembler alignment |
| graph_pi_load_pack | 1044 | 1211 | Far Pascal,three far arguments,RETF12 |
| Ordinary outer EVEN | 14FF | 1 | Assembler alignment |
| _read_color | 1500 | 238 | Private near helper |
| byte_load | 15EE | 44 | Private near helper |
| _buffer_load | 161A | 18 | Private near helper |

There are four callable procedures. The shared error exit is not a fifth:
it restores DGROUP and pops the caller-established DI/SI/BP frame before returning.
The two outer EVEN bytes have source/native ownership; they do not add procedures.
Internal macro alignment remains part of the original symbolic implementation.

The actual producer is `th03_mainl.asm`, TASM5/GAME3/L, whose10944-byte `_TEXT`
starts at decoded0000:0272. Its actual group1 is DGROUP over BSS/DATA; group2
contains the separate game CODE contributions. Complete segment geometry,
literal include consumption, line-ending transport and every root dependency
are checked. All1524 owned bytes have explicit nonoverlapping LEDATA coverage.
No gaps are silently filled and no object or executable is patched.

The six emitted OMF fields retain their actual order:

| Site | Field | Resolved value |
| --- | --- | --- |
| 103C | Group1 segment | DGROUP0E3F |
| 1120 | Group1 segment | DGROUP0E3F |
| 1179 | Group1 segment | DGROUP0E3F |
| 1125 | Own DATA offset WORD,addend0744 | mem_AllocID0856 |
| 117E | Own DATA offset WORD,addend0744 | mem_AllocID0856 |
| 14EC | Group1 segment | DGROUP0E3F |

The complete independently resolved bytes equal both pinned Japanese target and
current candidate. The literal ordered MZ vector is103C,1120,1179,14EC,all in
segment0000,with no straddling relocation. Both MAP public tables establish the
loader and allocator-tag addresses. Five genuine PUSH CS/CALL bridges target
DOS_ROPEN,SMEM_WGET,HMEM_LALLOCATE twice and SMEM_RELEASE; every other near call
enters one of the three private helpers. All branches enter complete owned
instructions. Each complete procedure/shared exit has its original return ABI.

The decoder builds its adaptive16x16 color table in the private16KiB input-buffer
allocation. It keeps bit-buffer state, color-rank updates, variable-length copy
lengths and five positional copy forms. Source `_too`/`_tor` macros preserve the
original64KiB offset wrapping and1000h segment adjustment. Heap/stack providers,
root DATA/BSS and external allocation ownership remain outside this range.

Preserve the original unchecked behavior: initial/refill DOS read CF/AX are not
validated; refill POPA restores AX and XOR SI clears carry. A failed extension
allocation stores AX and continues without skipping its bytes. Width/height
arithmetic wraps at16bits; zero/odd geometry is not sanitized. Position zero
consumes the high length word while other copy paths do not. Early exits can
leave resources allocated. This review does not add defensive fixes or claim
physical DOS/device execution.

The unchanged full source graph, tools,938 cold outputs, normal893-member CRT
library rebuild and decoded/DIET stored identities are revalidated. Previous97
native owner records and complete scoped gate evidence are retained from
commit3e7e9dd after checking every old proof input except the deliberately
updated acceptance module. Only the six demonstrated origin classifications
change in current prior owners. Historical runtime observations are preserved and
not reexecuted by this native review. No compilation or full cold replay was
necessary because all native inputs remain unchanged.

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.decoded_mainl_pi_decoder_native
.venv/bin/python scripts/publish_th03_mainl_work_scopes.py
```

The provider's historical `.asm` include name remains part of its frozen source
recipe. It is a bounded provider in the real containing TU, not an invented
standalone TU. Rename it deliberately when that recipe changes. Whole MAINL
source ownership and canonical packed-file unit credit remain open.
