# Gauge and shared Extra Attack: natural native guards

The Gauge charge helper now has separate early returns for active Hyper
and an already-full Gauge. The compiler still emits the same short-circuit
behavior, unmodified 16-bit compound addition and post-add saturation.
The shared far-Pascal Extra Attack dispatcher uses a natural `!pid` branch
while retaining the two 16-bit coordinate copies and both callback ABIs.

Both original physical owners (`p_gauge`, `p_exatt`) pass the two-round
TC4/TLINK comparison at `af1169a`: 96 CODE bytes, three ordered native
fields and the full Japanese MAIN loaded image and relocations.
