from __future__ import annotations
import unittest
from src.cortex_bound import CortexClaimBound, DataClaim

class CortexTests(unittest.TestCase):
    def test_uncited(self):
        b = CortexClaimBound({"q1"})
        r = b.check(DataClaim("revenue up", ()))
        self.assertFalse(r.ok)

    def test_ok(self):
        b = CortexClaimBound({"q1"})
        r = b.check(DataClaim("revenue up", ("q1",)))
        self.assertTrue(r.ok)

if __name__ == "__main__":
    unittest.main()
