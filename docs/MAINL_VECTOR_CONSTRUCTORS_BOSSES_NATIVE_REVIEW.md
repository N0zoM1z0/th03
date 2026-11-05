# Two original C++ array constructor bosses — after393

The pinned Japanese Borland `CL.LIB` members `vnew` (index 144) and `vnewv`
(index 147) are now fully recovered in the maintained, separate 8086 source
translation units `src/mainl/crt/vnew.asm` and `vnewv.asm`.

The first exports `__vector_new_` with **313 original-equal CODE bytes**; the
second exports `__vector_vnew_` with **345 original-equal CODE bytes**. Both
handle optional array allocation, the 16-bit element count, an optional
leading two-byte count header, near/far constructor callback dispatch in eight
modes, and a length/count-controlled iteration. The `vnewv` calling convention
passes an additional original zero initializer argument, which accounts for
its longer native code. Neither is an artificial byte blob or an object patch.

Each native member matches its entire original `_TEXT`/`_DATA`/`_BSS` segment
sizes, the public entry at CODE+0, the single far import `@$bnew$qui`, and **all
9 relocation fields**: seven genuine `dw offset` entries in a CODE-resident
mode table, one symbolic table dispatch, and one imported allocation call.
All frames/targets/addends match their original OMF fields. As with `vdel`,
original Borland orders the FIXUPP fields in descending site order whereas
TASM's literal record chronology differs. The two full Borland member record
programs are not claimed literally identical.

The incremental source-bound builder, reviewer and tests are:

```
PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_after393_work.py vector-constructor-bosses
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after393_work.py vector-constructor-bosses
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after393_work -v
```

Both independent fresh native TASM/TLIB/TLINK rounds retain entire raw
OBJ/LIB/EXE/MAP vectors and writer logs, inherited from the unchanged 532-member
after392 CRT carrier, without full cold replay. The CRT now contains **534/893**
source-built members, 359 contextual original vendor members, and **160,990
original-equal source CODE bytes**. The complete decoded Japanese original
`MAINL.EXE` (67,372 bytes, 677 ordered MZ relocations) and MAP are byte exact
in both rounds. This proves the scoped working CRT relation, *not* Factory
source acceptance, packed-original unit ownership or original library member
record serialization.
