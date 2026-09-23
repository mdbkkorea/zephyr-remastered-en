"""Package a prepared kit with bounded, Windows Explorer-friendly paths."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

MAX_MEMBER_UNITS = 60
# Includes a conservatively long extraction destination; reserve room below 260.
DESTINATION_BUDGET = 180

def units(text):
    return len(text.encode('utf-16-le')) // 2

def package(kit, destination):
    kit, destination = Path(kit), Path(destination)
    manifest = json.loads((kit / 'payload/manifest.json').read_text())
    edition = manifest.get('platform', 'steam')
    if edition not in ('steam', 'purple'):
        raise ValueError('Unknown game edition')
    prefix = 'ZSteam' if edition == 'steam' else 'ZPurple'
    entries = {}
    notices = []
    for path in sorted(kit.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(kit)
        if any(p in ('__pycache__', '.build-venv', 'build', 'dist', '.git') for p in rel.parts) or path.suffix == '.pyc':
            continue
        name = rel.as_posix()
        data = path.read_bytes()
        if rel.parts[0] == 'licenses':
            short = f'licenses/L{len(notices)+1:03d}.txt'
            notices.append({'file': short, 'original_path': name, 'sha256': hashlib.sha256(data).hexdigest()})
            name = short
        member = prefix + '/' + name
        if units(member) > MAX_MEMBER_UNITS or DESTINATION_BUDGET + 1 + units(member) >= 260:
            raise ValueError('ZIP member path exceeds Windows packaging budget: ' + member)
        if any(p.endswith((' ', '.')) or any(c in p for c in '<>:"\\|?*') for p in member.split('/')):
            raise ValueError('Invalid Windows member name: ' + member)
        key = member.casefold()
        if key in entries:
            raise ValueError('Case-insensitive ZIP path collision: ' + member)
        entries[key] = (member, data)
    index = (prefix + '/licenses/INDEX.json', json.dumps(notices, ensure_ascii=False, indent=2).encode('utf8'))
    if index[0].casefold() in entries:
        raise ValueError('License index collision')
    entries[index[0].casefold()] = index
    if destination.exists():
        raise ValueError('Refusing to replace an existing distribution ZIP')
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in entries.values():
                archive.writestr(name, data)
        with zipfile.ZipFile(destination) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP integrity check failed')
            for name, data in entries.values():
                if archive.read(name) != data:
                    raise ValueError('ZIP content mismatch: ' + name)
        return {'archive': str(destination), 'edition': edition, 'files': len(entries),
                'license_files_preserved': len(notices),
                'max_member_utf16_units': max(units(name) for name, _ in entries.values()),
                'destination_budget': DESTINATION_BUDGET,
                'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}
    except Exception:
        destination.unlink(missing_ok=True)
        raise

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kit', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(package(a.kit, a.output), indent=2))
