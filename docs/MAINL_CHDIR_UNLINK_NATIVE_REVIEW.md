# Original DOS chdir / unlink: two exact CRT objects in 55-source MAINL

The original far DOS change-directory and unlink modules at distinct
CRT member indices8 and136 now have maintained native 8086 sources:
src/mainl/crt/chdir.asm and src/mainl/crt/unlink.asm. Both use the
original DS:DX far path convention with saved/restored caller DS and
DOS INT 21h, preserving AH=3Bh (chdir) and AH=41h (unlink), carry
semantics, and genuine near __IOERROR on failure. They are distinct
original public/file-system owners, not duplicate coverage of the
already source-reconstructed CRT remove module.

Native TASM5 reproduces **all 28 CODE bytes in each module** and
the original far PUBLIC, near __IOERROR import, CODE-framed
relocation at site22, zero DATA/BSS and literal original
08ff03ff02 BSS-before-DATA group. All ordered OMF fields are
identical; no extra guards, machine-code byte arrays or object
patching are used.

The scoped builder inherits the verified 53-source original CRT
(including the large strftime, timecvt, 395-byte tempnam, xx,
sorters, directory, file and scanner modules), replaces the
distinct chdir/unlink members and leaves **838 other original
893-member program records byte-identical**. Two actual native
TASM/TLIB/TLINK rounds reproduce the entire **67,372-byte
Japanese decoded MAINL EXE and native MAP** bit-for-bit, including
**677 original MZ relocations**. The 55-source working CODE extent
is **27,422 original bytes**, an increase of56 newly source-built
CODE bytes.

The existing fopen/fclose/_timecvt/strftime/tempnam raw OMF
discrepancies are still explicitly OPEN in their own modules.
The accepted28-provider CRT, formal211-owner MAINL publication,
pinned candidate-local-attested original and cold pair are
unchanged. Source-only normal-link exactness adds no formal
accepted credit. No full cold or DIET replay was executed.

Affected-only validation:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_posttempnam_work.py dirs
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttempnam_work.py dirs
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttempnam_work

Both full source OBJ/LIB/EXE/MAP output vectors, actual Borland
writer logs and source/driver-bound receipts are retained in
.analysis/work/posttempnam-dirs-*.
