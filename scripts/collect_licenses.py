"""Collect notices from installed build dependencies; no game paths are read."""
import importlib.metadata as metadata,json,re,shutil,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'licenses'/'python';out.mkdir(parents=True,exist_ok=True)
names=['UnityPy','numpy','spooky','pillow','lz4','brotli','texture2ddecoder','etcpak','astc-encoder-py','fmod_toolkit','fsspec','attrs','tpk_ar','archspec','pyfmodex','setuptools','packaging','pyinstaller','pyinstaller-hooks-contrib']
rows=[]
for name in names:
 d=metadata.distribution(name);dest=out/name;dest.mkdir(exist_ok=True);copied=[]
 for f in d.files or []:
  if not re.search(r'(^|/)(licenses?|copying|notice|authors)([./_-]|$)',str(f),re.I):continue
  src=Path(d.locate_file(f))
  if not src.is_file() or src.suffix.lower() in ['.py','.pyc','.exe','.dll']:continue
  target=dest/str(f).replace('/','__').replace('\\','__');shutil.copy2(src,target);copied.append(target.name)
 if not copied:
  license_text=d.metadata.get('License') or d.metadata.get('License-Expression') or 'See upstream project.'
  (dest/'LICENSE-METADATA.txt').write_text(license_text,encoding='utf8')
 rows.append(dict(name=name,version=d.version,license=d.metadata.get('License-Expression') or d.metadata.get('License','').split('\n')[0],notices=copied))
shutil.copy2(Path(sys.base_prefix)/'LICENSE.txt',out/'Python-LICENSE.txt')
(root/'dependency-versions.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
print('Collected notices for',len(rows),'packages and Python')
