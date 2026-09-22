"""Apply optional, identity-pinned translation changes for a supported mod."""
import copy
import json
from pathlib import Path

PROFILE = Path(__file__).resolve().parents[1] / 'localization/mods/zephyr-passives-2.4.3.json'


def apply_profile(rows):
    profile = json.loads(PROFILE.read_text(encoding='utf-8'))
    result = copy.deepcopy(rows)
    by_id = {r['id']: r for r in result}
    seen = set()
    for edit in profile['overrides']:
        if edit['id'] in seen:
            raise ValueError('Duplicate mod override: ' + edit['id'])
        seen.add(edit['id'])
        row = by_id.get(edit['id'])
        if row is None or any(row[k] != edit[k] for k in ('original', 'reference')) or row['target'] != edit['base_target']:
            raise ValueError('Mod override no longer matches base translation: ' + edit['id'])
        row['target'] = edit['target']
    return result, profile
