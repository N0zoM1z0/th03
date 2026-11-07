# Chiyuri's paired Extra Attack updater: native C++ branch recovery

The 298-byte `exatt_update_chiyuri` is part of the full 978-byte
Extra Attack producer alongside the 518-byte beam renderer and other
helpers. Its initial state check previously used a hand-written
`mov bx` / `cmp byte ptr [bx], 0` / `je` block that jumped into a
separate conditional's interior, past a declaration and an increment.

A natural C++ statement now expresses the same two-pointer control flow:

    if(exatt_entity_p->state == 0) {
        exatt_entity_p++;
        continue;
    }

The `for` iteration step increments `exatt_entity_p` once more,
advancing over the paired slot exactly as the original jump did. The
`state == 1` branch retains its separate single increment/continue;
the state 2, arrival and beam lifetimes are untouched.

The change is verified with actual **two independent Turbo C++ 4.02
compiles plus TLINK rounds** through the retained, unchanged after596
99-object source-native MAIN link. Run the affected scope only:

    PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py \
      --stage af601n --units ex_chyu

Both C++-compiled objects match the original Chiyuri object for the
**entire 978 CODE bytes, all 55 ordered fixup fields, four PUBLIC
offsets and all segment definitions**. Both normal linked EXEs and
normalized complete MAPs match the after596 native pair. The original
Japanese program and 1,553 ordered relocations match, and the
independent standard DOS MZ serializer gives the full original
130,882-byte file, without embedding target bytes or patching an
object.

Evidence is retained at
`.analysis/work/exatt-layout-af601n/report.json`,
SHA-256
`181d0a3f54c2816059b33e5a272b67e03f8ce7a7b7d4543e1b6eff516c490ce7`,
with both raw new objects, links, MAPs, compiler logs and overlay TUs.
This replaces an unnecessary manual branch with exact natural C++.
No new already-owned bytes are credited, and original vendor OMF
packet identity or canonical Factory acceptance is not asserted.
