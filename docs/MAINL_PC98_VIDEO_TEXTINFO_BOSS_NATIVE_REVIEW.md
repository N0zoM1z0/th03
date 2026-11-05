# Original PC-98 video-mode translation and gettextinfo boss — after456

Original Japanese Borland CRT member `vidinfo` (index **570**) is now
maintained as real native [8086 source](../src/mainl/crt/vidinfo.asm).
It contains a private near video-mode translator (CODE+0, Pascal
cleanup) and the public far `_gettextinfo` at CODE+89. The actual
translator handles the original `__conio_type == 2` display-mode
bit permutation using a meaningful 8-entry word table; other modes
return the original input. The far public reads real PC-98 `__video`
window coordinates, uses `___get_windowy2`, `___get_screen_height`
and the near `__WHEREXY` helper, preserves original one-based
screen coordinates, and fills the caller's 13-byte data structure.

Native TASM produces all **231 original CODE bytes** and **16 typed
initialized DATA bytes** (the true mode-permutation words
`0,1,4,5,2,3,6,7`). The original `_TEXT`/`_DATA`/`_BSS`
segments, public/import interface and DATA-first group match.
All **14 OMF relocation sites, kinds, targets and addends** match.
**Thirteen of the 14 relocation frames** also match exactly.
At CODE+192 the original Borland `__WHEREXY` near imported call
uses TARGET-frame method 5, while TASM's equivalent near call
uses CODE-frame method 0. The builder and test only permit this
single independently attested site/target pair; all other OMF
fields stay strict. Neither literal ordered FIXUPP identity nor
complete raw Borland OBJ program equality is claimed.

An initial copied stage descriptor incorrectly expected the previous
member's 230-byte `_TEXTA`, not this member's original 231-byte
`_TEXT`. This was corrected against original library and retained
vendor OBJ evidence before building; no native comparison was weakened.

After456 validates the unchanged after455 source-bound carrier and
performs two fresh native TASM/TLIB/TLINK rounds, retaining entire
raw OBJ/LIB/EXE/MAP pairs, logs and source/driver hashes. Both
Japanese decoded MAINL EXE/MAP are byte-for-byte target-equal:
67,372 EXE bytes, 677 ordered MZ relocations. The working CRT
reaches **664/893** source-linked original members, **178,363 CODE
bytes**, and 229 contextual vendor programs. This remains bounded
working source evidence, not new formal Factory acceptance or
a full cold replay.

Focused review: `scripts/review_th03_mainl_after456_work.py
pc98-video-textinfo-boss`; tests: `tests.test_mainl_after456_work`.
