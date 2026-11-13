"""Offline contract checks for C# creation pattern research wave; no production QA."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = "https://github.com/anupavanm/csharp-design-patterns-for-humans"
IDS = {"factory-method-creation-seam", "abstract-factory-consistent-family"}


class CsharpCreationCatalogTests(unittest.TestCase):
    def test_reviewed_source_is_bidirectionally_linked(self):
        cards = json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))["cards"]
        sources = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))["sources"]
        chosen = {card["id"]: card for card in cards if card["id"] in IDS}
        self.assertEqual(set(chosen), IDS)
        source = next(item for item in sources if item["url"] == SOURCE)
        self.assertEqual(source["status"], "reviewed")
        self.assertEqual(set(source["patterns"]), IDS)
        for card in chosen.values():
            self.assertEqual(card["source_review"], "reviewed")
            self.assertEqual(card["source_urls"], [SOURCE])
            for field in ("signals", "approach", "avoid", "verification"):
                self.assertTrue(card[field].strip())

    def test_proposed_qa_is_not_claimed_executed(self):
        cases = json.loads((ROOT / "data/qa-scenarios.json").read_text(encoding="utf-8"))["items"]
        selected = [case for case in cases if case["id"] in {
            "klidan-factory-method-creation-seam", "klidan-abstract-factory-family"
        }]
        self.assertEqual(len(selected), 2)
        for case in selected:
            self.assertEqual(case["decision_status"], "proposed")
            self.assertTrue(set(case["must_consider"]) & IDS)
            self.assertTrue(case["acceptance"])

    def test_upstream_backlog_remains_distinct_from_review(self):
        backlog = json.loads((ROOT / "data/upstream-index.json").read_text(encoding="utf-8"))
        entry = next(item for item in backlog["items"] if item["url"] == SOURCE)
        self.assertEqual(entry["review_status"], "not_reviewed_from_index")


if __name__ == "__main__":
    unittest.main()
