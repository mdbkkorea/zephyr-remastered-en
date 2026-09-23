"""Open the private NAS review in Safari using a loopback-only Mac server."""
import errno
import hashlib
import json
from pathlib import Path
import subprocess
import threading
import urllib.request
from server import make_server

root=Path(__file__).resolve().parent.parent
page=root/'Web/index.html'
notes=root/'Suggestions'
url='http://127.0.0.1:8766/'
if not page.is_file():
    raise SystemExit('Review HTML not found. Keep this launcher inside the NAS review folder.')
try:
    server=make_server(page,notes,['http://127.0.0.1:8766','http://localhost:8766'],8766)
except OSError as ex:
    if ex.errno != errno.EADDRINUSE: raise
    try:
        data=json.load(urllib.request.urlopen(url+'api/health',timeout=3))
        expected=hashlib.sha256(str(notes.resolve()).encode()).hexdigest()
        if data.get('service')!='zephyr-review' or data.get('storage_id')!=expected:raise ValueError('Different service')
    except Exception:
        raise SystemExit('Port 8766 is busy. Close the previous review server and try again.')
    subprocess.run(['open','-a','Safari',url],check=True)
    print('Opened the existing review session in Safari.')
else:
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    subprocess.run(['open','-a','Safari',url],check=True)
    print('\nReview is open in Safari: '+url)
    print('Markdown suggestions save to: '+str(notes))
    print('Keep this Terminal window open while reviewing. Press Control-C to stop.')
    try:worker.join()
    except KeyboardInterrupt:print('\nReview server stopped. Saved suggestions remain on the NAS.')
    finally:server.shutdown();server.server_close()
