# Two original TH03 MAIN master.lib CODE carriers: exact native source

The original `mst_pref.obj` and `mst_body.obj` are sizeable physical CODE
owners contributed by **ReC98 `master.lib`**, not newly reverse-engineered
TH03 gameplay functions. Their symbolic assembler **build-carrier recipes**
are tracked under `config/main_work/library_carriers/`, outside `src/main`
to distinguish external vendor-library composition from maintained product
source. They compose the original library's actual subroutine includes and
preserve the fixed `_TEXT`, `_DATA`, `_BSS` and DGROUP layout and externals.

| Original physical object | Initialized CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `mst_pref` | 2,269 bytes | 128 | 30 |
| `mst_body` | 8,301 bytes | 336 | 73 |
| **Total** | **10,570 bytes** | **464** | **103** |

Scoped stage `af1338c` assembles these two complete original physical
owners in two independent rounds with original TASM 5.0, then substitutes
them into the frozen normal 99-object TLINK 6.10 response. Both complete
Japanese MAIN executables are byte-identical to the original normal link;
complete normalized MAP, segment definitions, all ordered native OMF
fields, all PUBLIC positions and ordered MZ relocations also match.

The source-bound reviewer recursively checks the carrier's library
`include` graph byte-for-byte against the retained ReC98 vendor reference
and the **actual include files consumed by TASM** in the toolchain
worktree. The reference directory is externally retained and ignored by
Git; no claim is made that this commit independently vendors that entire
third-party library. The retained proof records the include hashes, and
the build requires the same reference checkout.

These two objects add 10,570 bytes to the *physical object native-scope*
metric, not 10,570 newly authored or first-time recovered BOSS/game bytes.
The historical `input_s` TC4 417-byte/ASM 418-byte link gap remains open;
complete canonical Factory or whole-product acceptance is not established.
Only the affected two original library objects were reassembled; no full
cold source build occurred.

Read-only current source-bound evidence:

```
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_master_library_asm.py --stage af1338c --check
```
