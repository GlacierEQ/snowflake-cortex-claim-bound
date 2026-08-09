from __future__ import annotations
import unittest
from pathlib import Path
SQL = Path(__file__).resolve().parents[1] / "sql" / "cortex_claims.sql"
class T(unittest.TestCase):
    def test_citations(self):
        t = SQL.read_text()
        self.assertIn("data_claims", t)
        self.assertIn("claim_citations", t)
if __name__ == "__main__":
    unittest.main()
