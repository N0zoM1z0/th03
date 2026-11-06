# MAINL large cutscene control: natural C++ plus after570 sound sources

The maintained source src/mainl/cutscene.cpp contains a complete 3,195-byte
GAME=3 / BINARY=L Turbo C++ cutscene script and drawing controller, including
13 near procedures (3,122 instruction bytes), an inline 72-byte compiler
switch table and one original zero context byte. It handles script loading,
sequencing, picture display, EGC VRAM copies, text effects and input timing.

The original cutscene compilation was already source-reviewed; in particular,
the old source comment claiming three unresolved PI call operands is
historical and was superseded by the independently reviewed exact native
cutscene proof. This stage does **not** count these functions again or
rewrite the frozen original source/cold publication.

The new independent src/mainl/cutscene/producer.cpp translation unit explicitly
includes that one maintained natural C++ implementation, without altering
its original contents or adding compiler-specific padding. Two independent
Turbo C++ 4.02 compilations used the exact original first-use
GAME=3/BINARY='L' flags. Each compiled object reproduces the entire original
3,195-byte CODE initializer, all 13 PUBLIC names/offsets, all
236 **ordered OMF relocation fields** and segment geometry. The original
56 literal MZ relocation sites within the producer are unchanged.

Each round then replaced just the CUTSCENE object in the *latest* source-native
MAINL link, already containing four natural sound hardware TASM functions,
the natural input-scan EVEN, typed DATA banks, registration EVEN, original
C0/CRT and vector functions. Both actual TLINK runs exactly reproduced
the **entire original Japanese 67,372-byte decoded MAINL EXE** and all
**677 ordered MZ relocations**, with full MAP contributions identical
after normalizing the new compiler diagnostic module path.

All original scope proofs were checked against maintained source/headers
but the 36-object cold chain was **not** replayed. The resulting raw
OBJ/EXE/MAP rounds, C++ wrappers, fourteen source dependency hashes,
four native writer logs and linker responses are retained.

Read-only affected review:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_cutscene_after573_work.py

Producer: scripts/build_th03_mainl_cutscene_after573_work.py
Report: .analysis/work/mainl-cutscene-after573-native-build.json
Review: .analysis/work/mainl-cutscene-after573-native-review.json

The original C++ OMF THEADR/COMENT dependency paths may differ when the
independent source wrapper changes the module's diagnostic file name.
No original compiler-identity, new authored-function denominator, packed
DIET product source closure or canonical Factory acceptance is claimed.
This is a scoped native source-integration proof, not duplicate credit.
