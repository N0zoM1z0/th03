# MAINL DOS overlay execution

`src/mainl/crt/exec.asm` recovers the complete 933-byte member: 671 CODE +262
file-backed CS storage bytes. It contains the 574-byte near cdecl __exec API
and a 97-byte copied load/transfer continuation. Both are explicit entry kinds;
the latter is not a second C function. All bytes are library source, with no
authored game credit. Previous 182 owners and nested scopes remain unchanged.

## Native source and composition

Two actual TASM/TLIB/TLINK rounds reproduce complete raw OBJ/LIB/EXE/MAP vectors.
The whole EXE equals the pinned Japanese decoded target and the whole MAP equals
the retained MAP. This selected normal library includes the new exec producer,
the unchanged natural farheap object from its validated native pair, and the six
retained source CRT producers. All 893 member positions and 891 other current
member payloads remain unchanged. Thirty-six project objects are reused.

The entire initialized native payload equals the original member. All 21 fields
retain their literal order, sites, widths, targets and addends. Four scalar DOS
globals use an explicit DGROUP frame where the old object used a target frame;
only these four exact equivalent changes are allowed. Both complete streams are
checked without sorting or object edits. The whole scoped MZ vector is empty.

The ordinary five-byte external __cexit far call naturally becomes
NOP/PUSH CS/near CALL through real TLINK. DGROUP@ is the actual CS-resident startup
WORD at 026D, containing DGROUP; the code reads that word. It is an offset
reference, not a segment immediate. IOERROR is the actual near error provider.
BYTE CODE, WORD empty DATA, DGROUP membership, the public entry and both MAP
tables are checked. No fake callee or replacement binary is used.

All 938 cold outputs, source, recipe and tools remain validated and unchanged.
The unchanged farheap native pair is reused, not reassembled. Only exec and the
affected combined library/links were rebuilt. No full cold, DIET or ancestor
runtime replay is needed. The full cold recipe still has six CRT replacements;
this selected recipe demonstrates their composition with two newer providers.

## Copied code and genuine work fields

The first 255 bytes are real uninitialized work storage: a 143-byte temporary
stack, PSP WORD, 80-byte path, two FCB result bytes, 24-byte MZ header and two
overlay-loader WORDs. The next 97 bytes are the copied continuation. The copy
length is derived from labels as 352 bytes, and its entry offset is 255 relative
to the copy. No native fixup falls within this copied code.

The initialized four-byte transfer vector contains that relative IP and a zero
segment, later filled by the caller. A saved environment WORD remains DW?. The
last initialized byte is the original sticky environment-reuse flag of 1.
Thus five bytes have source initializers, while 257 file-backed bytes do not.
Only those uninitialized file bytes use actual independently repeated linked
output in the comparison. No zero array or error string is introduced.

The continuation establishes its original odd temporary SP, loads with DOS
4B03h, restores the image SS:SP, updates PSP memory-end/environment fields and
transfers through the relative MZ entry. Its failure path retains the original
write of 15 bytes from the buffer start and DOS termination. The original object
does not initialize an error string there; reconstruction does not invent one.

## Original execution and error paths

__exec takes three far pointers through a near caller-pop ABI. It opens the
image, copies the PSP command tail, parses two FCBs, queries/resizes the DOS
block, scans the environment and reads the initial 24-byte image header. MZ and
COM paths preserve their original size arithmetic, extension handling and
entry/stack setup. Path copying remains unchecked, the environment flag remains
sticky, and DOS-version/environment fallback behavior remains unchanged.

It copies the continuation to the top of retained memory, copies the environment,
calls real runtime cleanup and transfers without returning on success. Error
unwind restores the original segment/register frame, invokes near callee-pop
IOERROR, and returns with the original near cdecl convention. No defensive
checks, new allocation rollback, initialized scratch or physical DOS execution
claims are added. All code regions, local branches and transfer boundaries are
checked against the actual native output and fixed target.

Actual private inputs in `.analysis/work/`: `mainl-exec-build.json`,
`mainl-exec-native.json`, `exec-source.asm`, `exec-library.rsp`, `exec-link.lnk`,
and both `exec-roundN.obj/.lib/.exe/.map` vectors. The previous farheap source,
report and native objects remain required inputs. Whole-product source ownership
and physical DOS behavior remain open.
