# MAINL project-source cold build

This checkpoint stages all 35 project objects from maintained source producers and the frozen ReC98 source archive. It does not use cached project OBJ, EXE or MAP files as build inputs. TC4 startup C0L.OBJ and EMU.LIB, MATHL.LIB and CL.LIB remain explicitly declared toolchain context. The six CRT replacements are a separate integration lane.

## Source stage

Run from the repository root:

    python3 -B scripts/stage_th03_mainl_cold.py --output .analysis/mainl-cold-aggregate-proposal-new/staged

The output directory must be fresh. The helper reads the frozen reference source archive, chains maintained heap, graphics/staff, root, PI, resources, archive, display, root-tail and linked-game composers, and applies maintained registration, cutscene and shared providers. No native tool is invoked. Context text is committed with canonical LF endings and explicitly converted to CRLF during staging. Source inputs are fixed to 2026-10-21T00:00:00Z. The declared response preserves original order and first-use GAME/BINARY flags, including scoredat GAME=3/BINARY=O. Original vector.obj is explicitly replaced by maintained vector_far.obj at ordinal 14.

The original portable stage reproduced the reviewed historical 1,881-file snapshot exactly. The current stage adds two maintained alignment providers and composes their root changes, producing 1,883 source files. The historical proof does not attest this post-alignment full 35-object stage; a new full cold run remains pending. Its 35-object graph includes 30 TCC and five TASM stages, followed by one TLINK. The native proof uses two fresh carriers and groups of at most five commands, 90-second per-native execution plus 15-second owned cleanup, 115-second supervisor allowance, 900-second work and 1,000-second Factory group budgets.

## Evidence and limits

`config/mainl_cold_context/proof.json` records completed group receipts and all 37 raw products (35 OBJ, EXE and MAP). Repeat equality is checked on raw files without timestamp or output normalization. The historical native proposals and failures remain in ignored evidence; this checkpoint does not overwrite their hashes.

The historical cold EXE is 67,372 bytes and byte-identical to prior MLG12 SHA-256 6d159b90fffe0d0ac00d587429204fa616228abc7244ee4c4e184449a2fdde63. Therefore prior runtime model evidence can be retained by whole-file identity. No fresh runtime models are claimed. The native verifier's runtime_pending field denotes no fresh runtime invocation, not absence of reusable identical-EXE evidence.

For that historical cold EXE, the loaded image is 63,276 bytes with exactly one byte difference: DATA 0E3F:0849 (linear 60473), target 90h versus candidate 00h. All 677 relocation members agree, but 461 ordered indices differ. The new MAP differs only in the vector_far module name and omission of that replacement's zero-length DATA/BSS contributions; EXE code and layout remain unchanged.

Frozen headers, declarations, macros, root DATA/BSS, original scanner codestring, and generated flake.asp remain declared context, not additional source-owned functions. The lexical closure records 325 project inputs and ten toolchain headers; it is not a claim of native preprocessor tracing. This proof adds no source function count, byte count or canonical exactness credit. The later alignment root-only build and repeat close the decoded DATA difference, but do not replace this historical full-cold proof. The aligned loaded image equals the decoded target; 461 relocation-order differences and packed inequality remain. See mainl-vsync-alignment.md for the separate proof scope.
