# Native performance and audio comparison — 2026-11-14

TH03 `18a00eba` already includes TH04's main synthesis and transport fixes.
The remaining shared opportunities are host frame scheduling and some rendering
work. This comparison uses TH04 `1ba7107`, including its October 27 audio,
rendering and UI corrections. No product source or deployed executable changed.

## Already present

After removing only the adaptation banner and namespace, TH03's
`audio_device.cpp`, `audio_output.cpp`, `pmd/pmd_pcm.cpp`, `pmd/pcm_filter.hpp`
and both modified ymfm headers equal their TH04 counterparts. The output header
only additionally changes an include path. This retains:

- Immediate commitment of ordered FM key-off/on edges at one IRQ timestamp.
- Corrected FM/SSG mix, 256-tap antialias filter and fractional DC blocker.
- Exact 3,993,600/7,987,200 Hz board clocks and the PMD86 default launcher.
- WinMM fragment coalescing into 1,024-frame blocks, 16 stable headers,
  pending-tail accounting and bounded driver ownership/cleanup.

TH03's song-start/stop differences are intentional adaptations to its own PMD
residents, previously checked against their original ordered writes. Do not
replace those functions wholesale with TH04 versions.

Windows PCM and fake-device checks pass again; Linux's corresponding two CTest
checks pass. They cover repeated versus held FM attacks, mix/alias controls and
fragmented-buffer ownership. On this host, synthesizing ten logical seconds of OP.M takes about 219 ms CPU
with PMD and 250 ms with PMD86 (480,000 stereo frames each). These are song-specific
synthesis observations, excluding transport, graphics and hardware listening.

TH03 also already converts the 16 live colors once in `Canvas::frame`, and its
Japanese text renderer reads a glyph row once per scanline. Those TH04-style
improvements do not need another implementation.

## Remaining differences

| Area | Current TH03 evidence | Next useful action |
| --- | --- | --- |
| Windows waits | `view.cpp` uses `sleep_until`, without TH04's high-resolution message-aware timer | Adopt the host timer policy while retaining TH03's simulation/audio semantics |
| Overdue deadlines | Every loop adds one period; there is no catchup bound or resync after a long stall | Bound overdue work and test input, painting and audio queue behavior together |
| Static menu painting | Both backends redraw every refresh, including an unchanged title/menu | Cache unchanged visible menu state; retain animated scene updates |
| Menu RGB conversion | `pi_frame` computes RGB separately for every indexed pixel | Use a 16-color table and packed-pair expansion |
| Raster loops | Several BFNT, planar/MRS and picture paths retain per-pixel work | Profile actual battle/UI hotspots before choosing row or packed kernels |

A console-only Windows probe uses the production 16.667 ms deadline increment,
one CPU and below-normal priority. Each wait mode runs two passes, with 120
observations per pass after warmup. It compares the current standard-library
wait with a process-local high-resolution one-shot timer:

| Wait primitive | Interval p95 | Largest interval | Deadline lateness p95 |
| --- | ---: | ---: | ---: |
| Current `sleep_until` | 19.03–19.18 ms | 31.15–31.38 ms | 9.63–15.29 ms |
| High-resolution timer | 17.01–17.05 ms | 17.16–17.24 ms | 0.60–0.63 ms |

This reproduces timer-level jitter in a headless, process-local control. A
production change still needs a real private-window check, including GDI
presentation, delayed work and message responsiveness.

For TL02.PI, nine batches of 100 conversions have median batch-average cost
0.825 ms/frame in current `pi_frame`, versus 0.375 ms/frame in a scratch
16-color-table implementation. Complete output pixels agree. Existing
`Canvas::frame` measures 0.117 ms/frame on an indexed fixture. These are Release
CPU kernels, excluding GDI presentation and audio; they do not establish that
battle rendering exceeds its frame budget.

Probe source and output: `build/perf-audit/probe.cpp` and `probe.log` in the
native worktree. It links the existing Windows Release core/PMD/ymfm archives
and uses the external HDI/ROM.

## Different or unproven cases

TH04's Mugetsu-to-Gengetsu delay-2 inheritance bug has no corresponding boss
handoff in TH03. TH03's ordinary `RoundLoop::present` resets `reset_frames` to 1;
loss animation can request 2 again on its next update. No equivalent persistent
half-speed leak was identified here.

TH04's calibrated refresh period is 17.723227 ms; TH03 currently declares 60 Hz
in both host pacing and `Sound::refresh`. TH03's recovered initialization requests
640x400 through BIOS INT 18h, but that call alone does not establish its actual
GDC oscillator/totals. Check original TH03 raster timing before changing cadence;
copying TH04's period alone would also change game/music synchronization.

TH04 reference notes: [rendering and pacing](https://github.com/N0zoM1z0/th04/blob/1ba7107/docs/reconstruction/product/TH04_PORTABLE_RENDER_PERFORMANCE.md),
[audio fidelity](https://github.com/N0zoM1z0/th04/blob/1ba7107/docs/reconstruction/product/TH04_PORTABLE_AUDIO_FIDELITY.md),
[audio profile and WinMM packing](https://github.com/N0zoM1z0/th04/blob/1ba7107/docs/reconstruction/product/TH04_PORTABLE_AUDIO_PROFILE.md),
[UI row/bulk rendering](https://github.com/N0zoM1z0/th04/blob/1ba7107/docs/reconstruction/product/TH04_PORTABLE_UI_AND_INVINCIBILITY.md).
