import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CaptureWorkerCatalogTests(unittest.TestCase):
    def test_worker_cards_and_proposed_cases(self):
        p = json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))
        s = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
        q = json.loads((ROOT / "data/audio-capture-scenarios.json").read_text(encoding="utf-8"))
        cards = {c["id"]: c for c in p["cards"]}
        sources = {x["url"]: x for x in s["sources"]}
        for cid in ("audio-capture-stop-reset-barrier", "audio-capture-invalidation-recovery"):
            c = cards[cid]
            self.assertEqual("reviewed", c["source_review"])
            for field in ("signals", "approach", "avoid", "verification"):
                self.assertTrue(c[field])
            for url in c["source_urls"]:
                self.assertEqual("reviewed", sources[url]["status"])
                self.assertIn(cid, sources[url]["patterns"])
        self.assertEqual(10, len(q["items"]))
        for case in q["items"]:
            self.assertEqual("proposed", case["decision_status"])
            self.assertTrue(set(case["must_consider"]) <= cards.keys())
        for path in (ROOT / "data").glob("*-scenarios.json"):
            self.assertEqual(p["version"], json.loads(path.read_text(encoding="utf-8"))["version"])

if __name__ == "__main__":
    unittest.main()
