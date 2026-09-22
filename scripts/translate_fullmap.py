"""Build a private, hash-pinned Fullmap English DLL; never edits its input.

The unsigned managed DLL keeps its method bodies and metadata intact. Replace
only display strings, and relocate the embedded JSON into an expanded final
readable PE section. Requires dnfile (kept in private/mod-inspection-deps here).
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import dnfile

ROOT = Path(__file__).resolve().parents[1]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def align(n, size):
    return (n + size - 1) // size * size

def build(source, output):
    profile = json.loads((ROOT/'localization/mods/zephyr-fullmap-1.8.0.json').read_text())
    original = source.read_bytes()
    if sha(original) != profile['source_sha256']:
        raise ValueError('Unsupported Fullmap DLL; expected original 1.8.0.')
    if (ROOT/'private').resolve() not in output.resolve().parents or output.exists():
        raise ValueError('Use a new file inside private/.')
    pe = dnfile.dnPE(data=original)
    if pe.net.struct.StrongNameSignatureSize or pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].Size:
        raise ValueError('Signed images are not supported.')
    resources = pe.net.resources
    if len(resources) != 1 or resources[0].name != 'fullmap_data.json':
        raise ValueError('Unexpected managed resources.')
    mapping = {r['original']: r['target'] for r in profile['rows']}
    data = json.loads(resources[0].data)
    counts = {}
    def translate(value):
        if isinstance(value, dict):
            return {k:translate(v) for k,v in value.items()}
        if isinstance(value, list):
            return [translate(v) for v in value]
        if isinstance(value, str) and re.search('[가-힣]', value):
            if value not in mapping: raise ValueError('Untranslated label: '+value)
            counts[value] = counts.get(value, 0) + 1
            return mapping[value]
        return value
    translated = translate(data)
    payload = json.dumps(translated, ensure_ascii=False, separators=(',',':')).encode()
    result = bytearray(original)
    heap = pe.net.user_strings
    heap_base = pe.get_offset_from_rva(pe.net.struct.MetaDataRva) + heap.struct.Offset
    offset = 1
    edited = []
    while offset < len(heap.__data__) and heap.__data__[offset]:
        item = heap.get(offset)
        if item.value in mapping:
            old = item.value.encode('utf-16le')
            new = mapping[item.value].encode('utf-16le')
            if len(new) > len(old): raise ValueError('Display literal exceeds allocation.')
            new += b' \x00' * ((len(old)-len(new))//2)
            prefix = item.raw_size - len(old) - 1
            start = heap_base + offset + prefix
            assert result[start:start+len(old)] == old
            result[start:start+len(old)] = new
            # Both UI replacements are ASCII without special characters.
            result[start+len(old)] = 0
            edited.append(item.value)
        offset += item.raw_size
    if set(mapping)-set(counts) != set(edited):
        raise ValueError('Review strings do not match resource and literal coverage.')
    last = pe.sections[-1]
    if last.Name.rstrip(b'\0') != b'.reloc' or len(original) != last.PointerToRawData+last.SizeOfRawData:
        raise ValueError('Unexpected final section/overlay.')
    at = align(len(result), pe.OPTIONAL_HEADER.FileAlignment)
    block = struct.pack('<I',len(payload)) + payload
    result.extend(b'\0'*(at-len(result)))
    result.extend(block)
    virtual_size = len(result)-last.PointerToRawData
    raw_size = align(virtual_size, pe.OPTIONAL_HEADER.FileAlignment)
    result.extend(b'\0'*(last.PointerToRawData+raw_size-len(result)))
    def set32(obj, field, value):
        struct.pack_into('<I', result, obj.get_field_absolute_offset(field), value)
    set32(last,'Misc_VirtualSize',virtual_size)
    set32(last,'SizeOfRawData',raw_size)
    set32(last,'Characteristics',last.Characteristics & ~0x02000000) # retain resource pages
    set32(pe.OPTIONAL_HEADER,'SizeOfImage',align(last.VirtualAddress+virtual_size,pe.OPTIONAL_HEADER.SectionAlignment))
    set32(pe.OPTIONAL_HEADER,'SizeOfInitializedData',pe.OPTIONAL_HEADER.SizeOfInitializedData+raw_size-last.SizeOfRawData)
    set32(pe.net.struct,'ResourcesRva',last.VirtualAddress+at-last.PointerToRawData)
    set32(pe.net.struct,'ResourcesSize',len(block))
    set32(pe.OPTIONAL_HEADER,'CheckSum',0)
    check = dnfile.dnPE(data=bytes(result))
    set32(pe.OPTIONAL_HEADER,'CheckSum',check.generate_checksum())
    check = dnfile.dnPE(data=bytes(result))
    assert json.loads(check.net.resources[0].data) == translated
    # No code or method tokens changed; the only #US edits are the two UI literals.
    for method in pe.net.mdtables.MethodDef:
        if method.Rva:
            from dncil.cil.body import CilMethodBody
            from dncil.cil.body.reader import CilMethodBodyReaderBytes
            body=CilMethodBody(CilMethodBodyReaderBytes(pe.get_data(method.Rva)))
            assert pe.get_data(method.Rva,body.size)==check.get_data(method.Rva,body.size)
    for a,b in zip(pe.net.mdtables.ManifestResource,check.net.mdtables.ManifestResource):
        assert a.struct.__pack__()==b.struct.__pack__()
    for key in pe.net.metadata.streams:
        if key!=b'#US':assert pe.net.metadata.streams[key].__data__==check.net.metadata.streams[key].__data__
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(result)
    return dict(source_sha256=sha(original),target_sha256=sha(result),json_occurrences=sum(counts.values()),unique_json_labels=len(counts),literal_edits=len(edited),method_bodies_unchanged=True,output=str(output))

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    print(json.dumps(build(a.source,a.output),indent=2))
