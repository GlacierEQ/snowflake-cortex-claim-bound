from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text())


CANONICAL = load("machine/canonical-position.json")
CAPABILITIES = load("machine/capabilities.json")
TARGET = load("machine/target-contract.json")
PROOF = load("machine/canonical-position-proof.json")


class CanonicalPositionContractTests(unittest.TestCase):
    def test_repository_owns_only_registered_query_claim_fence(self):
        self.assertEqual(CANONICAL["role"], "CANONICAL_SPECIALIST")
        self.assertEqual(CANONICAL["owns"], "registered_query_citation_claim_fence")
        self.assertIn("query purpose/downstream-use authorization", CANONICAL["does_not_own"])
        self.assertIn("semantic entailment between query result and natural-language claim", CANONICAL["does_not_own"])

    def test_query_intent_sibling_is_reference_only(self):
        edge = CANONICAL["relationships"][0]
        self.assertEqual(edge["repository"], "GlacierEQ/snowflake-query-intent-ledger")
        self.assertFalse(edge["integration_exercised"])

    def test_capabilities_are_repository_native(self):
        capabilities = set(CAPABILITIES["capabilities"])
        self.assertNotIn("hyper-scaling", capabilities)
        self.assertIn("exact_claim_identity_fingerprint", capabilities)
        self.assertIn("query_registry_fingerprint", capabilities)
        self.assertIn("claim_registry_bound_decision_receipt", capabilities)

    def test_target_reflects_earned_canonical_position(self):
        self.assertEqual(TARGET["current"]["state"], "EVOLVING")
        self.assertFalse(TARGET["current"]["canonical_position_pending_exact_head_proof"])
        self.assertEqual(TARGET["promotion"]["next_gate"], "EVOLUTION_CURSOR_DEFINED")
        self.assertEqual(PROOF["result"], "PASS")
        self.assertEqual(PROOF["tested_source_sha"], "b9174fcc5a19ae59287f3dfee66ffd449d799ffd")

    def test_truth_boundary_does_not_inflate_citation_into_semantics(self):
        boundary = CAPABILITIES["truth_boundary"]
        self.assertIn("does not execute queries", boundary)
        self.assertIn("prove semantic entailment", boundary)
        self.assertIn("authorize downstream query use", boundary)


if __name__ == "__main__":
    unittest.main()
