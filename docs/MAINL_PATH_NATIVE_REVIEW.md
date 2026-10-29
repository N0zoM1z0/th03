# MAINL DOS path normalization

Four complete maintained TUs add1247 CODE+22 initialized DATA bytes in six
library extents,covering nine procedures. The complete `fullpath` module at
0000:4706 is834 bytes:31-byte near pop2 separator predicate,58-byte near pop8
SBCS separator predicate and745-byte far cdecl `__fullpath` coordinator. Companion
modules are `getdcwd`157 at4A48,`_pathops`208 at430C and `dosgdriv`48 at2F68.
The path module's DATA16 is at0E3F:1158 and INIT6 at0E3F:132A.

The coordinator always allocates a161-byte temporary. Its signed character/ctype
mask detects an explicit alphabetic drive; toupper supplies the one-based drive
number,while the original letter remains available for the absolute-path prefix.
Otherwise DOS supplies current drive. Relative input is appended to that drive's
current directory,adding a backslash when needed. Absolute input receives the
drive/colon prefix. Unchecked strcpy and all16-bit offset-only cursor arithmetic
remain intact. Slash and backslash retain their original characters.

The second pass copies characters,collapses dot and parent components only at
SBCS separator boundaries,and preserves DBCS lead/trail pairs. A parent above
an SBCS drive root fails after freeing the temporary. Termination removes a
trailing separator but retains the drive-root backslash. A supplied output buffer
must fit strlen+1; success copies and frees the temporary. With null output,
the function returns realloc(temp,strlen+1),retaining original error behavior.
The maximum-length argument does not add bounds checks to temporary copying.

Current-directory query preserves its70-byte unchecked local path buffer and
WORD drive. It uses DOS19h for drive0,DOS47h for the directory,and requires
strlen(path)<capacity. Too-small capacity writes ERANGE34; failed optional malloc
writes ENOMEM8. DOS failure returns null without an added errno translation.
Drive get/set wrappers preserve one-based public drive numbers and DOS zero-based
conversion,including the set-drive service's returned count through a far pointer.

The73-byte near path initializer preserves its original8086 register save sequence,
including PUSH SP and the corresponding discarded POP BX. If the range vector is
zero,it requests DOS6300h ranges. Carry,same returned segment as DS,or SI=FFFF
select the local empty fallback table. The vector is an initially zero far pointer;
the twelve-byte fallback is six zero lower/upper range pairs with a terminating
first pair. These16 bytes are genuinely initialized DATA,not padding or BSS.
The37-byte far lead-byte routine walks ranges; the98-byte far SBCS routine tracks
SBCS/lead/trail states through the candidate offset. NUL clears the state.

One bounded actual-native probe runs the near SBCS separator helper plus its two
real DBCS callees. A supplied ordinary DOS-style range table classifies81h as a
lead. Candidate backslash after81h returns false; after ASCII A it returns true.
Both executions return and consume the actual8 helper argument bytes. This
resolves the DBCS separator/ABI question without a DOS,heap or fullpath model.

INIT6 stores type0,priority15,the near initializer offset and a zero segment slot.
The actual retained startup dispatcher uses a near call for type0. Its offset
reference has no segment relocation. The sole real new MZ relocation is0000:433F,
the initializer's DGROUP segment immediate. Explicit DGROUP qualification emits
exactly the original field frame; no equivalent-frame exception is needed.

All four fresh objects match complete initialized payloads,31 field identities,
publics,segment sizes,BYTE/WORD alignments and original group orders. Both emitted
field streams remain available without sorting MZ relocations. Twenty ordinary
far calls naturally relax; all fields independently resolve into complete linked
CODE/DATA/INIT bytes and literal scoped ordered MZ vectors. Full dense procedures,
local branch destinations,public entries and actual near/far cleanup are checked.

Two actual TASM/TLIB/TLINK rounds compose fifteen source CRT providers:four new,
five validated reused natural pairs and six retained source providers. All893
normal library positions and884 other current member payloads remain unchanged.
Whole four-OBJ/LIB/EXE/MAP vectors repeat; complete decoded EXE/MAP match the pinned
Japanese target/retained MAP. The36 project objects and938 cold outputs/source/
recipe/tools remain unchanged. No full cold/DIET or ancestor runtime replay is
needed. The frozen cold recipe remains six CRT replacements; the selected recipe
establishes coexistence of fifteen providers without rewriting earlier hashes.

MAINL now accepts193 extents,259 procedures/entries and32,870 bytes:
30,962 CODE+1,908 DATA;16,695 authored+16,175 library. Previous187 owner records
and nested scopes are unchanged. Source presence becomes222 extents/43,312 bytes,
including overlapping historical aggregates that gain no duplicate accepted
credit. No source padding,object patches,defensive changes,physical DOS execution
or whole-product source acceptance is claimed. Further CRT/ownership work remains.
