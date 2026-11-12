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

    def test_sqlite_dataroot_patterns_have_reviewed_sources(self):
        catalog = json.loads((ROOT / 'data' / 'patterns.json').read_text(encoding='utf-8'))
        sources = json.loads((ROOT / 'data' / 'sources.json').read_text(encoding='utf-8'))
        by_id = {c['id']: c for c in catalog['cards']}
        by_url = {s['url']: s for s in sources['sources']}
        expected = {'sqlite-cross-store-intent', 'sqlite-wal-checkpoint-control',
                    'sqlite-wal-durability-policy', 'sqlite-online-backup',
                    'sqlite-write-contention', 'sqlite-integrity-recovery-gate'}
        self.assertTrue(expected <= by_id.keys())
        for pid in expected:
            self.assertTrue(any(by_url[url]['status'] == 'reviewed'
                                for url in by_id[pid]['source_urls']))

    def test_sqlite_recovery_contract_has_failure_boundaries(self):
        text = (ROOT / 'references' / 'sqlite-dataroot-recovery-contract.md').read_text(encoding='utf-8')
        for token in ('RootId', 'pending', 'readback', 'cross-volume', 'power loss',
                      'foreign_key_check', 'ReplaceFileW'):
            self.assertIn(token, text)


    def test_staya_machine_readable_scenarios(self):
        from pathlib import Path
        doc = json.loads((ROOT / 'data' / 'staya-scenarios.json').read_text(encoding='utf-8'))
        catalog = json.loads((ROOT / 'data' / 'patterns.json').read_text(encoding='utf-8'))
        ids = {item['id'] for item in catalog['cards']}
        self.assertEqual(doc['schema_version'], 1)
        self.assertEqual(doc['version'], catalog['version'])
        self.assertEqual(len(doc['items']), 6)
        for case in doc['items']:
            self.assertEqual(case['decision_status'], 'proposed')
            self.assertTrue(set(case['must_consider']) <= ids)
            self.assertGreaterEqual(len(case['acceptance']), 2)

    def test_staya_p1_cards_have_reviewed_sources(self):
        catalog = json.loads((ROOT / 'data' / 'patterns.json').read_text(encoding='utf-8'))
        sources = json.loads((ROOT / 'data' / 'sources.json').read_text(encoding='utf-8'))
        cards = {item['id']: item for item in catalog['cards']}
        by_url = {item['url']: item for item in sources['sources']}
        required = {'ipc-request-deadline', 'ipc-protocol-format-guard', 'ipc-generation-fence',
                    'staya-subscription-ssrf-boundary', 'staya-subscription-normalization',
                    'staya-active-path-health', 'staya-staged-config-promotion', 'staya-secret-lifecycle'}
        self.assertTrue(required <= cards.keys())
        for pid in required:
            card = cards[pid]
            self.assertEqual(card['source_review'], 'reviewed')
            self.assertTrue(all(by_url[url]['status'] == 'reviewed' for url in card['source_urls']))

    def test_staya_contract_separates_preflight_and_live(self):
        content = (ROOT / 'references' / 'staya-ipc-resilience-security-contract.md').read_text(encoding='utf-8')
        for term in ('SSRF', 'leastLoad', 'rollback', 'end-to-end', 'DOC_REVIEW', 'LIVE_TRANSPORT_QA'):
            self.assertIn(term, content)

    def test_devops_scenarios_are_proposed_and_referential(self):
        db = json.loads((ROOT / 'data' / 'patterns.json').read_text(encoding='utf-8'))
        src = json.loads((ROOT / 'data' / 'devops-scenarios.json').read_text(encoding='utf-8'))
        valid_ids = {p['id'] for p in db['cards']}
        self.assertEqual(src['version'], db['version'])
        self.assertEqual(len(src['items']), 8)
        for case in src['items']:
            self.assertEqual(case['decision_status'], 'proposed')
            self.assertTrue(set(case['must_consider']) <= valid_ids)
            self.assertGreaterEqual(len(case['acceptance']), 2)

    def test_devops_patterns_reference_reviewed_sources(self):
        db = json.loads((ROOT / 'data' / 'patterns.json').read_text(encoding='utf-8'))
        src = json.loads((ROOT / 'data' / 'sources.json').read_text(encoding='utf-8'))
        by_id = {p['id']: p for p in db['cards']}
        by_url = {p['url']: p for p in src['sources']}
        expected = {'config-caddy-validate-reload', 'compose-health-dependency',
                    'update-tuf-antirollback', 'update-publisher-signature-policy',
                    'windows-msi-custom-rollback', 'observability-bounded-cardinality',
                    'deployment-stage-journal', 'progressive-release-acceptance'}
        self.assertTrue(expected <= by_id.keys())
        for pid in expected:
            self.assertEqual(by_id[pid]['source_review'], 'reviewed')
            self.assertTrue(all(by_url[u]['status'] == 'reviewed' for u in by_id[pid]['source_urls']))

    def test_devops_contract_has_trust_and_runtime_boundaries(self):
        text = (ROOT / 'references' / 'devops-release-qa-contract.md').read_text(encoding='utf-8')
        for marker in ('WinVerifyTrust', 'TUF', 'MSI', 'depends_on', 'caddy validate',
                       'canary', 'rollback', 'cardinality'):
            self.assertIn(marker, text)

    def test_perf_cases_and_source_links(self):
        catalog = json.loads((ROOT / 'data' / 'patterns.json').read_text(encoding='utf-8'))
        sources = json.loads((ROOT / 'data' / 'sources.json').read_text(encoding='utf-8'))
        perf = json.loads((ROOT / 'data' / 'performance-scenarios.json').read_text(encoding='utf-8'))
        self.assertEqual(perf['version'], catalog['version'])
        self.assertEqual(len(perf['items']), 8)
        ids = {c['id'] for c in catalog['cards']}
        for case in perf['items']:
            self.assertEqual(case['decision_status'], 'proposed')
            self.assertTrue(set(case['must_consider']) <= ids)
            self.assertGreaterEqual(len(case['acceptance']), 2)
        urls = {s['url']: s for s in sources['sources']}
        for card in catalog['cards']:
            if card['id'] in {'pooled-buffer-ownership', 'bounded-channel-overflow-policy',
                              'concurrent-getoradd-side-effect', 'cache-size-revision-budget',
                              'latest-frame-coalescing', 'cancellation-source-lifecycle'}:
                self.assertTrue(all(urls[u]['status'] == 'reviewed' for u in card['source_urls']))

    def test_perf_contract_mentions_physical_limits(self):
        text = (ROOT / 'references' / 'performance-memory-contract.md').read_text(encoding='utf-8')
        for s in ('ArrayPool', 'GetOrAdd', 'AdvanceTo', 'Dispose', 'p95', 'Program'):
            self.assertIn(s, text)

    def test_all_scenario_versions_match_catalog(self):
        catalog = json.loads((ROOT / 'data' / 'patterns.json').read_text(encoding='utf-8'))
        for filename in ('staya-scenarios.json', 'devops-scenarios.json', 'performance-scenarios.json'):
            content = json.loads((ROOT / 'data' / filename).read_text(encoding='utf-8'))
            self.assertEqual(content['version'], catalog['version'])

if __name__ == '__main__':
    unittest.main()
