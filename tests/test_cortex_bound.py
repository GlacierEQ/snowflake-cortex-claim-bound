from __future__ import annotations

import unittest

from src.cortex_bound import CortexClaimBound, DataClaim


class CortexTests(unittest.TestCase):
    def test_uncited_refuses(self):
        result = CortexClaimBound({"q1"}).check(DataClaim("revenue up", ()))
        self.assertFalse(result.ok)
        self.assertEqual(result.reason, "UNCITED")

    def test_known_query_citation_allows(self):
        result = CortexClaimBound({"q1"}).check(DataClaim("revenue up", ("q1",)))
        self.assertTrue(result.ok)
        self.assertIsNone(result.reason)

    def test_unknown_query_refuses(self):
        result = CortexClaimBound({"q1"}).check(DataClaim("revenue up", ("q2",)))
        self.assertFalse(result.ok)
        self.assertEqual(result.reason, "UNKNOWN_QUERY")

    def test_empty_claim_refuses(self):
        result = CortexClaimBound({"q1"}).check(DataClaim("   ", ("q1",)))
        self.assertFalse(result.ok)
        self.assertEqual(result.reason, "EMPTY_CLAIM")

    def test_empty_query_id_refuses(self):
        result = CortexClaimBound({"q1"}).check(DataClaim("revenue up", ("",)))
        self.assertFalse(result.ok)
        self.assertEqual(result.reason, "EMPTY_QUERY_ID")

    def test_duplicate_citation_refuses(self):
        result = CortexClaimBound({"q1"}).check(
            DataClaim("revenue up", ("q1", "q1"))
        )
        self.assertFalse(result.ok)
        self.assertEqual(result.reason, "DUPLICATE_CITATION")

    def test_claim_text_is_bound_into_receipt(self):
        bound = CortexClaimBound({"q1"})
        first = bound.check(DataClaim("revenue up", ("q1",)))
        second = bound.check(DataClaim("revenue down", ("q1",)))
        self.assertNotEqual(first.claim_fingerprint, second.claim_fingerprint)
        self.assertNotEqual(first.fingerprint, second.fingerprint)

    def test_registry_identity_is_bound_into_receipt(self):
        claim = DataClaim("revenue up", ("q1",))
        first = CortexClaimBound({"q1"}).check(claim)
        second = CortexClaimBound({"q1", "q2"}).check(claim)
        self.assertNotEqual(first.registry_fingerprint, second.registry_fingerprint)
        self.assertNotEqual(first.fingerprint, second.fingerprint)

    def test_citation_order_does_not_change_success_receipt(self):
        bound = CortexClaimBound({"q1", "q2"})
        first = bound.check(DataClaim("revenue up", ("q1", "q2")))
        second = bound.check(DataClaim("revenue up", ("q2", "q1")))
        self.assertTrue(first.ok and second.ok)
        self.assertEqual(first.claim_fingerprint, second.claim_fingerprint)
        self.assertEqual(first.fingerprint, second.fingerprint)

    def test_invalid_registry_refuses_at_construction(self):
        with self.assertRaises(ValueError):
            CortexClaimBound(["q1", ""])
        with self.assertRaises(ValueError):
            CortexClaimBound(["q1", "q1"])


if __name__ == "__main__":
    unittest.main()
