"""Read-only verification of the original OP DIET restoration chain.

No subprocess, extraction, native execution, output write, or acceptance.
The caller must validate this helper and its supplied describe_blob callback
before calling. Historical receipt inputs are checked, never regenerated.
"""
from pathlib import Path
import hashlib
import io
import json
import re
import tarfile
import tomllib

RECEIPT = '.analysis/th03-diet/sol-diet-restoration-20261006-b/receipt.json'
RECEIPT_SHA256 = 'ca533176a0ce89ccc7a782ff397965a781d4a60fdcf750e1b5fcbc3ead85d71d'
RECEIPT_BYTES = 192413
ARCHIVE = '.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar'
ARCHIVE_SHA256 = '9f7a4eb17f24ae2d99adaba4320f6c46f4fc8d659f9b784f6d8e5f3af99bf705'
SOURCE_INPUTS = {
    'config/th03_diet.toml', 'config/targets.toml',
    'config/toolchain.toml', 'scripts/review_th03_diet.py',
}
REVISION = 'b6ba5b0a529edbb31efdf8c0e939263804f8ee47'


def need(value, message):
    if not value:
        raise ValueError('OP DIET lineage: ' + message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_diet_lineage(root, describe_blob):
    """Return (recomputed identity witness, mandatory path/bytes/SHA pins)."""
    root = Path(root)
    pins = {}

    def read(name, expected=None, size=None):
        relative = Path(name)
        need(not relative.is_absolute() and '..' not in relative.parts and
             name not in ('', '.') and '\\' not in name, 'unsafe path ' + name)
        path = root / relative
        need(path.is_file() and not any(p.is_symlink() for p in (path, *path.parents)),
             'missing regular input ' + name)
        data = path.read_bytes()
        digest = sha(data)
        need(expected is None or digest == expected, 'historical input drift ' + name)
        need(size is None or len(data) == size, 'historical input size ' + name)
        pins[name] = dict(path=name, bytes=len(data), sha256=digest)
        return data

    receipt = json.loads(read(RECEIPT, RECEIPT_SHA256, RECEIPT_BYTES))
    need(receipt['kind'] == 'th03-private-diet-restoration-diagnostic' and
         receipt['run_id'] == 'sol-diet-restoration-20261006-b', 'wrong receipt')
    need(receipt['source_acceptance'] is False and receipt['exact_acceptance'] is False,
         'historical acceptance inflation')
    need(receipt['canonical_targets_unchanged'] is True and
         receipt['restoration_checks_pass'] is True, 'historical restoration failed')
    need(set(receipt['source_inputs']) == SOURCE_INPUTS, 'historical source-input set')
    source = {name: read(name, digest) for name, digest in receipt['source_inputs'].items()}
    diet = tomllib.loads(source['config/th03_diet.toml'].decode())
    targets = tomllib.loads(source['config/targets.toml'].decode())
    toolchain = tomllib.loads(source['config/toolchain.toml'].decode())
    need(receipt['config_sha256'] == sha(source['config/th03_diet.toml']), 'config digest')
    need(receipt['reference_revision'] == diet['reference_revision'] == REVISION,
         'reference revision')

    def unique(rows, key, value):
        selected = [row for row in rows if row[key] == value]
        need(len(selected) == 1, 'ambiguous ' + key + '=' + value)
        return selected[0]

    observed = unique(receipt['observations'], 'artifact', 'th03-op')
    declared = unique(diet['artifacts'], 'id', 'th03-op')
    target = unique(targets['artifacts'], 'id', 'th03-op')
    expected_decoded = str(Path(RECEIPT).parent / 'op.exe')
    need(observed['decoded_path'] == expected_decoded, 'decoded path')
    stored = read(target['private_path'], target['sha256'], target['size'])
    decoded = read(expected_decoded, declared['decoded_sha256'], declared['decoded_size'])
    stored_description = describe_blob(stored)
    decoded_description = describe_blob(decoded)
    need(stored_description == observed['stored'], 'recomputed stored description')
    need(decoded_description == observed['decoded'], 'recomputed decoded description')
    need(stored_description['format'] == target['format'] == 'mz' and
         stored_description['md5'] == target['md5'] and
         stored_description['format_integrity']['valid'] is True, 'stored format identity')
    header = stored_description['mz']['header']
    need(stored[28:32] == b'diet' and header['header_size'] == 32 and
         header['number_of_relocations'] == 0, 'stored DIET envelope')
    need(decoded_description['format'] == declared['decoded_format'] == 'mz' and
         decoded_description['format_integrity']['valid'] is True, 'decoded format identity')
    need(decoded_description['md5'] == declared['reference_input_md5'] ==
         observed['reference_input_md5'], 'reference decoded MD5')

    tool = diet['tool']
    read(tool['path'], tool['sha256'], tool['size'])
    need(receipt['tool_sha256'] == tool['sha256'] and tool['version'] == '1.45f',
         'DIET tool identity')
    runner_name = toolchain['paths']['msdos_player']
    runner = unique(toolchain['surfaces'], 'path', runner_name)
    need(runner['kind'] == 'file' and runner['required'] is True, 'runner manifest')
    read(runner_name, runner['sha256'])

    commands = receipt['commands']
    for suffix, filename, code, marker in [
        (['-!'], 'diet-selfcheck.log', 0, b'DIET.EXE is original file!'),
        (['-ra', 'OP.EXE'], 'th03-op.log', 1, b'Success! (36041 to 63866 bytes)'),
    ]:
        matches = [c for c in commands if c['argv'][-len(suffix):] == suffix]
        need(len(matches) == 1, 'ambiguous restoration command')
        command = matches[0]
        argv = command['argv']
        need(len(argv) == 5 + len(suffix) and argv[0] == 'wine' and
             Path(argv[1]).parts[-len(Path(runner_name).parts):] == Path(runner_name).parts and
             argv[2:5] == ['-e', '-x', 'DIET.EXE'] and
             type(command['returncode']) is int and command['returncode'] == code,
             'historical restoration command')
        log = read(str(Path(RECEIPT).parent / filename), command['output_sha256'])
        need(marker in log and b'version 1.45f' in log, 'historical command log')

    archive = read(ARCHIVE, ARCHIVE_SHA256)
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as stream:
        members = [m for m in stream.getmembers() if m.name == 'th03_op.asm']
        need(len(members) == 1 and members[0].isfile(), 'reference archive member')
        reference = stream.extractfile(members[0]).read()
    need(observed['reference_root'] == declared['reference_root'] == 'th03_op.asm',
         'reference root name')
    # Archive is the pinned DOS source representation; receipt hashed git-show LF.
    # This explicit source-text transform never touches any target/candidate bytes.
    git_representation = reference.replace(b'\r\n', b'\n')
    need(sha(git_representation) == observed['reference_root_sha256'], 'historical root blob')
    md5 = re.findall(rb'Input\s+MD5\s*:\s*([0-9a-fA-F]{32})', git_representation)
    need(len(md5) == 1 and md5[0].decode().lower() == observed['reference_input_md5'],
         'root input MD5 declaration')
    result = dict(
        stored_sha256=sha(stored), decoded_sha256=sha(decoded),
        candidate_local_attested=True, independent_pristine_attestation=False,
        stored_to_decoded_lineage_verified=True, historical_receipt=RECEIPT,
        historical_receipt_sha256=RECEIPT_SHA256,
        historical_observed_utc=receipt['observed_utc'],
        restoration_native_invocations_now=0, current_format_recomputed=True,
        tool_sha256=tool['sha256'], runner_sha256=runner['sha256'],
        source_inputs_verified=sorted(SOURCE_INPUTS),
        source_reference=dict(archive=ARCHIVE, archive_sha256=ARCHIVE_SHA256,
                              member='th03_op.asm', archive_member_sha256=sha(reference),
                              historical_git_blob_sha256=sha(git_representation),
                              source_representation_transform='CRLF-to-LF'),
    )
    return result, [pins[name] for name in sorted(pins)]
