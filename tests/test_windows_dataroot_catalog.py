"""Offline Windows DataRoot publication knowledge tests. No Win32 operations executed."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
IDS = ("windows-replacefile-partial-failure-recovery", "windows-cross-volume-publish-copy-delete-boundary")

class WindowsDataRootCatalogTests(unittest.TestCase):
    def test_cards_and_reverse_sources(self):
        cards = {x["id"]: x for x in json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))["cards"]}
        sources = {x["url"]: x for x in json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))["sources"]}
        for key in IDS:
            card = cards[key]
            self.assertEqual(card["source_review"], "reviewed")
            for field in ("signals", "approach", "avoid", "verification"):
                self.assertTrue(card[field])
            for url in card["source_urls"]:
                self.assertEqual(sources[url]["status"], "reviewed")
                self.assertIn(key, sources[url]["patterns"])

    def test_failure_codes_and_non_atomic_copy_delete(self):
        cards = {x["id"]: x for x in json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))["cards"]}
        text = cards[IDS[0]]["signals"] + cards[IDS[0]]["verification"]
        for code in ("1175", "1176", "1177"):
            self.assertIn(code, text)
        self.assertIn("copy/delete", cards[IDS[1]]["approach"])

    def test_proposed_qa_and_versions(self):
        paths = ("patterns.json", "sources.json", "qa-scenarios.json", "audio-capture-scenarios.json", "devops-scenarios.json", "performance-scenarios.json", "staya-scenarios.json", "wpf-accessibility-scenarios.json")
        catalogs = [json.loads((ROOT / "data" / p).read_text(encoding="utf-8")) for p in paths]
        self.assertEqual({x["version"] for x in catalogs}, {"0.9.6-preview.1"})
        case = next(x for x in catalogs[2]["items"] if x["id"] == "windows-dataroot-publication-failure-matrix")
        self.assertEqual(case["decision_status"], "proposed")
        self.assertEqual(case["must_consider"], list(IDS))
