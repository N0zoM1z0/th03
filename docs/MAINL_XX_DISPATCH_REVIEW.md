# MAINL xx local unwind and dispatch source candidate

`src/mainl/crt/xx_dispatch.inl` recovers a bounded bank from the original
monolithic `xx.cpp` TU. It is an include rather than a proposed new product TU.
The bank at0000:72B3 spans1565 bytes:1533 instruction bytes in five procedures
and32 bytes of actual inline tables/signature. It is source-present,with zero
new exact credit. MAINL acceptance stays211 extents/288 procedures/36,946 bytes.
Source presence becomes241 extents/48,953 gross bytes.

| Bank-relative offset | Procedure | Instruction bytes | Return |
| ---: | --- | ---: | --- |
| 0 | local_unwind | 447 | near cdecl |
| 459 | _Local_unwind | 32 | far cdecl |
| 491 | _Return_unwind | 42 | far cdecl |
| 533 | findMatchingHandler | 132 | near cdecl |
| 673 | _ExceptionHandler | 880 | far cdecl |

The complete xx module remains12622 CODE-class bytes,18 DATA bytes and10 BSS
bytes. Public-symbol gaps do not define function sizes: the880-byte dispatcher
ends at78C4,followed by a12-byte switch table and further destruction helpers.
The bank's other table is12 bytes at7472; the semantic `**BCCxh1` tag occupies
754C..7553. Both six-entry switch tables enter actual instruction boundaries.
A native `#pragma codestring` emits the meaningful tag. No opcode array,padding
or target-derived product bytes are introduced.

The ABI header describes only the prefixes used by this bank. Native
`__InitExceptBlocks` and actual dispatcher accesses establish SS-relative
registration pointers,SS:0014 for the exception chain and SS:0016 for the far
runtime-info pointer. Registration fields are table+6,SP+10,context+12,DS+14,
SI+16,unwind flag+18,exception code+20,exception-info SS pointer+24 and a DWORD
destructor counter+26. The header's31-byte registration prefix does not prove
the size or tail padding of every original registration allocation.

Exception descriptors retain a WORD callback DS at+24 and a far free callback
at+26. Registration,matching handler and context are at+36,+38,+42; the used
prefix ends at58. Freeing a descriptor switches DS to the recorded callback
DS,then restores it. Destruction minima are signed16 values converted to the
callee's32-bit count. Near destructor-table offsets are paired with the context
table's segment,not left relative to DS. Compile-time offset/width constraints
check these concrete ABI questions against the actual16-bit compiler.

The local unwinder walks outer contexts before executing finally,catch cleanup
or destructor cleanup. Catch cleanup retains the original unchecked assumption
that its descriptor exists. The dispatcher preserves both saved DS and SI,
checks throw specifications while unwinding,and handles C++ catches plus C
filter forms. It preserves the original negative-filter rule: with the
noncontinuable flag set,it changes the registration context to the outer
context before returning continue-execution. No defensive product changes are
made. The later Win32 `_fpreset`,Delphi paths and flattened-pointer declarations
are not imported.

The later Borland [xx implementation](https://github.com/earthsiege2/borland-cpp-ide/blob/a0bdb214ae2a492edef4f82c91c55ec86394e7b3/SOURCE/RTL/SOURCE/EXCEPT/XX.CPP)
and [internal header](https://github.com/earthsiege2/borland-cpp-ide/blob/a0bdb214ae2a492edef4f82c91c55ec86394e7b3/SOURCE/RTL/RTLINC/XX.H)
were structural references. Their flat definitions and callback/environment
layout differ from the target. A new private Ghidra database of the fixed
67372-byte decoded Japanese MZ was independently attested against its existing
DIET declaration before observations were used. Complete original OMF fields,
MAP boundaries,linked bytes,body returns and branches were then checked directly;
Ghidra's inferred boundaries and parameter types are hypotheses.

The retained diagnostic profile uses the existing scoped BCC4.5 compiler with
`-O2-pg -Os -Z- -S`,then actual TASM5 and TLINK. Borland's
[optimizer documentation](https://bitsavers.trailing-edge.com/pdf/borland/borland_C%2B%2B/Borland_C%2B%2B_Version_3.1_Users_Guide_1992.pdf)
explains the separate optimization controls; this profile's suitability is
limited to the observed output. Two native rounds repeat full generated ASM,
two-OBJ,mini-EXE and MAP vectors. The wrapper includes the maintained bank and
ABI header; all64 available active SDK headers match the pinned installation.
This is an inventory of all available headers,not an inferred consumed subset.

Candidate CODE is1566 bytes and BSS8. The three public entry offsets match the
original bank,but the complete native bank does not match. Seven surrounding
private/runtime interfaces remain unresolved for full-TU integration. Internal
far calls become external five-byte calls; stack-cleanup grouping and field
streams differ. The diagnostic does not replace the original normal library
member or link the whole product. Exact ownership requires recovering and
integrating the surrounding xx TU,not normalizing these differences.

A single targeted native probe runs the negative constant C-filter branch in
the real target and real mini-linked source. Both return0 through the far
cdecl caller frame,preserve DS/SS/BP/SI/DI,move context0010 to0006,retain the
existing exception-info pointer,and write the saved DS/SI runtime fields.
No imported helper is executed: the mini-link's explicit context providers are
unreachable traps,not behavior models. The miniature has a real uninitialized
stack segment; the focused runner supplies its own caller stack. Other branches,
real DOS execution and whole-game exception behavior are not established.

The original211 accepted owners,their publication and verifier inputs,and the
938-output cold pair remain unchanged and are validated. No full cold/DIET or
ancestor runtime chain is replayed. Next work is the remaining original xx
helpers. Ghidra suggests spans of1151 for RaiseException,815 for
tossAnException and1035 for dtorCleanup; their returns and any inline metadata
need direct review before those sizes can support ownership. Original TU/layout
and literal relocation streams must be retained before this bank gains exact credit.
