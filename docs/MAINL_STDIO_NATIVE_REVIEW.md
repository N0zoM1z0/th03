# MAINL buffered stream and DOS write bank

Ten complete source TUs add1808 CODE+10 initialized DATA/INIT bytes in twelve
library extents,covering thirteen procedures. Sources are fflush209,flushall76,
fseek492,setvbuf289,write358,writea91,xfflush63,setupio164,lseek45 and isatty21.
The fseek module contains a137-byte near callee-pop4 byte-count helper,130-byte
far fseek and225-byte far ftell. Writea contains63-byte raw DOS writer and28-byte
public wrapper. Setupio is a near startup callback; other public APIs are far
cdecl. Three actual IOERROR imports are near callee-pop2,without caller cleanup.

All ten TUs consume the maintained `stdio_layout.inc`. Native field accesses and
the installed16-bit compiler header agree on FILE20:WORD level/flags,BYTE fd/hold,
WORD bsize,far buffer/curp,WORD temporary/token. Validity comparisons intentionally
compare only the FILE pointer offset against token. No new pointer defenses or
normalization are introduced. Full CODE preserves original16-bit sizes and
signed/unsigned comparisons,including signed mode<=2 in setvbuf.

Buffered position accounting starts with positive input level or,for output,
bsize+negative-level+1. Text mode additionally counts LF while scanning forward
through input or backward through pending output. Binary mode skips expansion.
Fseek flushes first,adjusts relative input offsets by buffered physical bytes,
clears EOF/input/output flags,resets cursor and invokes DOS seek. Ftell adjusts
the physical position by buffered bytes; append output temporarily seeks end
and restores the old physical position before adding pending bytes. Original
carry/sign extension and offset-only pointer increments remain unchanged.

Fflush(NULL) calls flushall and returns zero. Flushall returns the number of open
streams visited,ignoring individual fflush failures. Pending output resets
level/cursor before the write. A nonterminal short write sets the stream error
flag and returns-1; the original terminal branch returns success. Exit callback
xfflush deliberately visits only four FILE slots. No all-stream expansion is added.

Setvbuf keeps original mode/size/token checks,marks first stdin/stdout configuration,
ignores the position-preserving fseek result,and retains free/malloc ownership.
Its default unbuffered pointers address the FILE hold byte. Buffered mode installs
the genuine far xfflush callback. Two private initially zero standard-stream
flags contribute4 DATA bytes at0E3F:116C. Setupio initializes slots starting at5,
checks terminal status and applies the original stdin/stdout modes with512-byte
sizes. Its6-byte type0/priority2/near-offset/zero-segment startup record is at
0E3F:131E. These are real initialized storage,not BSS or padding.

Translated write checks the handle before the WORD count0/FFFF fast return. Append
seek failure is ignored as in the original. Text output clears handle EOF,adds
CR before LF,and checks the128-byte flush threshold after copying both bytes.
Consequently a chunk may contain129 bytes. Original short-write accounting and
signed error returns are preserved. The raw writer checks its original handle
flag,uses DOS AH40h with the caller's far buffer,restores DS and sets O_CHANGED
on success. Seek clears handle EOF before DOS AH42h even on failure. Isatty
returns the raw device80h bit after DOS4400h without checking carry.

One bounded actual-native probe sends127 ASCII bytes plus LF through the real
translated writer and real raw writer. Only successful DOS AH40h is hooked to
capture its buffer. It observes a single129-byte write with CR/LF,returned input
count128,restored DS,far caller-cleanup stack and original EOF/changed flag updates.
This resolves the chunk-boundary question without a heap,FILE or DOS model.

All initialized payloads match the original objects. All58 field identities and
geometry are reviewed with both literal emitted streams retained. Only the near
IOERROR call at write+23 changes its frame from target-derived to explicit same
CODE; the actual mapped target,addend,relative field and near callee-pop2 ABI agree.
Twenty ordinary far calls naturally relax. Complete independent field resolution
matches full linked CODE/DATA/INIT,target and current candidate. The sole real
new MZ relocation is0000:4EA7,the exit-buffer callback segment assignment.
Near startup and far callback offset WORDs do not gain segment relocations.
All complete dense procedures,local branches,publics and returns are checked.

Two actual TASM/TLIB/TLINK rounds compose25 source CRT providers:ten new,nine
validated reused natural pairs and six retained providers. All893 normal library
positions and874 other current member payloads remain unchanged. Whole ten-OBJ/
LIB/EXE/MAP vectors repeat; complete EXE/MAP match pinned Japanese decoded target/
retained MAP. All36 project objects and938 cold outputs/source/recipe/tools stay
unchanged. No full cold/DIET or ancestor runtime replay is needed. The frozen
cold recipe still replaces six CRT providers; this bounded recipe establishes
coexistence of twenty-five without rewriting older proof hashes.

MAINL now accepts205 extents,272 procedures/entries and34,688 bytes:
32,770 CODE+1,918 DATA;16,695 authored+17,993 library. Previous193 owner records
and nested scopes are unchanged. Source presence becomes234 extents/45,130 bytes,
including overlapping old aggregates which receive no duplicate accepted credit.
Stream/handle tables remain contextual; this scope credits only the storage above.
No padding,object patches,defensive changes,physical DOS execution or whole-product
source acceptance is claimed. Further CRT/data ownership work remains.
