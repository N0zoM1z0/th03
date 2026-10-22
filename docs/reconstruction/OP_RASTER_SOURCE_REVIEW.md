# OP raster source checkpoint

Two complete authored functions are maintained in their original GAME3 C++ translation units:

- nopoly_B_put: decoded0990:0CF6,30 bytes,src/op/music/nopoly_blit.inl,original th03/op_music.cpp.
- box_column16_unput: decoded0990:180A,94 bytes,src/op/menu/column_restore.inl,original th03/op_main.cpp via th03/op/m_main.cpp.

The additive stage_th03_op_raster.py substitutes only each complete source function with its maintained include. It requires original full carrier and function hashes, preserves every byte outside those scopes and never changes prior stagers. Its compose API accepts the prior source dictionary; its payload API requires an explicit original source reference. There are no opcode arrays, byte emission, padding compensation, fake frames or linked-output edits.

Symbolic inline ASM naturally emits the five target instruction bytes: XOR DI/DI and SI/SI use31 rather than33; ADD DI/AX uses01C7 rather than03F8; XOR AL/AL uses30 rather than32. TC4 owns real BP frames, SI/DI preservation and near RET/RET2. nopoly_B is a segment-only pointer and incoming DF is unchanged. The column function retains the original BOX_BOTTOM versus BOX_H bug and beyond-VRAM accesses; no real-device correctness is claimed.

## Historical native outcome and separate correction

Three actual native phases, two original compiler invocations and one context link, exited0 with certain owned cleanup. Exactly25 other project objects were retained. Both complete new functions'124 bytes and zero owned ordered relocation words match the decoded target; all42 prior bodies/12816 bytes retain baseline raw bytes, literal relocation order and MAP positions. The resulting executable SHA256 is ca6786f03b28415da3601f8e49fe5dac6ec908dae0d0f420dd701ac58b4e2275.

The original runner completion is nevertheless false. Its final aggregation incorrectly required every prior owner to equal target relocation order, including the already-known selection negative. The original manifest, runner, verifier, completion and failed linked report remain immutable.

A separate offline replay reproduced that original report exactly. Correct aggregation independently observes each prior target-order predicate from the actual baseline, requires preservation rather than erasure of prior negatives, and separates prior preservation from new raster success. A dated parent-run post-diagnostic audit additionally checked the originally skipped source/input/tool-mtime/registry/output-membership guards. Its report is .analysis/op-raster-offline-correction-v01/audit-result.json, SHA256 c13d4c4c4009a6da64d057dc720ad18b515ab4098986a43a6a09a4dccd1572cd. This does not turn the original failed completion into success.

Maintained replay binds actual maintained source and real import/helper closure before imports. It does not rerun obsolete historical whole-tree HEAD guards, live registry checks, native compilers or models. The successful post-diagnostic current-state audit remains dated evidence, not a claim about a later machine state.

Only five program bytes change from the actual baseline. The remaining programDD95 target90/candidate00 byte is vendor EVEN alignment with zero authored credit. The prior selection target-order negative and313 global literal relocation-order differences remain explicit; relocation lists are never sorted. No canonical packed file offsets, whole-product equality, runtime/device, full cold repeat, native/model rerun or exact acceptance is claimed.

After the five-helper source checkpoint, the sparse two-row update yields44/45 OP source units and12940 scoped function bytes, exact zero. Earlier candidate failures and analysis evidence are retained as historical evidence, not silently reclassified.
