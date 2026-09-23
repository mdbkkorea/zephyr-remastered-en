"""Hash-locked reveal speed and reviewed Auto-Advance layout adjustments."""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVEAL_INPUTS = {
    'ccdcca011a443114da40968ae486b3530efd9657cd41989667af052fb4a024a9': 0x81bd73,
    '5906c49ef11c51ae9985a088012771da811926d595eb667866426b82db299970': 0x8048a3,
}


def patch_reveal(original):
    digest = hashlib.sha256(original).hexdigest()
    if digest not in REVEAL_INPUTS:
        raise ValueError('Unsupported dialogue renderer binary')
    at = REVEAL_INPUTS[digest]
    if original[at:at+7] != bytes.fromhex('c74118295c8f3d'):
        raise ValueError('Unexpected TextSpeed initializer')
    result = bytearray(original)
    result[at+3:at+7] = struct.pack('<f', 0.028)
    return bytes(result)


def apply_layout(tree, relative, key):
    profile = json.loads((ROOT/'localization/auto-advance-layout.json').read_text())
    count = 0
    for change in profile['changes']:
        ref = change['reference']
        if (ref['file'], ref['serialized_file'], ref['object_id']) != (relative, *key):
            continue
        field, = ref['path']
        if tree[field] != change['expected'] or tree.get('m_text') != '<sprite=20> Auto-Advance':
            raise ValueError('Unexpected Auto-Advance label/font')
        tree[field] = change['value']
        count += 1
    return count
