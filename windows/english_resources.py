"""Reconstruct hash-locked English resources from compressed XOR deltas."""
import os
import hashlib
import sys
import zlib
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def windows_long_path(path):
    path = Path(path)
    text = str(path)
    if os.name == 'nt' and not text.startswith('\\\\?\\'):
        if text.startswith('\\\\'):
            return Path('\\\\?\\UNC\\' + text[2:])
        return Path('\\\\?\\' + text)
    return path


def safe(root, relative):
    root = windows_long_path(Path(root).resolve())
    relative = str(relative)
    if '\\' in relative or ':' in relative or relative.startswith('/') or '..' in Path(relative).parts:
        raise ValueError('Unsafe patch path.')
    path = windows_long_path((root / relative).resolve())
    if not path.is_relative_to(root) or path == root:
        raise ValueError('Path escapes the selected folder.')
    return windows_long_path(path)


def rebuild(original, out, patch, payload, verify_output=True):
    for index, item in enumerate(patch['files'], 1):
        src, dst = safe(original, item['path']), safe(out, item['path'])
        if sha(src) != item['before_sha256']:
            raise ValueError('Original file checksum failed: ' + item['path'])
        blob = safe(payload, item['delta']).read_bytes()
        if hashlib.sha256(blob).hexdigest() != item['delta_sha256']:
            raise ValueError('Patch delta checksum failed.')
        delta = zlib.decompress(blob)
        if len(delta) != item['after_size']:
            raise ValueError('Patch delta size mismatch.')
        before = src.read_bytes()
        result = bytes(a ^ b for a, b in zip(before[:len(delta)].ljust(len(delta), b'\0'), delta))
        if hashlib.sha256(result).hexdigest() != item['after_sha256']:
            raise ValueError('Reconstructed file checksum failed: ' + item['path'])
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(result)
        if sha(dst) != item['after_sha256']:
            raise ValueError('Staged file checksum failed.')
        if sys.stderr:
            print(f'Prepared resource {index}/{len(patch["files"])}', file=sys.stderr, flush=True)
