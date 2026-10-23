# Source layout

`src/main`, `src/op`, `src/mainl` and `src/zun` own the four TH03 products.
`src/shared` contains proved shared code. `.c`, `.cpp` and `.asm` are translation
units; `.inl` files are bounded includes. Use `compat/rec98` for explicit reference
forwarding. Keep private tools/targets/generated output out of Git.
