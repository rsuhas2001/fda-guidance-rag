import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag_engine import PharmaRAGEngine
from app.schemas import QueryRequest


class TestFDAGuidanceRAGEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = PharmaRAGEngine()

    def test_corpus_loaded_with_fourteen_documents(self):
        doc_ids = {c.doc_id for c in self.engine.chunks}
        self.assertEqual(len(doc_ids), 14)
        self.assertIn("FDA-ELASTOMERS-CMC", doc_ids)
        self.assertIn("CFR-201-LABELING", doc_ids)
        self.assertIn("CFR-211-CGMP", doc_ids)
        self.assertIn("FDA-OOS-2006", doc_ids)

    def test_in_scope_usp_381_query(self):
        req = QueryRequest(
            question="What are the FDA CMC elastomeric closure penetrability and fragmentation limits for elastomeric vial stoppers?",
            top_k=4,
            strict_grounding=True,
        )
        resp = self.engine.answer_query(req)
        self.assertFalse(resp.telemetry.abstained)
        self.assertEqual(resp.citations[0].doc_id, "FDA-ELASTOMERS-CMC")
        self.assertTrue("10 N" in resp.answer or "48" in resp.answer)
        self.assertGreaterEqual(resp.telemetry.groundedness_score, 0.85)

    def test_in_scope_cfr_211_cgmp_query(self):
        req = QueryRequest(
            question="Under 21 CFR 211.84 and 211.170, what incoming test is mandatory and how long are reserve samples retained?",
            top_k=4,
        )
        resp = self.engine.answer_query(req)
        self.assertFalse(resp.telemetry.abstained)
        self.assertEqual(resp.citations[0].doc_id, "CFR-211-CGMP")
        self.assertIn("identity", resp.answer.lower())

    def test_out_of_scope_abstention_guardrail(self):
        req = QueryRequest(
            question="Who won the UEFA Champions League final in 2023 and what was the score?",
            top_k=4,
            strict_grounding=True,
        )
        resp = self.engine.answer_query(req)
        self.assertTrue(resp.telemetry.abstained)
        self.assertIn("ABSTAIN", resp.answer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
