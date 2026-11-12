import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class AudioCaptureCatalogTests(unittest.TestCase):
    def test_reviewed_sources_and_proposed_scenarios(self):
        patterns = json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))
        sources = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
        qa = json.loads((ROOT / "data/audio-capture-scenarios.json").read_text(encoding="utf-8"))
        cards = {x["id"]: x for x in patterns["cards"]}
        urls = {x["url"]: x for x in sources["sources"]}
        expected = {"audio-capture-discontinuity-evidence", "audio-clock-domain-reconciliation", "audio-capture-packet-epoch"}
        self.assertTrue(expected <= cards.keys())
        self.assertEqual(patterns["version"], qa["version"])
        self.assertEqual(4, len(qa["items"]))
        for pid in expected:
            card = cards[pid]
            self.assertEqual("reviewed", card["source_review"])
            for url in card["source_urls"]:
                self.assertEqual("reviewed", urls[url]["status"])
                self.assertIn(pid, urls[url]["patterns"])
        for item in qa["items"]:
            self.assertEqual("proposed", item["decision_status"])
            self.assertTrue(set(item["must_consider"]) <= cards.keys())

if __name__ == "__main__":
    unittest.main()
