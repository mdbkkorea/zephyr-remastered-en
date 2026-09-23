"""Release version and user-facing installer filenames."""
import re

VERSION = '1.0.0-beta.5'


def distribution_name(platform, version=VERSION):
    labels = {'steam': 'Steam', 'purple': 'Purple', 'macos': 'Macos', 'linux': 'Linux'}
    match = re.fullmatch(r'(\d+\.\d+\.\d+)-beta\.(\d+)', version)
    if platform not in labels or not match:
        raise ValueError('Expected steam/purple/macos/linux and a version such as 1.0.0-beta.5')
    return f'ZEnglish{labels[platform]}_{match[1]}_beta{int(match[2]):02d}'


if __name__ == '__main__':
    import json
    import sys
    from pathlib import Path
    platform = sys.argv[1]
    if platform == 'windows':
        manifest = json.loads((Path(__file__).parent / 'payload/manifest.json').read_text())
        platform = manifest.get('platform', 'steam')
        if platform not in ('steam', 'purple'):
            raise ValueError('Unsupported Windows edition')
        if manifest.get('release_version') != VERSION:
            raise ValueError('Build script and payload release versions do not match')
    print(distribution_name(platform))
