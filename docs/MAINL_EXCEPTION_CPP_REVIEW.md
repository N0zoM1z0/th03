# MAINL natural C++ allocation and exception candidates

`new.cpp`, `xalloc.cpp` and `xmsg.cpp` recover the high-level allocation/message
policy and let the compiler emit its actual copy constructors, destructors,
exception scopes and type records. They are source candidates. No new source
bytes are accepted: complete initialized payloads and whole EXE/MAP do not match.
The existing205 owners/272 procedures/34,688 accepted bytes remain unchanged.

Operator new converts a zero request to one,tries malloc,and calls the installed
far handler before retrying. A null handler permits a null return. The default
handler throws the static xalloc("Out of memory",0); the requested-size field is
not rewritten by operator new. Set-new-handler returns the previous pointer.
Xalloc initializes its xmsg base and size,then raises by value. Xmsg owns a distinct
string object. Its copy constructor deep-copies the message; assignment checks
self-identity,then deletes before allocating the replacement. That original
exception-safety behavior is preserved.

Original module boundaries are754/513/955 bytes in CODE-class segments. Actual
instruction ownership is508/355/700 bytes in7/4/5 far procedures;246/158/255 bytes
are inline cleanup/type/scope data. The first xmsg constructor is167 CODE bytes,
followed by a36-byte cleanup record before the next public method. Linear decoding
through these records incorrectly invents instructions. The new module additionally
has DATA24,INIT6 and EXIT6. Its DATA has only18 initializer bytes; the first6 bytes
reserve the static object without an OMF initializer. These distinctions give no
new exact credit while the maintained producer remains unmatched.

The retained current profile is large-model8086 C++ with `-O -r- -Z -xc -Vs
-zC_TEXT`. Compatible exception prologs recover helper-based exception state;
local inline emission avoids separate communal code segments. The flag families
are described by the archived [Borland4.0 guide](https://bitsavers.org/pdf/borland/borland_C%2B%2B/Borland_C%2B%2B_Version_4.0_Users_Guide_Oct93.pdf),
[compatible-exception documentation](https://bitsavers.trailing-edge.com/pdf/borland/borland_C%2B%2B/Borland_C%2B%2B_Version_5_Users_Guide_1997.pdf)
and [local virtual/inline emission documentation](https://bitsavers.trailing-edge.com/pdf/borland/borland_C%2B%2B/Borland_C%2B%2B_Version_3.1_Users_Guide_1992.pdf).
Actual compiler output,not the manuals,determines the current result.

Current TC4 emits735/502/935 CODE-segment bytes. All original public/external
identities and all122 field counts are reproduced,but this does not establish
byte or layout equality. For example,xalloc raise moves from127 to123; the
original constructor saves unused SI/DI while this profile omits those saves.
Other helper instruction choices also differ. The tested automatic/declared/off
register profiles,debugging,optimization and DLL-class variations did not close
native output. DLL-class mode also changes public mangling and is not retained.
The installed compiler's compatibility with the original library must not be
assumed from a matching banner or API header.

Literal MZ order is another constraint: xalloc/xmsg vectors descend within each
module. Direct TCC output keeps this form,while ordinary TASM output observed in
the diagnostic uses another order. Matching instructions through edited assembly
would still require a genuine native relocation-order solution. No object edits,
relocation sorting,unused source variables or padding are used to force equality.

Two actual compiler/TLIB/TLINK rounds use the maintained sources,all recorded
consumed SDK headers and19 validated reused natural objects. A normal893-member
library contains28 source providers; all member positions and871 other current
member payloads remain unchanged. Whole three-OBJ/LIB/EXE/MAP vectors repeat.
Both full EXE and full MAP comparisons fail. The diagnostic reviewer validates
source/flags/SDK/driver/output binding and explicitly requires source_acceptance
false and accepted_source_bytes0. Reproducibility never upgrades these candidates.

Six source-present ledger extents cover the three original module boundaries
and new's DATA/INIT/EXIT:2258 gross bytes,not newly accepted CODE. Source presence
becomes240 extents/47,388 bytes. Accepted publication and its verifier inputs
remain byte-for-byte unchanged; old cold/source/tools and exact scopes are reused.
No full cold/DIET or ancestor runtime replay is run. The next source question is
which original compiler/ABI settings produced the extra register preservation
and helper layout. Keep current source candidates and raw failed replay vectors
available for that investigation; do not replace the fixed target.
