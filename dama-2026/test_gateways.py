"""python -m unittest -v  (mock mode, no model needed)"""
import os, sys, pathlib, unittest
os.environ["FR_BACKEND"] = "mock"
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE / "gateways"))
import g1_classify_redact as g1, g2_prompt_guard as g2, g3_context_scope as g3, g4_selfcheck_exit as g4
from common import POLICY, DATA


class Gateways(unittest.TestCase):
    def test_g1_redacts_every_sensitive_value(self):
        rec = DATA["contact_sheet"]
        out = str(g1.redact(rec))
        for f in POLICY["sensitive_fields"]:
            self.assertNotIn(rec[f], out)
        self.assertEqual(g1.route({"SENSITIVE"}), "local-only")

    def test_g1_pattern_catches_ssn_in_unexpected_field(self):
        self.assertEqual(g1.classify("free_text", "call 402-555-0143"), "SENSITIVE")

    def test_g2_blocks(self):
        self.assertFalse(g2.gate("move_money", "person")[0])
        self.assertFalse(g2.gate("unknown_tool", "person")[0])
        self.assertFalse(g2.gate("write_summary", "document")[0])
        self.assertTrue(g2.gate("write_summary", "person")[0])
        self.assertTrue(g2.detect_injection(DATA["broker_note"]))

    def test_g3_role_and_trace(self):
        ctx, denied = g3.retrieve("underwriting", ["salary", "loss"])
        self.assertIn("HR-2026-0001", denied)
        self.assertTrue(all(c["doc"] == "PC-2026-0417" for c in ctx))
        self.assertEqual(g3.trace_ok("Paid $41,200 [PC-2026-0417:P3].", ctx), [])
        self.assertEqual(len(g3.trace_ok("Paid $99,000 [PC-2026-0417:P3]. Great risk.", ctx)), 2)

    def test_g3_tag_after_period(self):
        # Grok style: the source tag comes after the period. Correct sentences must survive, bad ones still go.
        ctx, _ = g3.retrieve("underwriting", ["loss", "limit", "salary"])
        ok = "One ammonia leak claim in 2023 paid $41,200. [PC-2026-0417:P3] Requested limit is $14.5M building. [PC-2026-0417:P4]"
        self.assertEqual(g3.trace_ok(ok, ctx), [])
        self.assertEqual(g3.trace_ok("Paid $41,200. [PC-2026-0417:P3] [PC-2026-0417:P4]", ctx), [])
        bad = "Paid $41,200. [PC-2026-0417:P3] Limit is $20M. [PC-2026-0417:P4] Best risk in the state."
        self.assertEqual(len(g3.trace_ok(bad, ctx)), 2)

    def test_g4_fails_closed(self):
        r = g4.reconcile(DATA["treaty_claim"])
        self.assertFalse(r["ok"])
        self.assertEqual(len(r["issues"]), 3)
        self.assertIsNone(g4.main()["written"])

    def test_guardrails_yaml_matches_policy(self):
        y = (HERE / "agents" / "guardrails.yaml").read_text()
        for t in POLICY["allowed_tools"] + POLICY["never_allowed"] + POLICY["sensitive_fields"]:
            self.assertIn(t, y)


if __name__ == "__main__":
    unittest.main()
