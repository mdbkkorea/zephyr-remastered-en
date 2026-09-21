"""Optional display-name conversion; active saves remain untouched."""
import gzip
import json
from pathlib import Path

def prepare_saves(source, output, mapping):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.exists() or source == output or source in output.parents:
        raise ValueError('Choose a new output folder outside the saves folder.')
    changes = []
    def visit(value):
        if isinstance(value, dict):
            for key,item in value.items():
                if key in {'DialogueName','FullName','JobName'} and isinstance(item,str) and item in mapping:
                    if mapping[item] != item:
                        changes.append((key,item,mapping[item]))
                        value[key] = mapping[item]
                else: visit(item)
        elif isinstance(value,list):
            for item in value: visit(item)
    output.mkdir(parents=True)
    files = 0
    for path in sorted(source.rglob('save_*.dat')):
        before = path.read_bytes()
        if not before.startswith(b'\x1f\x8b'): continue
        data = json.loads(gzip.decompress(before))
        previous = len(changes)
        visit(data)
        if len(changes) == previous: continue
        dest = output/path.relative_to(source)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(gzip.compress(json.dumps(data,ensure_ascii=False,indent=2).encode(),mtime=0))
        if json.loads(gzip.decompress(dest.read_bytes())) != data or path.read_bytes() != before:
            raise ValueError('Save verification failed.')
        files += 1
    return f'Prepared {files} converted save copies in:\n{output}\n\nActive saves were not changed. Back them up and close the game before manually replacing matching files. Do not replace newer progress with an older converted copy.'


