# MAIN remaining player-family ownership

Reviewed2026-10-26 against pinned Japanese MAIN (`candidate-local-attested`).
Four disjoint native owners close nine **existing** C++ bodies:2,107 CODE bytes,
748 instructions. This is ownership recovery,not a new implementation or an
original source filename/spelling claim. Executable source is unchanged.

## Complete boundaries

All addresses below are load offsets; CS is096E. All branches land on decoded
instruction boundaries. These nine functions contain no inline table,alignment
byte or shared tail. Each entire function ends in the stated return.

| Owner / function | Load range | Bytes | Instructions | ABI |
| --- | --- | ---: | ---: | --- |
| render-knock-bomb / player_render | DE95..DF18 | 131 | 48 | near Pascal RET2 |
| player_overlay_render | DF18..DFE9 | 209 | 81 | near Pascal RET2 |
| player_knockback_update | DFE9..E080 | 151 | 58 | near Pascal RET2 |
| player_bomb | E080..E0F7 | 119 | 46 | near Pascal RET2 |
| stage-shot-sprites / stage_prepare_shot_sprites | E266..E313 | 173 | 46 | near noargs RET0 |
| round-results / round_objects_and_counters_reset | E313..E35B | 72 | 28 | near noargs RET0 |
| round_result_number_put | E35B..E3F2 | 151 | 68 | near Pascal RET6 |
| round_match_result_render | E3F2..E737 | 837 | 286 | near noargs RET0 |
| player-shots-add / player_shots_add | E737..E83F | 264 | 87 | near noargs RET0 |

The complete core3135 partition retains move284,Hyper595,state-update1106,
state367 and adds render/knock/bomb610 plus sprite173. Complete results1060 owns
its three functions. Complete shots449 retains the separately accepted185-byte
update/render suffix after new shots_add264; that suffix is not recounted.
Every overlapping global owner must equal this explicit partition. No generic
peer-exhaustion waiver or source-filename-based acceptance is used.

Native TC4 records remain core1024/1022/1024/65,results1018/42,shots449. All27
publics,exact MAP contributions,full physical OMF records,complete producer raw
bytes and literal ordered relocations remain checked. All three objects have
zero private DATA/BSS; external storage does not become owned by reference.

## Actual calls, widths and behavior

- Render/overlay real round-loop calls at CS0205/0210 and0220/022B push near
  player65A6/6626 after setting live byte pid.current. The four pointer APIs read
  BP+4,save SI/BP and DI when used,and RET2. Render's loss path pushes this and
  calls the accepted **near member** at2B68 (RET2),not a far callback. Normal
  drawing observes byte animation fields,WORD coordinates and live PID; overlay
  keeps signed subpixel shifts,gauge thresholds and four-frame animation.
- State-update calls knockback4909,bomb49A0 and shots5057. Knockback retains
  random quarter-circle selection at time64,byte length decay while time>32,
  far vector output and near movement/clamp. Time0 clears active then underflows
  its BYTE timer to255; no sanitization was introduced. Bomb checks live PID,
  bomb/hyper flags,updates bomb count or full-gauge Hyper and then story skill.
  Sound is far0E8F:034A. Native PUSH CS/near-call relaxation to HUD/bomb-explosion
  preserves their declared far/Pascal return contracts,not near callback ABI.
- Stage call0766 reaches4B86. Sprite preparation writes portA6 for page1 then0,
  making six far super_put calls on each page. It returns on page0. Twelve
  ordinary far relocation entries are retained; no hardware/pixel claim.
- Round preparation call0805 reaches reset4C33:32 shot records with14-byte
  stride and64 effects with48-byte stride have only their leading BYTE cleared.
  Existing DWORD round_frame6592,WORD round_or_result_frame6596 and BYTE reset
  flags6599/65A0 keep their exact widths. No wholesale record memset is inferred.
- Result call026E reaches4D12. Number helper4C7B reads signed WORD x/y/value
  at BP+8/+6/+4 and RET6; signed division and negative-value behavior remain.
  Result rendering uses far resident pointer at1D90,story bytes+33/+34 and
  128-byte player stride. BYTE statistics feed DWORD bonus products/accumulation
  at6890; signed division by192 precedes the **unsigned**65535 cap comparison.
  WORD step/low/high at688A/688C/688E and DWORD countdown retain widths. Actual
  text/gaiji far calls and relaxed HUD/high-digits/score calls preserve their
  own contracts; their bodies and near label strings are not new ownership.
- Shot creation uses live BYTE mode/PID,near player/shot pointers and14-byte
  records. Modes1/2/3 choose one/two/four pairs; Reimu mode4 calls actual far
 139D:113A twice with two WORD coordinates before the regular pair. Invalid
  nonzero modes deliberately retain uninitialized left/pair locals. The32-entry
  scan preserves signed clipping,allocation order,WORD velocity/so_pid and BYTE
  animation/PID writes. No speculative initialization or semantic cleanup.

These player animation,game-state,shot formation and result-score operations,
with actual game callers and fixed game structures,positively identify authored
code rather than CRT/library/compiler support. Referenced shared root DATA/BSS,
resident state,graphics providers and callback bodies remain separate owners.

## Evidence and limits

Existing full two-cold replay passes all11 configured exact gates and repeats100
raw outputs/98 native objects. Aggregate acceptance is103 extents/78,530 CODE
bytes/455 functions. New owner literal relocation counts are6/12/11/3; all1,553
whole-image literal entries match. EC2D and MZ header remain open; VS remains
prebuilt vendor context. Whole-product source exactness is false.

`config/main_work/player_family_acceptance.json` binds the source,recipe,cold
pair and native review. Historical pins/recipes/observations are unchanged.
Use `scripts/replay_th03_main_native.py`. Runtime/ABI probes remain supporting;
no new executed-body runtime evidence,test framework or harness is claimed.
Existing focused checks and full CI are pending at note writing; final receipt
is reported separately with no documentation edits after final validation.
