"""Cortex claim bound — NL claims must cite registered query intents."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


def digest(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class DataClaim:
    text: str
    cited_query_ids: tuple[str, ...]


@dataclass(frozen=True)
class BoundResult:
    ok: bool
    reason: str | None
    fingerprint: str


class CortexClaimBound:
    def __init__(self, known_query_ids: set[str]):
        self.known = set(known_query_ids)

    def check(self, claim: DataClaim) -> BoundResult:
        if not claim.cited_query_ids:
            body = {"ok": False, "r": "UNCITED"}
            return BoundResult(False, "UNCITED", digest(body))
        unknown = [q for q in claim.cited_query_ids if q not in self.known]
        if unknown:
            body = {"ok": False, "r": "UNKNOWN_QUERY", "u": unknown}
            return BoundResult(False, "UNKNOWN_QUERY", digest(body))
        body = {"ok": True, "cites": list(claim.cited_query_ids)}
        return BoundResult(True, None, digest(body))
