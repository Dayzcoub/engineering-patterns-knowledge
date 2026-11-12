"""Offline SQLite backup catalog contract tests."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent


class SQLiteBackupCatalogTests(unittest.TestCase):
    def test_reviewed_sources_and_reverse_links(self):
        cards = {c["id"]: c for c in json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))["cards"]}
        sources = {s["url"]: s for s in json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))["sources"]}
        for pid in ("sqlite-backup-bounded-lifecycle", "sqlite-backup-error-classification"):
            card = cards[pid]
            self.assertEqual(card["source_review"], "reviewed")
            for field in ("signals", "approach", "avoid", "verification"):
                self.assertTrue(card[field])
            for url in card["source_urls"]:
                self.assertEqual(sources[url]["status"], "reviewed")
                self.assertIn(pid, sources[url]["patterns"])

    def test_qa_remains_proposed(self):
        qa = json.loads((ROOT / "data/qa-scenarios.json").read_text(encoding="utf-8"))
        case = next(x for x in qa["items"] if x["id"] == "sqlite-backup-bounded-retry")
        self.assertEqual(case["decision_status"], "proposed")
        self.assertEqual(len(case["must_consider"]), 2)
        self.assertTrue(any("deadline" in x for x in case["acceptance"]))

    def test_version(self):
        cards = json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))
        qa = json.loads((ROOT / "data/qa-scenarios.json").read_text(encoding="utf-8"))
        self.assertEqual(cards["version"], qa["version"])
        self.assertEqual(cards["version"], "0.9.4-preview.1")
