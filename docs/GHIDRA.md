# Headless analysis

Use `python3 scripts/ghidra.py ARTIFACT check` before database observations.
Targets are pinned in `config/targets.toml`; projects live in `ghidra-project/`
and exports in ignored `.analysis/ghidra/`. Run analyzeHeadless with Java
headless mode. Use `_JAVA_OPTIONS="-Xmx768m -XX:ActiveProcessorCount=1"` for
bounded resource use. Automatic functions and decompiler output are provisional.
