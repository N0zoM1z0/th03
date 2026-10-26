# MAIN player state update: existing-source ownership

Reviewed2026-10-26 against pinned Japanese MAIN (`candidate-local-attested`).
This closes ownership of already reconstructed C++, not a new implementation
or an original filename/source-spelling claim. Executable source is unchanged.

## Boundary and native producer

`core.cpp` → `state.inl` → `update.inl`: CS096E:4363..47B5, loadDA43..DE95,
fileF2A3,1,106 bytes. All375 decoded instructions agree; no inline DATA/switch
storage or shared tail. All jumps remain internal instruction boundaries.
The final instruction is RET4 at47B2. One MZ relocation is at096E:4562.

| Load extent | Bytes | Ownership |
| --- | ---: | --- |
| D6D4..D7F0 | 284 | Existing player-move |
| D7F0..DA43 | 595 | Existing Hyper dispatch |
| DA43..DE95 | 1,106 | New distinct player-state-update owner |
| DE95..E0F7 | 610 | Unaccepted render131/overlay209/knock151/bomb119 |
| E0F7..E266 | 367 | Existing distinct player-state owner |
| E266..E313 | 173 | Unaccepted stage-shot sprite context |

Complete3,135-byte core checks retain native TC4 CODE-only segments,
records1024/1022/1024/65,all21 publics,complete MAP placement,raw bytes and literal
ordered relocations. Containment grants no context ownership or DATA/BSS credit.

## Compact behavior and ABI review

Real round calls push a WORD input then near player65A6/6626. Entry reads BP+6
into DI and BP+4 into SI,uses six local bytes,preserves SI/DI/BP and returns RET4.
It independently computes `player_cur` (DS:6588) using live byte `pid.current`
and128-byte player stride. Do not equate this shared alias with the parameter.

- Byte invincibility/damage timers precede defeat/lose gates. Four base-speed
  components feed the near Hyper callback at member+64 (WORD).
- Human movement masks/retries only its first invalid direction. CPU handling
  uses its WORD frame,marker-dependent shot interval and64-entry charge ring.
  Byte/word wrap,repeated PID reads and source branch ordering are preserved.
- Knockback clears charge and suppresses collision. Charge accumulation,
  automatic release and400/800/C00/1000 thresholds select shot/gauge/boss actions.
  Charge callback member+68 is a far DWORD pointer,two WORD coordinate arguments.
- Shot release,bomb,Hyper drain,collision/damage/defeat transitions preserve order.
  Signed halfheart subtraction/clamp is distinct from byte timers. Final patterns
  depend on velocity,page,Hyper and invincibility.

Direct calls: movement403E/3FF4,CPU2E6A,knock4909,shots5057,bomb49A0,
hittest4A17,hitcircle20D3,damage4AF5,HUD224F,lose-update29F8; sound far0E8F:034A.
Declared samecodeseg far/Pascal APIs retain far-return contracts through native
relaxation. Near Hyper/far charge widths agree with packed-field assertions.
No callee or callback body is credited by its call site.

`shot_release_frames` is existing root BSS1D56:4B9C. Staging reversibly splits
five reserved bytes1+2+2 and checks all other allocation syntax unchanged.
No storage is introduced; the stale pending-link comment is corrected.

Player-specific input,charge,attack,damage and animation transitions,real game
callers and shared game-state/callback accesses positively classify this body
as authored game code,not generic library/CRT/compiler support.

## Evidence and limits

Existing full two-cold replay passes all11 configured exact gates,repeats100
outputs/98 objects in99 phases,and retains99 extents/76,423 bytes plus all1,553
literal ordered MZ entries. Prior98 extents remain unchanged. Full-product
exactness is false: EC2D and the MZ header differ. VS stays prebuilt vendor context.

`config/main_work/player_state_update_acceptance.json` binds current evidence;
replay with `scripts/replay_th03_main_native.py`. Historical recipes/observations
are unchanged. Existing round runtime stubs this callee: no executed-body claim.
Runtime/ABI probes are supporting,not extra mandatory gates. No new test suite
or harness. Full CI is pending at writing; final receipt is reported separately
rather than editing files after validation.
