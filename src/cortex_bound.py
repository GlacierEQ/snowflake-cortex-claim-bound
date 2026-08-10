"""Cortex claim bound — natural-language claims must cite registered query IDs.

This is a claim-evidence fence. It does not prove that a query result supports
the semantics of the claim; it proves only that the exact claim is explicitly
bound to a known query-ID registry under a deterministic citation contract.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Iterable


def digest(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@dataclass(frozen=True)
class DataClaim:
    text: str
    cited_query_ids: tuple[str, ...]


@dataclass(frozen=True)
class BoundResult:
    ok: bool
    reason: str | None
    claim_fingerprint: str
    registry_fingerprint: str
    fingerprint: str


class CortexClaimBound:
    def __init__(self, known_query_ids: Iterable[str]):
        known = tuple(sorted(known_query_ids))
        if any(not query_id.strip() for query_id in known):
            raise ValueError("known query IDs must be non-empty")
        if len(known) != len(set(known)):
            raise ValueError("known query IDs must be unique")
        self._known = frozenset(known)
        self.registry_fingerprint = digest({"known_query_ids": known})

    @staticmethod
    def _claim_fingerprint(claim: DataClaim) -> str:
        return digest(
            {
                "text": claim.text,
                "cited_query_ids": list(claim.cited_query_ids),
            }
        )

    def _result(
        self,
        claim: DataClaim,
        ok: bool,
        reason: str | None,
        citations: tuple[str, ...],
        unknown: tuple[str, ...] = (),
    ) -> BoundResult:
        claim_fingerprint = self._claim_fingerprint(claim)
        body = {
            "ok": ok,
            "reason": reason,
            "claim_fingerprint": claim_fingerprint,
            "registry_fingerprint": self.registry_fingerprint,
            "citations": list(citations),
            "unknown": list(unknown),
        }
        return BoundResult(
            ok=ok,
            reason=reason,
            claim_fingerprint=claim_fingerprint,
            registry_fingerprint=self.registry_fingerprint,
            fingerprint=digest(body),
        )

    def check(self, claim: DataClaim) -> BoundResult:
        if not claim.text.strip():
            return self._result(claim, False, "EMPTY_CLAIM", ())
        if not claim.cited_query_ids:
            return self._result(claim, False, "UNCITED", ())
        if any(not query_id.strip() for query_id in claim.cited_query_ids):
            return self._result(claim, False, "EMPTY_QUERY_ID", claim.cited_query_ids)
        if len(claim.cited_query_ids) != len(set(claim.cited_query_ids)):
            return self._result(claim, False, "DUPLICATE_CITATION", claim.cited_query_ids)

        citations = tuple(sorted(claim.cited_query_ids))
        unknown = tuple(query_id for query_id in citations if query_id not in self._known)
        if unknown:
            return self._result(claim, False, "UNKNOWN_QUERY", citations, unknown)
        return self._result(claim, True, None, citations)
