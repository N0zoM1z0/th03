# Signed polar, PI reload and DOS handoff: exact native ABI forms

Three independent leaf owners now have more direct C++ expressions while
preserving their complete original Turbo C++ 4.02 output:

- `polar` (`af1322h`, 26 CODE bytes, no fixups): compute `center +` the
  signed 32-bit radius/ratio product shifted arithmetically by eight bits.
  The far-cdecl signed 16-bit return still truncates the result. Do not
  replace the shift with `/256`, which rounds negative values differently.
- `pi_load` (`af1322i`, 70 CODE bytes, six ordered fields): explicitly retain
  the 16-bit stack result, release the old PI resource, and pass
  `pi_headers + slot` and `pi_buffers + slot` to the real far-Pascal loader.
  This is native-equivalent to the old array subscripting without hiding
  the two independent address calculations.
- `execl` (`af1322j`, 79 CODE bytes, 11 ordered fields): pass the executable
  filename twice as explicit `char far *`, followed by the original four-byte
  far-null vararg terminator. The 16-bit SDK needs non-const `char *`
  arguments; the casts discard const without losing the pointer segment.
  The two MRS frees and original DOS cleanup order are unchanged.

Each source bound to its own two-round native TC4/TLINK receipt and identical
full Japanese MAIN image and ordered MZ relocation vector. Joint stage
`af1322g` recompiled these three leaves plus the current Rikako BOSS:
**1,852 CODE bytes, 232 literal ordered native fields and 11 PUBLICs**
matched in both complete normal MAIN links. No full cold replay ran.

Negative trials explain why the natural expressions have these limits.
`af1322d` removed the casts on `execl` and the original compiler rejected
`const char *` for both non-const SDK arguments. `af1322f` cached the PI
header in a pointer local: TC4 enlarged the stack frame, produced 72
instead of 70 CODE bytes and changed the native fixup count from six to
five. The correct independent address expressions were restored.

Read-only recheck of current leaf scopes:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1322h af1322i af1322j
```
