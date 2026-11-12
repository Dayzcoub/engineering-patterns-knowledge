"""Offline behavior checks, independent of external URLs."""
import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent


class CatalogTests(unittest.TestCase):
    def test_validator(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'validate.py')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('errors=0', result.stdout)

    def test_upstream_index_is_backlog_not_review(self):
        index = json.loads((ROOT / 'data' / 'upstream-index.json').read_text(encoding='utf-8'))
        self.assertEqual(index['unique_urls'], 115)
        self.assertEqual(index['link_occurrences'], 122)
        self.assertTrue(all(item['review_status'] == 'not_reviewed_from_index' for item in index['items']))

    def test_search_project_json(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts' / 'search_patterns.py'), '--project', 'KLIDAN', '--json', 'reconnect'],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        cards = json.loads(result.stdout)
        self.assertTrue(cards, 'query should return some matches')
        self.assertTrue(all('KLIDAN' in card['projects'] for card in cards))

    def test_search_domain_and_limit(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts' / 'search_patterns.py'), '--domain', 'audio', '--limit', '1', '--json'],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        cards = json.loads(result.stdout)
        self.assertEqual(len(cards), 1)
        self.assertTrue(all(card['domain'] == 'audio' for card in cards))

    def test_p0_audio_primary_sources(self):
        catalog = json.loads((ROOT / 'data' / 'patterns.json').read_text(encoding='utf-8'))
        sources = json.loads((ROOT / 'data' / 'sources.json').read_text(encoding='utf-8'))
        by_id = {c['id']: c for c in catalog['cards']}
        by_url = {s['url']: s for s in sources['sources']}
        expected = {'wasapi-period-lattice', 'wasapi-actual-buffer-readback',
                    'audio-minimum-stable-profile', 'wasapi-invalid-device-recovery',
                    'audio-stream-shutdown-barrier'}
        self.assertTrue(expected <= by_id.keys())
        for pid in expected:
            card = by_id[pid]
            self.assertEqual(card['source_review'], 'reviewed')
            self.assertTrue(any(by_url[u]['status'] == 'reviewed' for u in card['source_urls']))

    def test_ross_bencina_remains_pending(self):
        sources = json.loads((ROOT / 'data' / 'sources.json').read_text(encoding='utf-8'))
        ross = next(s for s in sources['sources'] if 'rossbencina.com' in s['url'])
        self.assertEqual(ross['status'], 'pending_primary_review')

    def test_audio_profile_contract_requires_physical_evidence(self):
        text = (ROOT / 'references' / 'audio-probe-profile-contract.md').read_text(encoding='utf-8')
        for marker in ('NO_STABLE_PROFILE', 'GetBufferSize', '60/300/600', 'hardwareEvidence'):
            self.assertIn(marker, text)

    def test_p0_wpf_patterns_and_sources(self):
        catalog = json.loads((ROOT / 'data' / 'patterns.json').read_text(encoding='utf-8'))
        source_doc = json.loads((ROOT / 'data' / 'sources.json').read_text(encoding='utf-8'))
        by_id = {card['id']: card for card in catalog['cards']}
        urls = {item['url']: item for item in source_doc['sources']}
        expected = {'wpf-responsive-layout', 'wpf-per-monitor-dpi', 'wpf-dispatcher-ownership',
                    'wpf-async-generation-guard', 'wpf-virtualized-list', 'wpf-focus-scope'}
        self.assertTrue(expected.issubset(by_id))
        for pid in expected:
            card = by_id[pid]
            self.assertEqual(card['source_review'], 'reviewed')
            self.assertTrue(all(urls[u]['status'] == 'reviewed' for u in card['source_urls']))

    def test_wpf_contract_covers_fullhd_dpi_and_late_replies(self):
        content = (ROOT / 'references' / 'wpf-fullhd-dpi-contract.md').read_text(encoding='utf-8')
        for token in ('1920×1080', '100%', '125%', '150%', 'WorkArea',
                      'Dispose', 'Dispatcher', 'virtualization'):
            self.assertIn(token, content)


if __name__ == '__main__':
    unittest.main()
