# DOS strchr original native reconstruction and seven-source CRT carrier

src/mainl/crt/strchr.asm now restores all63 original 8086 CODE bytes in
the DOS large-model far-cdecl strchr library member at original index291.
The actual TASM native object matches the original code,one public _strchr
entry,zero literal ordered fixups,zero DATA/BSS extents,and the literal
BSS-before-DATA DGROUP record 08ff03ff02. It is mnemonic-based natural
source,not a target-byte array or a patched library member.

The routine saves DS/SI/DI, uses CLD, handles an odd starting string
offset with LODSB, then scans low and high bytes of successive WORDs
via LODSW. Each candidate character is checked before the appropriate
null terminator,with original pointers restored by the actual SI-relative
return arithmetic. Both the far not-found NULL and matching pointer paths
preserve the original ABI and instruction layout.

The cumulative native CRT source bank has now **seven** recovered
original member implementations: memchr37, memcmp40, memcpy36,
memset72 (two public entries), strchr63, strcmp48 and strlen33. Their
total is **329 source CODE bytes**. The real 893-member TLIB rebuild
replaces only original positions259/260/261/263/291/292/300 and
preserves all886 other native member program records literally. Two
actual serialized TASM/TLIB/TLINK rounds repeat complete raw OBJ/LIB/
EXE/MAP vectors. Both source-built MAINL executables are raw-identical
to every byte of the original fixed 67,372-byte decoded Japanese EXE
and MAP,including all677 ordered MZ relocations.

This is an independently proved source-only native CRT working carrier.
The accepted 28-provider library and211-owner source-credit ledger
remain unchanged; source-exact evidence does not alone publish acceptance.
The original cold/DIET and ancestor runtime chains were not replayed.

Affected-only reproducibility:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_crt_growth_work.py memchr-memset-strlen-strchr
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_crt_growth_work.py memchr-memset-strlen-strchr
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_crt_growth_work

Keep the current .analysis/work/mainl-crt-growth-memchr-memset-strlen-strchr
build/review reports, source inputs, phase logs, responses and both
complete native raw output vectors.
