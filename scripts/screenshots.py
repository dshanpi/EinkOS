#!/usr/bin/env python3
"""Encode real LVGL frames as PNG and prepare the daemon's HTML for browser capture."""
import ast
import hashlib
import html
import json
from pathlib import Path
import re
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/screenshots'


def chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))


def png_from_pgm(path):
    magic, dimensions, maximum, pixels = path.read_bytes().split(b'\n', 3)
    width, height = map(int, dimensions.split())
    assert magic == b'P5' and maximum == b'255'
    assert (width, height) == (240, 360) and len(pixels) == width * height
    assert set(pixels) == {0, 255}, f'Empty/non-monochrome rendering: {path}'
    scanlines = b''.join(b'\0' + pixels[y * width:(y + 1) * width] for y in range(height))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 0, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(scanlines, 9)) + chunk(b'IEND', b''))


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    captures = []
    for frame in sorted((ROOT / 'build/preview/frames').glob('*.pgm')):
        target = OUTPUT / (frame.stem + '.png')
        target.write_bytes(png_from_pgm(frame))
        captures.append({'file': target.name, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    assert len(captures) == 26, 'Expected all 11 desktop routes and documented state variants'
    inputs = ['src/ui.c', 'src/ui.h', 'src/lunar.c', 'src/settings.c', 'src/font_cjk_16.c',
              'src/lv_conf.h', 'tools/ui_capture.c', 'VERSION', 'platforms/tina/epd_disp.c']
    manifest = {'method': 'Actual LVGL 8.3.1 memory framebuffer; production ui.c and fonts; EPD threshold',
                'hardware_capture': False, 'size': [240, 360],
                'data': 'Fixed demo clock, fictional networks/devices/stats/text; no live device data',
                'inputs': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                'images': captures}
    (OUTPUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    source = (ROOT / 'platforms/tina/connectd.c').read_text()
    match = re.search(r'snprintf\(page, sizeof\(page\), ("(?:\\.|[^"\\])*"), networks\);', source)
    assert match, 'Portal template changed: update capture extraction'
    options = ''.join('<option value="%s">%s · %ddBm · %s</option>' % (html.escape(ssid), html.escape(ssid), signal, secure)
                      for ssid, signal, secure in [('EinkOS-Demo', -42, '加密'), ('Reading-Room', -58, '加密'), ('Guest', -71, '开放')])
    preview = ROOT / 'build/preview'
    (preview / 'portal.html').write_text(ast.literal_eval(match.group(1)) % options)
    for status, name in [('200 OK', 'portal-success'), ('400 Bad Request', 'portal-failure')]:
        pattern = r'http_reply\(client, "' + re.escape(status) + r'", ("<meta(?:\\.|[^"\\])*")\);'
        match = re.search(pattern, source)
        assert match, 'Portal response changed: update capture extraction'
        (preview / (name + '.html')).write_text(ast.literal_eval(match.group(1)))
    print(f'Wrote {len(captures)} actual LVGL screenshots and 3 HTML preview fixtures')


if __name__ == '__main__':
    main()
