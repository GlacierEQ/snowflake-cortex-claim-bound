# ISSUE CONTRACT

## Pain
Natural-language answers can state metrics or conclusions without any durable binding to the queries they cite, and a citation ID alone does not prove which registry was accepted at verification time.

## Success
- Every non-empty claim requires one or more unique query-ID citations.
- Unknown, empty, duplicate, or absent citations refuse.
- The exact claim text + citation set has a deterministic fingerprint.
- The known-query registry has a deterministic fingerprint.
- Every allow/refuse result binds claim identity, registry identity, normalized citations, and refusal evidence.

## Boundary
This mechanism proves **citation registration**, not semantic entailment. A registered query citation does not by itself prove that the query result supports the natural-language claim. Query purpose/use policy belongs to the separate query-intent ledger; result-to-claim semantic verification is a future composition gate.
