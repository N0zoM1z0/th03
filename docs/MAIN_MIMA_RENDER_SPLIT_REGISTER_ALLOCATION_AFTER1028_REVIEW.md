# TH03 MAIN Mima split renderer: parameter register allocation probes

`mima_render_split()` is a 223-byte near Pascal leaf. Its original code loads
the stack-passed distance into SI and keeps the first polar X result in DI;
the two registers stay distinct across both half-sprite draws. The maintained
source already expresses this with:

```cpp
register int split_distance = distance;
register screen_x_t left;
```

Two alternative natural declarations were tested against the complete
`ba_mima` owner and rejected:

- `af1028a`: make the Pascal `distance` parameter itself `register int` and
  remove `split_distance`. The compiler allocated the parameter to DI, which
  displaced the left-coordinate register and changed nine CODE bytes.
- `af1028b`: keep a plain non-register `int split_distance = distance` local.
  The complete `ba_mima` CODE payload also differed.

Both experiments were reverted. Keep the explicit register local: the target
needs distance in SI and left in DI, and the parameter-qualified form does not
preserve that allocation under original Turbo C++ 4.02.
