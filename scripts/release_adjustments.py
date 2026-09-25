"""Hash-locked reveal speed and verified UI layout adjustments."""
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


def layout_changes():
    for filename, default_text in (
        ('auto-advance-layout.json', '<sprite=20> Auto-Advance'),
        ('quest-layout.json', None),
    ):
        profile = json.loads((ROOT/'localization'/filename).read_text())
        for change in profile['changes']:
            yield change, change.get('expected_text', default_text)


def expected_layout_count(files):
    return sum(1 for change, _ in layout_changes() if change["reference"]["file"] in files)


def apply_layout(tree, relative, key):
    matched = []
    for change, expected_text in layout_changes():
        ref = change['reference']
        if (ref['file'], ref['serialized_file'], ref['object_id']) != (relative, *key):
            continue
        field, = ref['path']
        if tree.get(field) != change['expected'] or expected_text is None or tree.get('m_text') != expected_text:
            raise ValueError('Unexpected UI layout field or label: ' + str(key) + ' / ' + field)
        matched.append((field, change))
    # Validate all fields before changing the object.
    for field, change in matched:
        tree[field] = change['value']
    return len(matched)
