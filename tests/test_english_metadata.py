import hashlib
import struct
import unittest
from scripts.english_metadata import translate_metadata


def fixture(text='확인'):
    raw = text.encode()
    data = bytearray(40 + len(raw) + 8)
    struct.pack_into('<8I', data, 0, 0xFAB11BAF, 39, 32, 8, 2, 40, len(raw), 1)
    struct.pack_into('<2I', data, 32, 0, len(raw))
    data[40:40 + len(raw)] = raw
    data[-8:] = b'UNEDITED'
    row = dict(original=text, target='OK', reference=dict(offset=40, byte_length=len(raw),
               original_sha256=hashlib.sha256(raw).hexdigest()))
    return bytes(data), row


class MetadataTests(unittest.TestCase):
    def test_fixed_slot_preserves_header_offsets_and_suffix(self):
        data, row = fixture()
        result = translate_metadata(data, [row])
        self.assertEqual(result, data[:40] + b'OK    ' + b'UNEDITED')

    def test_bad_source_and_overflow_rejected(self):
        data, row = fixture()
        row['target'] = 'Too long for this slot'
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            translate_metadata(data, [row])
        row['target'] = 'OK'
        row['original'] = '취소'
        with self.assertRaisesRegex(ValueError, 'source mismatch'):
            translate_metadata(data, [row])

    def test_overlap_and_nonliteral_edit_rejected(self):
        data, row = fixture()
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            translate_metadata(data, [row, row])
        row['reference']['offset'] = 34
        with self.assertRaisesRegex(ValueError, 'outside'):
            translate_metadata(data, [row])

    def test_placeholder_loss_and_control_order_rejected(self):
        data, row = fixture('확인 {0}/10d/20d')
        row['target'] = 'OK/10d/20d'
        with self.assertRaisesRegex(ValueError, 'controls'):
            translate_metadata(data, [row])
        row['target'] = 'OK {0}/20d/10d'
        with self.assertRaisesRegex(ValueError, 'reordered'):
            translate_metadata(data, [row])
