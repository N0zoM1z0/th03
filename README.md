# 東方夢時空 ～ Phantasmagoria of Dim.Dream

This is the `port/modern-64` branch. Native C++17 menus, selection, introductions
and battle, results and score/continue flows build for Linux x64 and Windows x64; [portable status and commands](docs/PORTABLE.md)
describe the checks and unfinished game flow. The DOS reconstruction
is retained on `main` and remains the behavioral baseline.

Agent workflow: follow the highest-priority requirements in [AGENTS.md](AGENTS.md). Use affected exact checks and searchable Markdown knowledge; ordinary notes do not require full CI or replay.

<p align="center">
  <img src="resources/title-screen.png" width="640" alt="Original Japanese TH03 title screen">
</p>
<p align="center">
  <img src="resources/progress.svg" alt="TH03 reviewed reconstruction scopes">
</p>

This repository reconstructs the original Japanese PC-98 **Touhou 3:
Phantasmagoria of Dim.Dream**.

[Progress](docs/PROGRESS.md) · [Handoff](docs/RE_HANDOFF.md) · [Workflow](docs/RE_WORKFLOW.md) · [Architecture](docs/ARCHITECTURE.md)

Built on [ReC98](https://github.com/nmlgc/ReC98), with workflow reference from
[our TH04 reconstruction](https://github.com/N0zoM1z0/th04).
