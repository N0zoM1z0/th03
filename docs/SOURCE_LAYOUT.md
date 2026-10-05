# Source layout

| Directory | Product ownership |
| --- | --- |
| `src/main/` | MAIN.EXE gameplay subsystems |
| `src/op/` | OP.EXE opening and menu |
| `src/mainl/` | MAINL.EXE ending/results |
| `src/zun/` | ZUN.COM launcher/resident code |
| `src/shared/` | Proved shared TH03 declarations and code |
| `compat/rec98/` | Explicit temporary declaration forwarders only |

Place files by artifact and subsystem, never reconstruction state. Record
translation-unit splits and linker order as replay inputs. Do not bulk-import
TH04 implementations or infer TH03 semantics from matching names.
