# Original DOS perror: exact 145 CODE + 19 initialized DATA and 50-source link

The original Borland DOS far-cdecl perror, CRT member269, now
has maintained 8086 source at src/mainl/crt/perror.asm. The actual
function checks the near _errno and __sys_nerr values, selects
the real far error-message pointer from __sys_errlist or the
default unknown-error message, optionally emits the supplied
prefix, and prints the original error message and newline through
the real far _fputs provider and __streams+40 stream pointer.

The original 19 bytes of initialized DATA are genuine message
strings, not padding or executable opcode copies: "Unknown error"
with NUL, ": " with NUL and a final LF/NUL. Its code consists
of 59 real 8086 instructions. The maintained source uses actual
external symbols and 18 non-overlapping instruction blocks
positioned at their original CODE offsets to preserve the
compiler's descending OMF writer order.

Native TASM reproduces **all145 original CODE bytes, all19 DATA
bytes, all17 literal ordered OMF FIXUPPs** and every original
PUBLIC/EXTDEF/segment-group property. These fields include
GROUP-framed _errno, __sys_nerr, __sys_errlist, __streams+40
and all three message-label offsets, as well as TARGET-framed
far _fputs calls. The original one public _perror at0, empty
BSS and original DATA-before-BSS group 08ff02ff03 match.

The scoped source-only builder inherits the 48-source time
conversion working library and original 38-byte strlwr member.
It assembles the two genuinely new members into the original
893-member Borland CRT, leaving **843 other original member
program records byte-identical**. Two complete native TASM/
TLIB/TLINK rounds produce the **entire original 67,372-byte
decoded Japanese MAINL EXE** and complete MAP raw-equal,
including all **677 MZ relocation entries**. The working
50-source library generates **25,630 exact original CODE bytes**
along with the new19 exact initialized DATA bytes.

A previous experimental attempt to count strncat as new was
correctly rejected by strict CRT program-record comparison:
strncat is already one of the 48 inherited source owners.
The added builder source guard explicitly rejects replacing
any already reconstructed owner in a new extension. Its
redundant untracked ASM experiment was discarded; no duplicate
bytes or ledger promotion are claimed.

The inherited near-frame differences for timecvt, original
fopen OMF order and fclose near-frame remain open and separately
tracked. The fixed Japanese target, accepted28-provider CRT,
published211-owner MAINL ledger and original cold pair are
unchanged. Source-only native product proof does not confer
formal accepted byte credit. No full cold/DIET replay occurred.

Affected-only verification:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_posttimecvt_work.py strlwr-perror
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttimecvt_work.py strlwr-perror
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttimecvt_work

Complete two-round native OBJ/LIB/EXE/MAP vectors and all writer
logs/receipts are preserved under
.analysis/work/posttimecvt-strlwr-perror-*.
