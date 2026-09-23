"""Private review service. Bind only to loopback, behind the existing tailnet proxy."""
import argparse
import datetime as dt
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import threading
from urllib.parse import urlsplit

PREFIX = '<!-- zephyr-review-record '

class ReviewStore:
    def __init__(self, page, directory):
        self.page = Path(page)
        raw = self.page.read_text(encoding='utf8')
        data = re.search(r'<script id="data" type="application/json">(.*?)</script>', raw, re.S)
        self.rows = {r['id']: r for r in json.loads(data[1])}
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.latest = {}
        self.requests = {}
        for path in sorted(self.directory.glob('*.md')):
            with path.open(encoding='utf8') as f:
                first = f.readline().strip()
            if not first.startswith(PREFIX): continue
            record = json.loads(first[len(PREFIX):-4])
            self.requests[record['request_id']] = record
            old = self.latest.get(record['id'])
            if old is None or record['saved_at'] > old['saved_at']:
                self.latest[record['id']] = record

    def save(self, data):
        if not isinstance(data, dict): raise ValueError('Invalid request')
        row = self.rows.get(data.get('id'))
        if row is None: raise ValueError('Unknown review ID')
        if data.get('key') != row['key'] or data.get('en') != row['en']:
            raise ValueError('This review entry changed. Reload before saving.')
        for name in ('suggestion', 'explanation'):
            if not isinstance(data.get(name), str) or len(data[name]) > 20000:
                raise ValueError('Each field must be text, up to 20,000 characters.')
        if not data['suggestion'].strip() and not data['explanation'].strip():
            raise ValueError('Enter a suggestion or explanation first.')
        request_id = data.get('request_id', '')
        if not isinstance(request_id, str) or not re.fullmatch(r'[a-f0-9]{32}', request_id):
            raise ValueError('Invalid save identifier')
        with self.lock:
            if request_id in self.requests:
                previous = self.requests[request_id]
                if any(previous[k] != data[k] for k in ('id', 'key', 'en', 'suggestion', 'explanation')):
                    raise ValueError('Save identifier already used')
                return previous
            old = self.latest.get(row['id'])
            if data.get('revision') != (old['request_id'] if old else None):
                raise ValueError('A newer suggestion was saved elsewhere. Reload to review it first; your draft is kept in this browser.')
            now = dt.datetime.now(dt.timezone.utc)
            filename = row['id']+'-'+now.strftime('%Y%m%dT%H%M%S%fZ')+'-'+request_id[:8]+'.md'
            record = dict(row, suggestion=data['suggestion'], explanation=data['explanation'],
                          request_id=request_id, saved_at=now.isoformat(), filename=filename, status='pending')
            header = json.dumps(record, ensure_ascii=True).replace('<', '\\u003c')
            body = PREFIX+header+' -->\n\n# '+row['id']+' — Translation suggestion\n\nStatus: pending — apply only when requested.\n\nSaved (UTC): '+record['saved_at']+'\n\n'
            for title, value in [('Korean original', row['ko']), ('Current English', row['en']),
                                 ('Translation suggestion', data['suggestion']), ('Explanation', data['explanation']),
                                 ('Resource', row['location'])]:
                fence = '`' * max(3, max([len(x) + 1 for x in re.findall(r'`+', value)] or [3]))
                body += '## '+title+'\n\n'+fence+'text\n'+value+'\n'+fence+'\n\n'
            temp = self.directory/('.'+filename+'.tmp')
            try:
                with temp.open('x', encoding='utf8') as f:
                    f.write(body); f.flush(); os.fsync(f.fileno())
                os.replace(temp, self.directory/filename)
            finally:
                if temp.exists(): temp.unlink()
            self.latest[row['id']] = record
            self.requests[request_id] = record
            return record


def make_server(page, directory, origins, port):
    store = ReviewStore(page, directory)
    allowed = set(origins)
    hosts = {urlsplit(origin).netloc for origin in allowed}
    token = secrets.token_urlsafe(32)
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(30)
        def reply(self, status, value, kind='application/json; charset=utf-8'):
            body = json.dumps(value, ensure_ascii=False).encode() if kind.startswith('application/json') else value
            self.send_response(status)
            self.send_header('Content-Type', kind)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'same-origin')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers(); self.wfile.write(body)
        def valid_host(self):
            if self.headers.get('Host') not in hosts:
                self.reply(403, {'error':'Unrecognized host'}); return False
            return True
        def do_GET(self):
            if not self.valid_host(): return
            path = urlsplit(self.path).path
            if path in ('/', '/index.html'):
                self.reply(200, store.page.read_bytes(), 'text/html; charset=utf-8')
            elif path == '/api/health':
                self.reply(200, {'service':'zephyr-review', 'storage_id':hashlib.sha256(str(store.directory.resolve()).encode()).hexdigest()})
            elif path == '/api/suggestions':
                with store.lock:
                    self.reply(200, {'token':token, 'saved':store.latest})
            else: self.reply(404, {'error':'Not found'})
        def do_POST(self):
            if not self.valid_host(): return
            if self.path != '/api/suggestions': self.reply(404, {'error':'Not found'}); return
            if (self.headers.get('Origin') not in allowed or self.headers.get('X-Review-Token') != token
                    or self.headers.get('Content-Type') != 'application/json'):
                self.reply(403, {'error':'Reload the review page before saving.'}); return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 200000: raise ValueError('Invalid request size')
                data = json.loads(self.rfile.read(size))
                record = store.save(data)
                self.reply(200, {'record':record})
            except (ValueError, TypeError, KeyError) as ex: self.reply(400, {'error':str(ex)})
            except OSError: self.reply(500, {'error':'NAS storage write failed. Your draft has not been saved; please retry.'})
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.store = store
    return server

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--page', required=True)
    parser.add_argument('--suggestions', required=True)
    parser.add_argument('--origin', action='append', required=True)
    parser.add_argument('--port', type=int, default=8766)
    args = parser.parse_args()
    make_server(args.page, args.suggestions, args.origin, args.port).serve_forever()
