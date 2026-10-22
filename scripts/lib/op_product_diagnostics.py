"""Bounded retained OP equality annotation, never acceptance or full replay."""
import hashlib
import json
from pathlib import Path

# Reviewed retained inputs, not a newly generated acceptance registry.
PINS = {'.analysis/gpt-dots-player-cpu-acceptance-install-v01/support.py': {'bytes': 5324,
                                                                     'sha256': 'fd19475aea02ec5aa6ae8e4c48f6ab88170f1d73e0f6ee7dbfa7231d50dc8c68'},
 '.analysis/op-alignment-checkpoint-proposal-v01/install-manifest.json': {'bytes': 2716,
                                                                          'sha256': 'b5cd95d41947d2021f822f142a4e2ad1d7742760af4803659422b0694251d834'},
 '.analysis/op-diet-exact-source-output-v01/calibration-verification.json': {'bytes': 2281,
                                                                             'sha256': '2dea9b389334a8f8cd9f9990966f848faec83b655b156dcdd619f574cb1249d9'},
 '.analysis/op-diet-exact-source-output-v01/completion.json': {'bytes': 428,
                                                               'sha256': '6c8496395a4f4a45e0346fcc43701a212ad66bd7f0043af52fed814c11a54303'},
 '.analysis/op-diet-exact-source-output-v01/manifest.json': {'bytes': 883232,
                                                             'sha256': '33e02ce2fde45abd2873feb56b8a7e0150bb95c5c7c81ebf2fa17d2d9de2fed6'},
 '.analysis/op-diet-negative-checkpoint-v01/replay.py': {'bytes': 3661,
                                                         'sha256': '6f8eb41eb507d2405cbb5eb122242126ae531bfe66e76c1cc81d96072ff862d1'},
 '.analysis/op-fullcold-exact-terminal-20261022-v01.json': {'bytes': 155032,
                                                            'sha256': '6e17905d2afd2a449f16f9d26ac3044311f0d2fcfe07a3cd71723772fb4c7dab'},
 '.analysis/op-fullcold-ordered-deferred-v03/r1g7-manifest.json': {'bytes': 657180,
                                                                   'sha256': '3f1b58456f943f0e7ccc77e3925b193647dc8e107e513566e39a1a46cef6d677'},
 '.analysis/op-fullcold-ordered-deferred-v03/r2g7-manifest.json': {'bytes': 661563,
                                                                   'sha256': 'ea475823da8755f8a9dc5b85cfd512cb7f633d43b8e1d13ecd199c5f348c3d32'},
 '.analysis/op-global-order-checkpoint-proposal-v01/install-manifest.json': {'bytes': 2739,
                                                                             'sha256': 'c020c4cf23b1b1170727f1143528b9d42d741a982b0d7a999a273afde7bfe589'},
 '.analysis/op-nopcall-checkpoint-proposal-v01/install-manifest.json': {'bytes': 2121,
                                                                        'sha256': 'ae2a25f09841a14395b90ee5ab638799891e8bffa4a17a598dd4ba9187771d3d'},
 '.analysis/op-nopcall-offline-correction-v01/audit.py': {'bytes': 6346,
                                                          'sha256': '2be7f0f9f0c42afd487649772a26643343dd5bb7ede9441851d6ea69bc3a61a6'},
 '.analysis/op-nopcall-offline-correction-v01/linked-verification.json': {'bytes': 92303,
                                                                          'sha256': '163247a0d93743d3f99a8059c0c334344486e7b33c15aedc01de9187b0232827'},
 '.analysis/op-pfopen-checkpoint-proposal-v01/install-manifest.json': {'bytes': 6939,
                                                                       'sha256': '35e125b3f95e3e81a85472d271b798e2036a4237188fb42a3ac4ad91d38264e2'},
 '.analysis/targets/th03/op.exe': {'bytes': 36041,
                                   'sha256': 'd7bfa7f1f8afe0943763ce76437d12ed412b8452716dd64f937c94796eba57ab'},
 '.analysis/th03-diet/sol-diet-restoration-20261006-b/op.exe': {'bytes': 63866,
                                                                'sha256': 'efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/bin/th03/op.exe': {'bytes': 63866,
                                                                    'sha256': 'efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th01/vplanset.obj': {'bytes': 647,
                                                                          'sha256': '4d358dd30d9c0e8d971e9a2088e55803cb8bf2779b130f323bb58dd5694340b6'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th02/exit_dos.obj': {'bytes': 839,
                                                                          'sha256': '2c032c4fee6d36e1d7bc3bdbc59e501f735d5f68438c27507c26e46382de1eb2'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th02/frmdely1.obj': {'bytes': 585,
                                                                          'sha256': '075104de34aeb0bc6d62c110ffc760b4e9c3c3f276ffe805a362d0acf70b7547'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th02/frmdely2.obj': {'bytes': 585,
                                                                          'sha256': 'f09853b5c6a770eb2ece84381190f23be87ea4c2f6a13e325c9007e41b445e4e'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th02/snd_load.obj': {'bytes': 742,
                                                                          'sha256': 'a637d985dcc5fd59d9ae6eb4bfbbf1ec446d9906b0bcb033dbaa1e49090b068f'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th02/snd_mode.obj': {'bytes': 651,
                                                                          'sha256': '13bed843b4c8416a4ce9b6fbf6586046ccf102b1784436a1f9359023fbf7e437'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th02/snd_pmdr.obj': {'bytes': 711,
                                                                          'sha256': '35fec9cc717a7cdf87bee36da853da229728c9a4ad58ff40bb34f846a29198fc'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/cdg_load.obj': {'bytes': 1522,
                                                                          'sha256': '0d17ed5480d820c52fc3e850d089c5e77997e255d899da815eb89223588232f6'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/cdg_p_na.obj': {'bytes': 487,
                                                                          'sha256': 'c23e4727258d020039d80560b0b9f407a74b2026c3f3070a641bb5441e520102'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/cdg_put.obj': {'bytes': 1076,
                                                                         'sha256': '8468bd0af9159d0ab7556b185dc37867038d54cd7a28a8682d4cd2ed75fdf3a1'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/exit.obj': {'bytes': 911,
                                                                      'sha256': '1559001e1b707cc318f84188341efe50da37fef4fe4a967889eda4a7b8d800d6'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/grppsafx.obj': {'bytes': 1687,
                                                                          'sha256': 'a0c5a878865d9164aeda7dbdbba66c9711b9c5759a6982b2b2a7651ca942be1b'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/hfliplut.obj': {'bytes': 272,
                                                                          'sha256': 'a6e70f6b525cfa8ce234c09907c4a8657b35ac8397a2d35cb104503e2880b877'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/initop.obj': {'bytes': 1279,
                                                                        'sha256': '52fb2c949c88c728e27074895c837474a21abacc36ef970b39f8e9ae79d4bd6c'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/inp_m_w.obj': {'bytes': 1679,
                                                                         'sha256': '8f8132e247e5594d9c0a702eeaadde40c9322d7949f714789653a129cc6f152b'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/input_s.obj': {'bytes': 1506,
                                                                         'sha256': 'abbf7ae32e781029167899e2cab3c8e009edee571c0f5d4264be810e1e681c7f'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/op.map': {'bytes': 68078,
                                                                    'sha256': '2666a302659c05b2c7d949db089cf01383f2abc19ca3cc996be052138bcbb00a'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/op.obj': {'bytes': 24740,
                                                                    'sha256': '8854f90597064c7cec66924d9ca09516c65f1c0b0fe1a0c8afb6c6dc44782ba5'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/op_01.obj': {'bytes': 9721,
                                                                       'sha256': 'd3b7e578a6be4ff3f157352dea83c0130400d5817018c6a13e4a465b674b9c6b'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/op_02.obj': {'bytes': 1273,
                                                                       'sha256': '61c23caa1603c1871d67669061b567e9677ee299ce82e425e53c55db1caf2860'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/op_main.obj': {'bytes': 3462,
                                                                         'sha256': '99d08e50979d1c76a2aefe8a558a9f21b40873a9ed079f22360be6119570369e'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/op_music.obj': {'bytes': 7698,
                                                                          'sha256': '451104da871d29e66f0f44dbf004c7d0f346693439b3cd43f06e07927b748cae'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/oplayout.obj': {'bytes': 323,
                                                                          'sha256': '77cca784bf9c1bd2a8811ad4d80597e4843801875c24c80d0a3e060509bb3dda'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/optail.obj': {'bytes': 3112,
                                                                        'sha256': '82f2c12bc8e23e009cf3f77dd0ed07502807cf086763766724b53bff4c0afc8e'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/pi_load.obj': {'bytes': 705,
                                                                         'sha256': '492b9a27743d17b3803cd83cf383e9b73a1e5c58e7b8dbb2ee3c32a64dd4bb86'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/pi_put.obj': {'bytes': 967,
                                                                        'sha256': '450f63e87759249ed9878a8cca108900e2680a3134589dfd03d01808f49b00b2'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/polar.obj': {'bytes': 407,
                                                                       'sha256': '022f968a35aba447fb0a8cd80fc06b720c0d2a5f1bf16b56e54a9902003f548a'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/scoredat.obj': {'bytes': 1266,
                                                                          'sha256': 'df7fd27e594e79565d4fc5d761cc501c57b6766670e859a72df6bd9f1d1a7819'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/selhelp.obj': {'bytes': 3062,
                                                                         'sha256': '16af70f2d3c052d6210b5ef4d077378d90ed9ac9100e9bf41f7f8f633a13b659'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/seltail.obj': {'bytes': 8251,
                                                                         'sha256': '0e49612d8903129f3f418a6e0682815b8284561ff6adbcdfbede6d8b59819ad9'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO211/obj/th03/snd_kaja.obj': {'bytes': 673,
                                                                          'sha256': '6fd5b2cb138ea88990c7e0b97603517ea45cecca5aa7450aade3d532eb65da3d'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/bin/th03/op.exe': {'bytes': 63866,
                                                                    'sha256': 'efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th01/vplanset.obj': {'bytes': 647,
                                                                          'sha256': '4d358dd30d9c0e8d971e9a2088e55803cb8bf2779b130f323bb58dd5694340b6'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th02/exit_dos.obj': {'bytes': 839,
                                                                          'sha256': '2c032c4fee6d36e1d7bc3bdbc59e501f735d5f68438c27507c26e46382de1eb2'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th02/frmdely1.obj': {'bytes': 585,
                                                                          'sha256': '075104de34aeb0bc6d62c110ffc760b4e9c3c3f276ffe805a362d0acf70b7547'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th02/frmdely2.obj': {'bytes': 585,
                                                                          'sha256': 'f09853b5c6a770eb2ece84381190f23be87ea4c2f6a13e325c9007e41b445e4e'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th02/snd_load.obj': {'bytes': 742,
                                                                          'sha256': 'a637d985dcc5fd59d9ae6eb4bfbbf1ec446d9906b0bcb033dbaa1e49090b068f'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th02/snd_mode.obj': {'bytes': 651,
                                                                          'sha256': '13bed843b4c8416a4ce9b6fbf6586046ccf102b1784436a1f9359023fbf7e437'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th02/snd_pmdr.obj': {'bytes': 711,
                                                                          'sha256': '35fec9cc717a7cdf87bee36da853da229728c9a4ad58ff40bb34f846a29198fc'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/cdg_load.obj': {'bytes': 1522,
                                                                          'sha256': '0d17ed5480d820c52fc3e850d089c5e77997e255d899da815eb89223588232f6'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/cdg_p_na.obj': {'bytes': 487,
                                                                          'sha256': 'c23e4727258d020039d80560b0b9f407a74b2026c3f3070a641bb5441e520102'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/cdg_put.obj': {'bytes': 1076,
                                                                         'sha256': '8468bd0af9159d0ab7556b185dc37867038d54cd7a28a8682d4cd2ed75fdf3a1'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/exit.obj': {'bytes': 911,
                                                                      'sha256': '1559001e1b707cc318f84188341efe50da37fef4fe4a967889eda4a7b8d800d6'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/grppsafx.obj': {'bytes': 1687,
                                                                          'sha256': 'a0c5a878865d9164aeda7dbdbba66c9711b9c5759a6982b2b2a7651ca942be1b'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/hfliplut.obj': {'bytes': 272,
                                                                          'sha256': 'a6e70f6b525cfa8ce234c09907c4a8657b35ac8397a2d35cb104503e2880b877'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/initop.obj': {'bytes': 1279,
                                                                        'sha256': '52fb2c949c88c728e27074895c837474a21abacc36ef970b39f8e9ae79d4bd6c'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/inp_m_w.obj': {'bytes': 1679,
                                                                         'sha256': '8f8132e247e5594d9c0a702eeaadde40c9322d7949f714789653a129cc6f152b'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/input_s.obj': {'bytes': 1506,
                                                                         'sha256': 'abbf7ae32e781029167899e2cab3c8e009edee571c0f5d4264be810e1e681c7f'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/op.map': {'bytes': 68078,
                                                                    'sha256': '2666a302659c05b2c7d949db089cf01383f2abc19ca3cc996be052138bcbb00a'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/op.obj': {'bytes': 24740,
                                                                    'sha256': '8854f90597064c7cec66924d9ca09516c65f1c0b0fe1a0c8afb6c6dc44782ba5'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/op_01.obj': {'bytes': 9721,
                                                                       'sha256': 'd3b7e578a6be4ff3f157352dea83c0130400d5817018c6a13e4a465b674b9c6b'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/op_02.obj': {'bytes': 1273,
                                                                       'sha256': '61c23caa1603c1871d67669061b567e9677ee299ce82e425e53c55db1caf2860'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/op_main.obj': {'bytes': 3462,
                                                                         'sha256': '99d08e50979d1c76a2aefe8a558a9f21b40873a9ed079f22360be6119570369e'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/op_music.obj': {'bytes': 7698,
                                                                          'sha256': '451104da871d29e66f0f44dbf004c7d0f346693439b3cd43f06e07927b748cae'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/oplayout.obj': {'bytes': 323,
                                                                          'sha256': '77cca784bf9c1bd2a8811ad4d80597e4843801875c24c80d0a3e060509bb3dda'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/optail.obj': {'bytes': 3112,
                                                                        'sha256': '82f2c12bc8e23e009cf3f77dd0ed07502807cf086763766724b53bff4c0afc8e'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/pi_load.obj': {'bytes': 705,
                                                                         'sha256': '492b9a27743d17b3803cd83cf383e9b73a1e5c58e7b8dbb2ee3c32a64dd4bb86'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/pi_put.obj': {'bytes': 967,
                                                                        'sha256': '450f63e87759249ed9878a8cca108900e2680a3134589dfd03d01808f49b00b2'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/polar.obj': {'bytes': 407,
                                                                       'sha256': '022f968a35aba447fb0a8cd80fc06b720c0d2a5f1bf16b56e54a9902003f548a'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/scoredat.obj': {'bytes': 1266,
                                                                          'sha256': 'df7fd27e594e79565d4fc5d761cc501c57b6766670e859a72df6bd9f1d1a7819'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/selhelp.obj': {'bytes': 3062,
                                                                         'sha256': '16af70f2d3c052d6210b5ef4d077378d90ed9ac9100e9bf41f7f8f633a13b659'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/seltail.obj': {'bytes': 8251,
                                                                         'sha256': '0e49612d8903129f3f418a6e0682815b8284561ff6adbcdfbede6d8b59819ad9'},
 '.analysis/toolchain/wineprefix/drive_c/OPCO212/obj/th03/snd_kaja.obj': {'bytes': 673,
                                                                          'sha256': '6fd5b2cb138ea88990c7e0b97603517ea45cecca5aa7450aade3d532eb65da3d'},
 '.analysis/toolchain/wineprefix/drive_c/OPDP211/DECODED.EXE': {'bytes': 63866,
                                                                'sha256': 'efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'},
 '.analysis/toolchain/wineprefix/drive_c/OPDP211/P1/OP.EXE': {'bytes': 36041,
                                                              'sha256': 'd7bfa7f1f8afe0943763ce76437d12ed412b8452716dd64f937c94796eba57ab'},
 '.analysis/toolchain/wineprefix/drive_c/OPDP211/P2/OP.EXE': {'bytes': 36041,
                                                              'sha256': 'd7bfa7f1f8afe0943763ce76437d12ed412b8452716dd64f937c94796eba57ab'},
 '.analysis/toolchain/wineprefix/drive_c/OPDP211/R1/OP.EXE': {'bytes': 63866,
                                                              'sha256': 'efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'},
 '.analysis/toolchain/wineprefix/drive_c/OPDP211/R2/OP.EXE': {'bytes': 63866,
                                                              'sha256': 'efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'},
 '.analysis/toolchain/wineprefix/drive_c/OPNF201/bin/th03/op.exe': {'bytes': 63866,
                                                                    'sha256': 'efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'},
 'config/op_fullcold_exact/proof.json': {'bytes': 559003,
                                         'sha256': '4f50ea52204458a1ede50a26fd98f0ffbc32c214ea9d3fa9731503e643c86cfd'},
 'config/op_source_packing/proof.json': {'bytes': 631184,
                                         'sha256': '0d937b68ad739e8bd2a0bb4de4c054b016d3dc5a93635edfe6a17d2c1694a25b'}}


def checked(root, name):
    pin = PINS[name]
    path = Path(root) / name
    if not path.is_file() or any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError('missing regular diagnostic input: ' + name)
    raw = path.read_bytes()
    if len(raw) != pin['bytes'] or hashlib.sha256(raw).hexdigest() != pin['sha256']:
        raise ValueError('retained diagnostic drift: ' + name)
    return raw


def retained_op_products(root):
    """Recheck pinned reports and literal products, not full provenance/runtime."""
    empty = dict(retained_equality=False, product_acceptance=False,
                 canonical_credit_changed=False, whole_game_percentage=None,
                 full_replay_now=False, current_source_compatibility_checked=False,
                 cold_outputs_packed=False)
    try:
        # Bounded allowlist: no directory scan, import of replay code, or subprocess.
        raw = {name: checked(root, name) for name in PINS}
        def obj(name):
            return json.loads(raw[name])
        cold = obj('config/op_fullcold_exact/proof.json')
        pack = obj('config/op_source_packing/proof.json')
        terminal = obj(cold['terminal_attestation']['path'])
        manifests = [obj(q['path']) for q in cold['final_manifests']]
        pm = obj(pack['output'] + '/manifest.json')
        pr = obj(pack['output'] + '/calibration-verification.json')
        completion = obj(pack['output'] + '/completion.json')
        def need(value):
            if not value:
                raise ValueError('retained diagnostic scope mismatch')
        need(terminal['comparison_pass'] is True and terminal['rounds'] == 2
             and terminal['fresh_project_objects'] == 60 and terminal['actual_native_phases'] == 62)
        need(all(r['diagnostic_checks_pass'] and r['whole_file_equal_target']
                 for r in terminal['per_round']) and len(terminal['per_round']) == 2)
        need(terminal['packed_equality'] is False and cold['packed_equality'] is False
             and not any(terminal[k] for k in ('source_acceptance','exact_acceptance',
                                               'whole_product_ownership','runtime','new_authored_code_credit')))
        need(completion['complete'] is True and completion['owned_lock_released'] is True
             and completion['native_invocations'] == 5 and not completion['errors']
             and completion['exact_acceptance'] is False)
        need(pr['diagnostic_checks_pass'] is True and pr['source_fed'] is True
             and pr['target_fed'] is False and pr['canonical_packed_equal'] is True
             and pr['packed_difference_count'] == 0 and pr['full_cold_build'] is False
             and not any(pr[k] for k in ('source_acceptance','exact_acceptance',
                                        'whole_product_ownership','new_authored_code_credit',
                                        'output_bytes_patched','canonical_inputs_modified')))
        target = raw[pm['decoded_reference']['path']]
        canonical = raw[pm['canonical']['path']]
        need(len(target) == 63866 and len(canonical) == 36041)
        need(manifests[0]['work'] != manifests[1]['work'])
        for m in manifests:
            need(raw[m['work'] + '/bin/th03/op.exe'] == target)
        need(raw[manifests[0]['work'] + '/obj/th03/op.map'] ==
             raw[manifests[1]['work'] + '/obj/th03/op.map'])
        need(len(cold['raw_object_pairs']) == 30)
        for pair in cold['raw_object_pairs']:
            need(raw[pair['round1']['path']] == raw[pair['round2']['path']])
        # Source-fed packing is a separate retained run, not either cold output.
        need(pm['decoded']['path'] not in [m['work'] + '/bin/th03/op.exe' for m in manifests])
        need(raw[pm['decoded']['path']] == raw[pack['work'] + '/DECODED.EXE'] == target)
        for n in ['P1/OP.EXE', 'P2/OP.EXE']:
            need(raw[pack['work'] + '/' + n] == canonical)
        for n in ['R1/OP.EXE', 'R2/OP.EXE']:
            need(raw[pack['work'] + '/' + n] == target)
        return dict(empty, retained_equality=True, decoded_bytes=63866, packed_bytes=36041,
                    cold_rounds=2, historical_cold_phases=62, historical_packing_phases=5)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        return dict(empty, reason=str(exc))


def product_diagnostic_summary(result):
    if not result['retained_equality']:
        return ('OP retained whole-product diagnostic unavailable: ' + result['reason'] +
                '. This does not change the separate scoped acceptance axis.')
    return ('OP retained whole-file equality diagnostics: two source-cold builds each produced '
            'the exact 63,866-byte decoded target, including its header and literal relocation order. '
            'A separate source-fed packing run produced the exact 36,041-byte canonical packed image '
            'twice and restored both copies to its exact decoded source. The cold outputs themselves '
            'were not packed by these proofs. This bounded display rechecks pinned retained reports, '
            '30 raw object pairs and literal products; it does not rerun the full historical provenance '
            'replay or check current source compatibility. Product acceptance, runtime and whole-product '
            'authorship remain open. The fixed 33-owner scoped acceptance and current source counts are '
            'separate and unchanged; no canonical credit or whole-game percentage is added.')
