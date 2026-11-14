# Native performance and audio comparison — 2026-11-14

TH03 retains TH04's main synthesis/transport fixes and now also applies the
host scheduling and menu optimizations identified in the `ac353a3a` audit.
TH04 reference revision is `1ba7107`. The DOS targets, game updates and PMD
implementation are unchanged.

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

## Implemented host and menu changes

`win32_frame_timer.hpp` uses a process-local high-resolution one-shot timer and
message-aware waits. Creation or arm failure falls back to a coarse
message-aware wait; `TH03_LEGACY_WINDOW_TIMER=1` forces that fallback for checks.
No global timer-period request is made. The window loop drains at most 64
messages before checking its simulation deadline.

`frame_schedule.hpp` admits at most four overdue ticks per wake. A remaining
backlog is rescheduled one period after the current host time. Discarded wall
time does not advance game counters or synthesize skipped PMD ticks. Rendering
presents the latest completed state after a batch. The existing 16,667 us host
period and 60 Hz audio clock remain unchanged. A host stall can still interrupt
playback while work is blocked; the correction bounds recovery afterward.

`ViewFrames` owns the current display image. OP title/main/Option/versus menus
reuse it while phase, screen, request, selection and option fields agree.
Idle counters, RNG, audio and attract entry continue ticking. Other scenes
remain dynamic. Win32 expose/resize paints use the owned image; SDL refreshes
its cached texture on expose/resize. Painting never repeats game updates.

Menu conversion computes 16 colors once, expands both packed pixels together,
and uses the same colors for OPWIN. In the same Windows Release probe, median
batch-average TL02.PI conversion falls from 0.825 to 0.136 ms/frame. Each result
is nine batches of 100 frames; complete pixels agree. This measures the CPU
conversion kernel rather than the whole application.

## Verification

Real Win32 tests use owned inactive desktops, the same current core with
old/new `view.cpp`, and PMD routed exclusively to a simulated 48 kHz consuming
device through production `audio::Output`. They resize and close each window:

| Observation | Old host loop | New host loop |
| --- | ---: | ---: |
| Static title render calls over about 3.5 seconds | 217 | 1 |
| Animated Music Room render interval p95 | 22.04 ms | 17.07 ms |
| Longest consecutive render burst below 5 ms after a 700 ms stall | 20 | 1 |
| Dropped stereo frames in the stalled run | 25,600 | 0 |

All generated frames in the new stalled run are accepted. Forced coarse-timer
fallback also creates/resizes/closes normally, with zero simulated audio drops.
These are rendered Windows controls with a fake audio device, not speaker tests.

Private Xvfb before/after tests exercise actual menu keys, rank/sound/key-mode
changes, resize, unmap/remap and exit. All seven complete RGB captures and saved
configuration bytes agree. Original Japanese MAINL decoding still agrees on
all 128,000 PI bytes, and the complete 640x400 menu agrees with the DOS frame.
The ordinary 79,298-input PMD86 clear also retains its preceding diagnostics,
63,438,399 sample frames, full final picture and YUME.NEM/YUME.CFG bytes.

Focused maintained checks:

```sh
th03-port64-checks --frame-policy
th03-port64-checks --menu-cache /path/to/zun.hdi /path/to/FREECG98.BMP
```

Both checks pass on Linux and Windows. They cover early message wakeups,
300 ms stalls, continuously slow work, all visible menu fields, versus,
request/scene invalidation, animated scenes and idle entry into attract mode.
Standard portable/PCM/device contracts also pass. Private probe sources and
results are in `build/host-perf/`; the earlier primitive-only timing probe is
in `build/perf-audit/`. Recompile a probe for the product under investigation.
Raster hot loops remain a profiling opportunity; no battle frame-budget overrun
was established by this work.

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
