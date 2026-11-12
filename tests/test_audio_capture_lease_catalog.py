import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CaptureLeaseCatalogTests(unittest.TestCase):
    def test_reviewed_cards_and_proposed_cases(self):
        p = json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))
        s = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
        q = json.loads((ROOT / "data/audio-capture-scenarios.json").read_text(encoding="utf-8"))
        cards = {x["id"]: x for x in p["cards"]}
        sources = {x["url"]: x for x in s["sources"]}
        expected = {"audio-capture-buffer-lease", "audio-capture-packet-size-mode"}
        self.assertTrue(expected <= cards.keys())
        self.assertEqual(p["version"], q["version"])
        self.assertEqual(7, len(q["items"]))
        for cid in expected:
            c = cards[cid]
            self.assertEqual("reviewed", c["source_review"])
            self.assertTrue(c["signals"] and c["approach"] and c["avoid"] and c["verification"])
            for url in c["source_urls"]:
                self.assertEqual("reviewed", sources[url]["status"])
                self.assertIn(cid, sources[url]["patterns"])
        for case in q["items"]:
            self.assertEqual("proposed", case["decision_status"])
            self.assertTrue(set(case["must_consider"]) <= cards.keys())
        for path in (ROOT / "data").glob("*-scenarios.json"):
            self.assertEqual(p["version"], json.loads(path.read_text(encoding="utf-8"))["version"])

if __name__ == "__main__":
    unittest.main()
