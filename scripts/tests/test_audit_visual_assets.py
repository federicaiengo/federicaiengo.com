"""Unit tests for favicon format, metadata, and social preview preflight."""
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_visual_assets import audit


def png(width, height):
    def chunk(kind, data):
        return (struct.pack('>I', len(data)) + kind + data
                + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff))
    raw = b''.join(b'\0' + b'\0\0\0' * width for _ in range(height))
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))


def ico():
    images = [png(16, 16), png(32, 32)]
    header = struct.pack('<HHH', 0, 1, len(images))
    entries, offset = [], 6 + len(images) * 16
    for size, payload in zip((16, 32), images):
        entries.append(struct.pack('<BBBBHHII', size, size, 0, 0, 1, 32,
                                   len(payload), offset))
        offset += len(payload)
    return header + b''.join(entries) + b''.join(images)


class VisualAssetTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        (self.root / 'src/layouts').mkdir(parents=True)
        (self.root / 'public').mkdir()
        for size in (16, 32):
            (self.root / 'public' / f'fi-eclipse-{size}.png').write_bytes(png(size, size))
        (self.root / 'public/favicon.ico').write_bytes(ico())
        self.layout = self.root / 'src/layouts/Base.astro'
        self.layout.write_text(
            '<head>\n<link rel="icon" sizes="16x16" href="/fi-eclipse-16.png">\n'
            '<link rel="icon" sizes="32x32" href="/fi-eclipse-32.png">\n'
            '<link rel="shortcut icon" href="/favicon.ico">\n'
            '<meta property="og:image" content={new URL("/social-preview.svg", Astro.site)}>\n'
            '</head>', encoding='utf-8')

    def test_valid_production_icons(self):
        result = audit(self.root)
        self.assertEqual(result['errors'], [])
        self.assertEqual(len(result['validated']), 3)
        self.assertTrue(result['warnings'])

    def test_missing_asset(self):
        (self.root / 'public/fi-eclipse-16.png').unlink()
        self.assertTrue(any('missing' in e.lower() for e in audit(self.root)['errors']))

    def test_wrong_size_metadata(self):
        self.layout.write_text(self.layout.read_text().replace('sizes="32x32"', 'sizes="64x64"'))
        self.assertTrue(any('mismatch' in e.lower() for e in audit(self.root)['errors']))

    def test_bad_ico_header(self):
        (self.root / 'public/favicon.ico').write_bytes(b'NOT AN ICON')
        self.assertTrue(any('ICO' in e for e in audit(self.root)['errors']))

    def test_flat_svg_rejected(self):
        (self.root / 'public/favicon.svg').write_text('<svg></svg>')
        self.layout.write_text(self.layout.read_text().replace('/fi-eclipse-16.png', '/favicon.svg'))
        self.assertTrue(any('simplified' in e.lower() for e in audit(self.root)['errors']))

    def test_bad_social_png(self):
        self.layout.write_text(self.layout.read_text().replace('social-preview.svg', 'social-preview.png'))
        self.assertTrue(any('social preview PNG missing' in e for e in audit(self.root)['errors']))


if __name__ == '__main__':
    unittest.main()
