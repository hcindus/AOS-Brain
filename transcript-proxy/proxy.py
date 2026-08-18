#!/usr/bin/env python3
"""Transcript proxy for Um/Uh + Sovereign Bingo games.
Fetches YouTube transcripts server-side (the client can't due to CORS).

Endpoints:
  GET /transcript?url=<youtube-url>  -> {ok, videoId, title, text}
  GET /health                          -> {ok}
"""
import re
import json
import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PORT = 8095

def extract_video_id(url):
    url = url.strip()
    # youtu.be/ID
    m = re.search(r'youtu\.be/([A-Za-z0-9_-]{6,})', url)
    if m: return m.group(1)
    # watch?v=ID or embed/ID or shorts/ID
    m = re.search(r'(?:v=|embed/|shorts/)([A-Za-z0-9_-]{6,})', url)
    if m: return m.group(1)
    # bare ID
    if re.fullmatch(r'[A-Za-z0-9_-]{11}', url):
        return url
    return None

def fetch_transcript(video_id):
    """Try youtube-transcript-api, then yt-dlp."""
    errs = []
    # Try 1: youtube-transcript-api
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        tr = api.fetch(video_id)
        text = ' '.join(s.text for s in tr)
        return text, None
    except Exception as e:
        errs.append(f"transcript-api: {type(e).__name__}")

    # Try 2: yt-dlp
    try:
        import yt_dlp, subprocess, tempfile, os
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, 'sub')
            opts = {
                'skip_download': True,
                'writeautomaticsub': True,
                'writesubtitles': True,
                'subtitleslangs': ['en.*'],
                'subtitlesformat': 'vtt',
                'outtmpl': out,
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            for fn in os.listdir(d):
                if fn.endswith('.vtt'):
                    raw = open(os.path.join(d, fn), encoding='utf-8', errors='ignore').read()
                    text = vtt_to_text(raw)
                    return text, None
        errs.append("yt-dlp: no vtt produced")
    except Exception as e:
        errs.append(f"yt-dlp: {type(e).__name__}")

    return None, "; ".join(errs)

def vtt_to_text(vtt):
    lines = vtt.split('\n')
    out = []
    for ln in lines:
        ln = ln.strip()
        if not ln: continue
        if '-->' in ln: continue
        if ln.startswith('WEBVTT') or ln.startswith('Kind:') or ln.startswith('Language:'): continue
        if re.match(r'^\d+$', ln): continue
        # strip inline tags
        ln = re.sub(r'<[^>]+>', '', ln)
        out.append(ln)
    text = ' '.join(out)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/health':
            self._send(200, {'ok': True})
            return
        if parsed.path == '/transcript':
            q = parse_qs(parsed.query)
            url = (q.get('url') or [''])[0]
            vid = extract_video_id(url)
            if not vid:
                self._send(400, {'ok': False, 'error': 'Could not parse a YouTube video ID from that URL.'})
                return
            text, err = fetch_transcript(vid)
            if text is None:
                self._send(502, {'ok': False, 'videoId': vid, 'error': f'Transcript unavailable (server IP may be blocked by YouTube). Details: {err}'})
                return
            self._send(200, {'ok': True, 'videoId': vid, 'text': text})
            return
        self._send(404, {'ok': False, 'error': 'Not found'})

    def log_message(self, *a):
        pass

if __name__ == '__main__':
    print(f"Transcript proxy on :{PORT}")
    HTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
