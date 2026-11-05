# Original full string::strip trim/COW method: 317-byte native CODE

The complete Japanese Borland CL.LIB member **429**, `strip`, is now
represented by real 8086 source at `src/mainl/crt/strip.asm`. This is a
full C++ trim method with original far return and call ABI, not a tiny leaf
or an import-only stub. The implementation scans leading and trailing
characters for the specified trim mode, calculates the remaining substring
and updates a `TStringRef`, including the original copy-on-write allocation
and reference handling. Both original allocation sites and all failure and
no-trim paths remain present.

Original `_TEXT` contains the **5-byte far unwind thunk**; `_TEXTC` holds
**312 bytes** of the complete exported method
`@string@strip$q16string@StripTypec`. Original DATA/BSS are zero bytes and
DGROUP order is `0aff02ff03`. Every original instruction byte, public
symbol, both imports and the complete original OMF fixup field population
agree with the actual pinned Japanese CL.LIB member.

The original BCC FIXUPP records are ordered **`_TEXTC+249`, then
`_TEXTC+110`**, both imported far `@$bnew$qui` references. Writing the
same original 8086 source forward preserved all 317 CODE bytes but emitted
them in the opposite OMF order. The final source emits the real later
allocation instruction block from its original offset 248 before the
preceding code using `ORG`, retaining the original opcode bytes while
restoring the **literal original FIXUPP order, width, frame, target and
addend**. There is no binary patch, synthesized executable padding or
machine-code data array. The complete original Borland OMF member record
serialization still differs from new TASM metadata and is not claimed equal.

`scripts/build_th03_mainl_after358_work.py string-strip-boss` consumes the
**410-member** source/receipt-verified CRT carrier, assembles only this
new member, and produces all 893 original library positions under native
TASM/TLIB/TLINK in **two independent rounds**. Both rounds are byte-identical
to the **67,372-byte Japanese decoded MAINL EXE and complete MAP**, including
**677 ordered DOS MZ relocations**. Working-source CRT now contains **411
complete original-equal members** and **482 unchanged original contextual
programs**, with **132,745 original-equal logical CRT CODE bytes**, an
increase of **317**. Raw native OBJ/LIB/EXE/MAP, assembly/linker logs, source
and parent SHA receipts are retained under `.analysis/work/after358-*`,
reviewed by `scripts/review_th03_mainl_after358_work.py` and
`tests/test_mainl_after358_work.py`.

This is verified working CRT source, not new Factory accepted decoded ownership
or canonical packed-file unit credit. No full cold replay was executed.
