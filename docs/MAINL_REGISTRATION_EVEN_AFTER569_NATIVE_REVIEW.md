# MAINL registration DATA: original word alignment with natural TASM EVEN

The after554 source-backed registration DATA bank contained **303 initialized
semantic bytes** but the original TASM context object also contained a final
initialized 00h byte at DATA+303. The normal linker supplied an equivalent
gap before the next word-aligned contributor. This preserved the complete
Japanese MAINL output, but did **not** prove source ownership of the
historical extra byte.

The maintained, human-readable source file
src/mainl/data/registration_even.asm is a narrowly bounded alternate
version of the same Japanese name/file bank. It preserves every original
statement, CP932 transport, true mutable near-data pointer relocations and
font constants, and adds one ordinary **TASM EVEN** directive immediately
before the original END. The after554 historic source stays unchanged to
preserve its existing acceptance/receipt bindings; the native source
variant is independently auditable against the older file.

Experimentation with TASM5 established an important difference:

- EVEN / ALIGN 2 both emit the initialized original 00h and extend the
  original DATA allocation from 303 to 304 bytes.
- The previously tried EVENDATA expands the DATA segment extent but does
  **not** produce the missing initialized byte and fails the original
  complete object initializer comparison.
- No raw target byte, appended 0 directive, output/object patch or manually
  copied suffix was used to make the alignment match.

The natural EVEN source was compiled in two separate native TASM rounds,
with the original mutable font codes staged and all other source modules
taken from the actual after566 input-scan parent. Each produced registration
OBJ agrees with the original 304-byte DATA initializer, **both literal
ordered OMF relocations**, **35 PUBLIC definitions/positions**, all segment
geometry and all nonvariable remaining OMF metadata. The complete original
**67,372-byte Japanese MAINL decoded EXE**, including all **677 ordered MZ
relocations**, remains byte-equal in both normal TLINK rounds. Except for
the one registration DATA contribution size changing from 012F to 0130,
the full original source-bound MAP coordinates/rows remain unchanged.

This closes the additional original initialized DATA byte as a genuine
assembler alignment result. It is **not a newly recovered function** nor
new authored game credit; the existing historical source and Factory
publication are not repinned. The 37,975-byte original DIET stored file is
not repacked here, and no whole cold replay was performed.

Read-only scoped native review:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_registration_even_after569_work.py

Driver: scripts/build_th03_mainl_registration_even_after569_work.py
Native stage: .analysis/work/mainl-register-even-after569-native-build.json
Reviewer: .analysis/work/mainl-register-even-after569-native-review.json
All raw OBJ/EXE/MAP rounds and native writer logs remain retained.
