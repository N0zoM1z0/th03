"""Recreate MAIN's mixed source carrier from pinned reference and maintained code."""

from pathlib import Path
import hashlib
import re
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[2]

RECIPE_INPUTS = (
    "scripts/lib/main_work_stage.py",
    "scripts/lib/main_master_prefix.py",
    "scripts/lib/main_master_body.py",
    "scripts/replay_th03_main_exact_units.py",
    "scripts/lib/th03_yumemi_bomb_candidate.py",
    "scripts/lib/th03_player_tail_candidate.py",
    "scripts/lib/th03_cpu_model.py",
    "scripts/lib/th03_yumemi_charge_candidate.py",
    "scripts/lib/th03_charge_contract.json",
    "scripts/stage_th03_main_shotroot.py",
    "config/th03_main_exact_units.toml",
    "config/th03_main_link.rsp",
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def recipe_hashes():
    return {name: sha((ROOT / name).read_bytes()) for name in RECIPE_INPUTS}


def once(text, before, after):
    if text.count(before) != 1:
        raise ValueError("source anchor is not unique: " + repr(before))
    return text.replace(before, after, 1)


def native_carrier(raw):
    """Move complete procedures and expose existing storage, without adding bytes."""
    text = raw.decode("latin1").replace("\r\n", "\n")
    first = "public _main\n_main\t\tproc far"
    last = "_main\t\tendp"
    start, end = text.index(first), text.index(last) + len(last)
    text = (
        text[:start]
        + "; MAIN entry is supplied by src/main/core/entry.cpp.\n"
        + text[end:]
    )

    for first, last, names, comment in (
        (
            "sub_DA43",
            "player_bomb",
            ["sub_DA43", "_player_render", "sub_DF18", "sub_DFE9", "player_bomb"],
            "Five state",
        ),
        (
            "sub_E266",
            "sub_E737",
            ["sub_E266", "sub_E313", "sub_E35B", "sub_E3F2", "sub_E737"],
            "Five P_SHOT",
        ),
    ):
        start = text.index(first + "\tproc near")
        end = text.index(last + "\tendp", start) + len(last + "\tendp")
        if re.findall(r"^(\S+)\s+proc near", text[start:end], re.M) != names:
            raise ValueError("complete native procedure interval differs: " + first)
        text = (
            text[:start]
            + "; "
            + comment
            + " procedures supplied by maintained C++ source.\n"
            + text[end:]
        )

    start = text.index("sub_A21F\tproc near")
    end = text.index("sub_A289\tendp", start) + len("sub_A289\tendp")
    if re.findall(r"^(\S+)\s+proc near", text[start:end], re.M) != [
        "sub_A21F",
        "sub_A289",
    ]:
        raise ValueError("complete round-finish procedure interval differs")
    text = (
        text[:start]
        + "extern _round_start_next:near\nextern @ROUND_SCORE_COMMIT$QUI:near\n"
        + text[end:]
    )
    text = re.sub(r"\bsub_A21F\b", "_round_start_next", text)
    text = re.sub(r"\bsub_A289\b", "@ROUND_SCORE_COMMIT$QUI", text)

    start = text.index("sub_9AD6\tproc near")
    end = text.index("sub_9EBF\tendp", start) + len("sub_9EBF\tendp")
    if re.findall(r"^(\S+)\s+proc near", text[start:end], re.M) != [
        "sub_9AD6",
        "sub_9B0F",
        "sub_9B14",
        "sub_9EBF",
    ]:
        raise ValueError("complete stage/round procedure interval differs")
    text = (
        text[:start]
        + "extern _stage_demo_update_active:near\nextern _stage_demo_update_none:near\nextern _stage_setup:near\nextern _round_prepare_players:near\n"
        + text[end:]
    )
    text = re.sub(r"\bsub_9AD6\b", "_stage_demo_update_active", text)
    text = re.sub(r"\bsub_9B0F\b", "_stage_demo_update_none", text)
    text = re.sub(r"\bsub_9B14\b", "_stage_setup", text)
    text = re.sub(r"\bsub_9EBF\b", "_round_prepare_players", text)

    start = text.index("sub_9778\tproc near\n")
    end = text.index("sub_9778\tendp", start) + len("sub_9778\tendp")
    if re.findall(r"^(\S+)\s+proc\s+(?:near|far)", text[start:end], re.M) != ["sub_9778"]:
        raise ValueError("complete round-loop procedure interval differs")
    text = text[:start] + "extern _round_loop:near\n" + text[end:]
    text = re.sub(r"\bsub_9778\b", "_round_loop", text)

    for segment, imports in (
        (
            "main_010_TEXT\tsegment\tbyte public 'CODE' use16",
            [
                "@PLAYER_STATE_UPDATE$QUIP14PLAYER_STUFF_T",
                "@PLAYER_RENDER$QP14PLAYER_STUFF_T",
                "@PLAYER_OVERLAY_RENDER$QP14PLAYER_STUFF_T",
            ],
        ),
        (
            "P_SHOT_TEXT segment byte public 'CODE' use16",
            [
                "@stage_prepare_shot_sprites$qv",
                "@round_objects_and_counters_reset$qv",
                "@round_match_result_render$qv",
                "@player_shots_add$qv",
            ],
        ),
    ):
        text = once(
            text,
            segment + "\n",
            segment
            + "\n"
            + "".join("\textern " + name + ":near\n" for name in imports),
        )

    renamed = {
        "sub_DA43": "@PLAYER_STATE_UPDATE$QUIP14PLAYER_STUFF_T",
        "_player_render": "@PLAYER_RENDER$QP14PLAYER_STUFF_T",
        "sub_DF18": "@PLAYER_OVERLAY_RENDER$QP14PLAYER_STUFF_T",
        "sub_E266": "@stage_prepare_shot_sprites$qv",
        "sub_E313": "@round_objects_and_counters_reset$qv",
        "sub_E3F2": "@round_match_result_render$qv",
    }
    for old, new in renamed.items():
        text = re.sub(r"\b" + re.escape(old) + r"\b", lambda m: new, text)

    for old, alias, distance in (
        ("sub_B37C", "_round_playfield_clear", "near"),
        ("sub_B4A3", "_stage_background_update_none", "near"),
        ("sub_B4A8", "_stage_demo_finish", "near"),
        ("sub_A38E", "_stage_palette_show", "far"),
        ("sub_A38E", "_round_objects_for_next", "far"),
        ("@GameExecl$qnxc", "MAIN_EXEC", "far"),
        ("sub_C248", "@PLAYER_LOSE_ANIM_RENDER$QP14PLAYER_STUFF_T", "near"),
    ):
        marker = old + "\tproc " + distance
        text = once(
            text,
            marker,
            "public " + alias + "\n" + alias + " label " + distance + "\n" + marker,
        )

    for name in (
        "reimu",
        "mima",
        "marisa",
        "ellen",
        "kotohime",
        "kana",
        "rikako",
        "chiyuri",
        "yumemi",
    ):
        old = "set_callbacks_" + name
        marker = old + "\tproc near"
        text = once(
            text,
            marker,
            "public " + old.upper() + "\n" + old.upper() + " label near\n" + marker,
        )
    text = once(
        text,
        "PID_NONE = -1\n",
        "PID_NONE = -1\npublic _story_cpu_safety_frames\n_story_cpu_safety_frames label word\n",
    )

    for label, symbol in (
        ("sub_C0D8", "@PLAYER_LOSE_ANIM_UPDATE$QP14PLAYER_STUFF_T"),
        ("sub_C1E6", "@PLAYER_LOSE_PARTICLE_PUT$QUCUC"),
        ("sub_C2F9", "@round_defeat_banners_render$qv"),
    ):
        pattern = rf"(?m)^{label}\s+proc near\n.*?^{label}\s+endp\n"
        text, count = re.subn(pattern, "extern " + symbol + ":near\n", text, flags=re.S)
        if count != 1:
            raise ValueError("complete lose procedure missing: " + label)
        text = re.sub(r"\b" + re.escape(label) + r"\b", lambda m: symbol, text)

    aliases = [
        ("aCOul", "_main_archive_name", "byte"),
        ("aGameft_bft", "_main_gaiji_font", "byte"),
        ("aOp", "_main_op_name", "byte"),
        ("arg0", "_main_ending_name", "byte"),
        ("farfp_20F20", "_main_background_init", "dword"),
        ("farfp_20F28", "_round_background_reset", "dword"),
        ("farfp_20F24", "_round_render_hook", "dword"),
        ("exatt_update_p1", "_round_exatt_update_p1", "dword"),
        ("exatt_update_p2", "_round_exatt_update_p2", "dword"),
        ("exatt_render_p1", "_round_exatt_render_p1", "dword"),
        ("exatt_render_p2", "_round_exatt_render_p2", "dword"),
        ("p1_205CE", "_round_player_hook_p1", "dword"),
        ("p2_205D2", "_round_player_hook_p2", "dword"),
        ("bomb_p1", "_round_bomb_p1", "dword"),
        ("bomb_p2", "_round_bomb_p2", "dword"),
        ("byte_23AFA", "_stage_render_timing_flag", "byte"),
        ("word_1E6E8", "_stage_result_wait_frames", "word"),
        ("fp_1E6EA", "_stage_demo_update", "word"),
        ("fp_1FBC0", "_stage_background_update", "word"),
        ("aLose_bf2", "_stage_lose_bfnt", "byte"),
        ("aRound_bf2", "_stage_round_bfnt", "byte"),
        ("aZikicw_bf2", "_stage_zikicw_bfnt", "byte"),
        ("byte_1FBC2", "_playfield_transition_frame", "byte"),
        ("byte_1FBC3", "_playfield_transition_midpoint", "byte"),
        ("byte_20E3D", "_round_defeated_player", "byte"),
        ("word_20E3E", "_player_lose_left", "word"),
        ("word_20E40", "_player_lose_top", "word"),
        ("word_20E42", "_player_lose_radius", "word"),
        ("byte_23AF9", "_round_reset_flag", "byte"),
        ("byte_23B00", "_round_reset_clear_flag", "byte"),
        ("score_23DEA", "_result_bonus_step", "word"),
        ("word_23DEC", "_result_bonus_low", "word"),
        ("word_23DEE", "_result_bonus_high", "word"),
        ("score_23DF0", "_result_bonus_remaining", "dword"),
        ("byte_23DF9", "_result_lives_remaining", "byte"),
    ]
    for old, alias in zip(
        (
            "aMAX_COMBO",
            "aGAUGE_ATTACK_TIMES",
            "aBOSS_ATTACK_TIMES",
            "aBOSS_REVERSAL_TIMES",
            "aBOSS_PANIC_TIMES",
            "aTOTAL",
            "aWINNER_BONUS",
            "aALL_CLEAR",
            "aPLAYER_REM",
        ),
        (
            "combo",
            "gauge",
            "boss",
            "reversal",
            "panic",
            "total",
            "winner",
            "clear",
            "lives",
        ),
    ):
        aliases.append((old, "_result_label_" + alias, "byte"))
    for old, alias, kind in aliases:
        matches = list(
            re.finditer(r"(?m)^" + re.escape(old) + r"[\t ]+(?:db|dw|dd)\b", text)
        )
        if len(matches) != 1:
            raise ValueError("existing storage definition differs: " + old)
        at = matches[0].start()
        text = (
            text[:at]
            + "public "
            + alias
            + "\n"
            + alias
            + " label "
            + kind
            + "\n"
            + text[at:]
        )

    text = once(
        text,
        "\t\tdb 5 dup(?)\n_collmap\t",
        "\t\tdb ?\npublic _shot_release_frames\n_shot_release_frames db 2 dup(?)\n\t\tdb 2 dup(?)\n_collmap\t",
    )
    from lib.main_master_prefix import detach
    from lib.main_master_body import detach as detach_body

    text = detach_body(detach(text))
    return text.replace("\n", "\r\n").encode("latin1")


def stage_carriers(work):
    from replay_th03_main_exact_units import apply_carrier_edits
    from lib.main_master_prefix import source as master_prefix_source
    from lib.main_master_body import source as master_body_source
    from stage_th03_main_shotroot import transform_score
    from lib import th03_yumemi_bomb_candidate as bomb
    from lib import th03_player_tail_candidate as tail
    from lib import th03_cpu_model as cpu
    from lib import th03_yumemi_charge_candidate as charge

    config = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    reference = ROOT / "_reference/ReC98"
    original = (reference / "th03_main.asm").read_bytes()
    expected = {
        u["carrier_sha256"]
        for u in config["units"]
        if u.get("carrier_path") == "th03_main.asm"
    }
    if expected != {sha(original)}:
        raise ValueError("pinned reference MAIN source differs")
    work.mkdir(parents=True, exist_ok=True)
    path = work / "th03_main.asm"
    path.write_bytes(original)
    for unit in config["units"]:
        apply_carrier_edits(unit, work)
    raw = path.read_bytes()
    raw = bomb.edit_root(raw)
    raw = tail.edit_root(raw)[0]
    raw = cpu.edit_root(raw)
    raw = charge.edit_root(raw)
    prepared = {
        "th03_main.asm": native_carrier(raw),
        "th03/mst_pref.asm": master_prefix_source(raw),
        "th03/mst_body.asm": master_body_source(raw),
        "th03/th03.inc": (reference / "th03/th03.inc").read_bytes(),
        "src/main/hud/score.asm": transform_score(
            (ROOT / "src/main/hud/score.asm").read_bytes()
        ),
    }
    for unit in config["units"]:
        if unit.get("ownership") == "bounded-include":
            prepared[unit["overlay_path"]] = (ROOT / unit["source"]).read_bytes()
    response = (ROOT / "config/th03_main_link.rsp").read_text()
    prepared["obj/th03/main.@l"] = response.replace("\n", "\r\n").encode("ascii")
    for name, content in prepared.items():
        dest = work / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
    return prepared


def generate_sprites(work):
    """Run the pinned reference bitmap converter; its output owns data, not code."""
    reference = ROOT / "_reference/ReC98"
    tool = ROOT / ".tools/bmp2arr"
    tool.parent.mkdir(parents=True, exist_ok=True)
    sources = ["Pipeline/bmp2arr.c", "Pipeline/bmp2arrl.c", "Pipeline/bmp2arrl.h"]
    compile_argv = [
        "cc",
        "-O2",
        "-D__cdecl=",
        *(str(reference / n) for n in sources[:2]),
        "-o",
        str(tool),
    ]
    subprocess.run(
        compile_argv,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    generated = {}
    report = dict(
        compiler=compile_argv,
        tool_sha256=sha(tool.read_bytes()),
        source_sha256={name: sha((reference / name).read_bytes()) for name in sources},
        conversions=[],
    )
    for name, symbol, width, height, flags in (
        ("score", "_sSCORE_FONT", 8, 8, ["-u"]),
        ("pellet", "_sPELLET", 32, 4, []),
    ):
        source = "th03/sprites/" + name + ".bmp"
        output = "th03/sprites/" + name + ".asp"
        raw = (reference / source).read_bytes()
        dest = work / source
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        argv = [
            str(tool),
            "-q",
            "-i",
            source,
            "-o",
            output,
            "-sym",
            symbol,
            "-of",
            "asm",
            "-sw",
            str(width),
            "-sh",
            str(height),
            *flags,
        ]
        subprocess.run(
            argv,
            cwd=work,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        generated[source] = raw
        generated[output] = (work / output).read_bytes()
        report["conversions"].append(
            dict(argv=argv, input_sha256=sha(raw), output_sha256=sha(generated[output]))
        )
    return generated, report
