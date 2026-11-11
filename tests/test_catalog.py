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


if __name__ == '__main__':
    unittest.main()
