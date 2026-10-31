# MAINL xx normal-library integration

The complete maintained DOS xx.cpp compiles under its real `xx` module name,
replaces that member in the normal893-member library,and links actual MAINL.
The current route uses BCC4.5 native `-c -y` output followed by TLIB/TLINK.
It remains a **raw-different diagnostic candidate**,with no new accepted bytes.

Two rounds repeat complete raw ASM,OBJ,LIB,EXE and MAP vectors. Candidate EXE
is67324 bytes versus the fixed Japanese67372-byte target. Both headers have
4096 bytes and677 relocations;the complete raw images and MAPs still differ.

## Source compilation and retained inputs

`build_th03_mainl_xx_work.py` validates and reuses the reviewed28-provider normal
library pair. Native TLIB extracts all893 members;every extracted member must
retain its actual program records. Only xx.cpp is recompiled. The new library
preserves all893 positions and all892 surrounding member records,including28
source providers. xx becomes candidate provider29;the accepted publication
remains211 owners/288 entries/36946 bytes with its28-provider library.

All36 project objects plus real pinned C0L,EMU.LIB and MATHL.LIB remain unchanged.
The link response binds those39 binary inputs explicitly. The938 retained cold
outputs are validated/reused;no ancestor runtime or full cold/DIET chain is rerun.

DOS transport shortens include filenames only. Actual BCC receives xx.cpp and
produces xx.obj directly. A separate ordinary `-S` pass supplies the50 mangled
procedure names and near/far declarations;its ASM is never assembled into the
product object. All linked CODE/DATA bytes come from actual native compilation.
The retained full-TU S/TASM miniature is a separate diagnostic baseline.

`decoded_mainl_xx_native.py` finds actual source definitions and closing braces,
then binds their lines to native source-file COMENT and LINNUM records. It
requires one entry/epilogue per procedure in source order,decodes the declared
RET/RETF before the next procedure,and separately reviews inline storage.
No guessed prologue scan or target-sized slicing supplies native boundaries.
Both builder and reviewer recompute all50 mappings from transported sources.

Native BCC cannot parse PUSHAD/PUSHFD,EAX or FS/GS even with -3. The maintained
native path expresses individual unsupported386 instructions with named
`__emit__` intrinsics. FS/GS stores use compiler-symbolic `context` plus
offsetof-derived displacements;no BP slot is hardcoded. The native inline
assembler reverses local-member offset addition:context.eflags addressed
BP-482 rather than BP-98,and SS read BP-490 rather than BP-90. An actual linked
Raise probe exposed the broken return to0000:0000. The corrected native spelling
uses `context - member_offset`,including symbolic DW displacements for FS/GS.
ES callback calls use the native compiler's slot spelling. The default S/TASM
path retains its previous readable instructions and operands. No function-byte
arrays,product object patches or compensating storage are involved.

## Complete native comparison

| Property | Original | Native candidate |
| --- | ---: | ---: |
| xx CODE at0000:580D | 12622 | 12572 |
| Literal native fields | 187 | 187 |
| Ordered xx MZ words | 20 | 20 |
| DATA/BSS | 18/10 | 18/10 |
| RTTI tail/metadata | 1735/136 | 1735/136 |
| Raise body/frame | 1151/390 | 1081/342 |

Candidate DATA/BSS remain at DGROUP:1172/2876;DGROUP is0E3C versus original0E3F.
Ordinary paragraph layout produces48 bytes of file movement. All18 initialized
DATA bytes agree;BSS has no invented initialization. CODE length50 is a size
difference,not a count of differing bytes. Native RTTI includes one actual
LEDATA zero and no LIDATA. Its descriptors,vtable,terminated lists and all
internal pointer identities are checked;the complete tail remains raw-different.

The reviewer resolves every CODE byte and all187 literal fields through the
real product MAP and18 library interfaces. All22 public bindings and20 emitted
xx MZ words match the actual executable. All18 EXTDEF names/indices agree in
original order. Equal field counts do not establish whole-record equality;
literal field vectors remain retained,without sorting or normalization.

The complete first1327 object bytes match the original,including all four
literal ordered fields. These bytes also match at their original linked address.
This includes sameTypeID157,findBaseType339 and compatibleType372. Native BCC
retains all six five-byte forward FAR CALLs that S/TASM shortened. Each original/
current field is checked for its actual9A opcode,far shape and real callee.
Complete linked destroyBases129 and destroyVariable715 now agree. Their linked
raw equality is a complete function-body observation within the unaccepted TU.

All50 complete linked bodies are compared;23 currently agree raw. Other useful
partial findings remain explicitly separate:

- dtorCleanup1035/frame32 differs only at object offsets976/977 in the
  callMemberFunc operand. All1025 bytes outside five local CALL operands agree;
  all five actual helper identities and field order40/996/932 agree.
- ExceptionHandler880/frame56 differs at seven object operand bytes. All854
  other bytes agree. Its12-byte table has original relative destinations and
  descending field order10/8/6/4/2/0. Body-field order still differs.
- initCatchArg674 versus678 recovers the class guard,leaving two reference
  branch forms. exceptionHandled223 versus216 retains one10/17-byte load
  sequence gap. Frames and local slots retain the recovered source declarations.
- `typeinfo::before` matches all120 unlinked bytes with original strcmp field
  EXTDEF8 at+96. Its linked displacement remains different.
- Raise retains all71 raw count/index/copy bytes. The48-byte frame region
  BP[-134,-86) has unproved type/purpose;no placeholder or flag fix is added.
  callCopyCtor767 versus750 and other layout/source differences remain open.

## Focused execution evidence and receipts

Five target/source pairs execute real linked RTTI/jump routines:virtual-address
merging,distinct-address ambiguity,downcast containment,secondary-vtable update
and register catch jump. They preserve the selected far frames and registers.
The linked Raise/dispatcher pair uses the unchanged actual TASM handler fixture
and the real library memcpy twice,without import redirection or a memory-helper
model. The handler's DEADBEEFh EAX update resumes correctly. At entry SP=FF00,
record/register/context observations agree including EFLAGS84h. At FF10 only
the known original80h/source84h discrepancy remains. These are focused probes,
not a DOS boot or ending-playthrough claim.

Keep `.analysis/work/mainl-xx-product-build.json`,
`mainl-xx-product-review.json`,both `xx-product-roundN-xx.asm/.obj`,
`xx-product-roundN-xxcrt.lib`, `xx-product-roundN-xxfull.exe/.map`,the exact
transported sources,maintained xx.cpp snapshot,responses and native phase logs.
Native LINNUM in the actual objects replaces product TASM listings. The earlier
failed displacement experiments and corrected native control are summarized in
`.analysis/work/xx-native-compiler-recovery.json`.

```sh
PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_xx_work.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_work.py
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_xx_work
```

Source presence stays250 extents/60028 gross bytes. Require complete original
CODE/ordered-field/layout and raw EXE/MAP equality before promotion. Next resolve
the remaining copy-adapter,catch,Raise storage and surrounding layout gaps.
