"""Validate fixed-byte English edits inside IL2CPP v39 literal data."""
import hashlib
import re
import struct
from scripts.check_korean_batch import tokens


def literal_spans(data):
    if len(data) < 32:
        raise ValueError('Truncated metadata header')
    magic, version, table, size, count, start, length, strings = struct.unpack_from('<8I', data)
    if magic != 0xFAB11BAF or version != 39:
        raise ValueError('Unsupported metadata format')
    if size != count * 4 or count != strings + 1 or table + size > len(data) or start + length > len(data):
        raise ValueError('Invalid literal table bounds')
    offsets = struct.unpack_from('<%dI' % count, data, table)
    if offsets[0] != 0 or offsets[-1] != length or any(a > b for a, b in zip(offsets, offsets[1:])):
        raise ValueError('Invalid literal offsets')
    return [(start + a, start + b) for a, b in zip(offsets, offsets[1:])]


def translate_metadata(data, drafts):
    spans = literal_spans(data)
    output = bytearray(data)
    ranges = []
    for row in drafts:
        ref = row['reference']
        start, length = ref['offset'], ref['byte_length']
        end = start + length
        if not any(a <= start < end <= b for a, b in spans):
            raise ValueError('Edit is outside a single literal')
        if any(start < b and a < end for a, b in ranges):
            raise ValueError('Overlapping metadata edits')
        original = data[start:end]
        if original != row['original'].encode('utf-8') or hashlib.sha256(original).hexdigest() != ref['original_sha256']:
            raise ValueError('Metadata source mismatch')
        target = row['target']
        if re.search('[\u3400-\u9fff\uac00-\ud7a3]', target) or tokens(target) != tokens(row['original']):
            raise ValueError('Invalid metadata translation or controls')
        for pattern in (r'/\d+[a-zA-Z]|/n', r'\r?\n'):
            if re.findall(pattern, target) != re.findall(pattern, row['original']):
                raise ValueError('Metadata controls reordered')
        replacement = target.encode('utf-8')
        if len(replacement) > length:
            raise ValueError('Metadata replacement exceeds fixed byte slot')
        output[start:end] = replacement.ljust(length, b' ')
        ranges.append((start, end))
    if len(output) != len(data) or literal_spans(output) != spans:
        raise ValueError('Metadata layout changed')
    cursor = 0
    for start, end in sorted(ranges):
        if output[cursor:start] != data[cursor:start]:
            raise ValueError('Unedited metadata bytes changed')
        cursor = end
    if output[cursor:] != data[cursor:]:
        raise ValueError('Unedited metadata suffix changed')
    return bytes(output)
