"""Detect supported optional plugins without installing or removing any mod."""
import copy
from english_resources import safe, sha


def select_patch(game, manifest, state):
    patch = copy.deepcopy(manifest)
    if not manifest.get('automatic_mods'):
        return patch, [], None
    notices = []
    error = None
    unsupported = False
    managed = (state or {}).get('installed_files', {})
    for mod in manifest['automatic_mods']:
        path = mod['path']
        plugin = safe(game, path)
        # A duplicate or relocated plugin could be loaded instead of the expected one.
        plugins = safe(game, 'BepInEx/plugins')
        candidates = list(plugins.rglob('*.dll')) if plugins.is_dir() else []
        duplicates = [p for p in candidates if p.name.casefold() == plugin.name.casefold() and p.resolve() != plugin.resolve()]
        if duplicates:
            error = f"{mod['name']}: duplicate or relocated DLL. Use its standard plugin folder before patching."
        if not plugin.exists():
            notices.append(f"{mod['name']}: not installed")
            continue
        digest = sha(plugin)
        known = [mod['sha256']]
        if mod.get('translation'):
            known.append(mod['translation']['after_sha256'])
        if digest not in known:
            unsupported = True
            notices.append(f"{mod['name']}: unsupported version")
            continue
        notices.append(f"{mod['name']} {mod['version']}: detected")
        if mod.get('files'):
            patch['files'] = copy.deepcopy(mod['files'])
            patch['translation_profile'] = mod['name'] + ' (default settings)'
        if mod.get('translation'):
            row = mod['translation']
            if digest == row['before_sha256'] or path in managed:
                patch['files'].append(copy.deepcopy(row))
            else:
                notices[-1] += ' — already English; preserved'
    if unsupported:
        patch = copy.deepcopy(manifest)
        patch['translation_profile'] = 'Standard game (unsupported mod fallback)'
        notices.append('Unsupported mod version: standard translation only; all mod files preserved.')
    patch.setdefault('translation_profile', 'Standard game')
    return patch, notices, error
