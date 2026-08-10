-- Babel: SQL — NL claims must cite registered query intents.
-- This fixture enforces non-empty claim/citation identities and local uniqueness.
-- A full deployment must add a foreign key or equivalent verified binding from
-- claim_citations.query_id to the authoritative query-intent registry.
CREATE TABLE IF NOT EXISTS data_claims (
  claim_id     VARCHAR PRIMARY KEY,
  claim_text   VARCHAR NOT NULL,
  created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (TRIM(claim_id) <> ''),
  CHECK (TRIM(claim_text) <> '')
);

CREATE TABLE IF NOT EXISTS claim_citations (
  claim_id     VARCHAR NOT NULL REFERENCES data_claims(claim_id),
  query_id     VARCHAR NOT NULL,
  PRIMARY KEY (claim_id, query_id),
  CHECK (TRIM(query_id) <> '')
);

-- Application-layer CortexClaimBound refuses uncited/unknown query IDs and
-- binds exact claim identity + registry identity into the decision receipt.
-- SQL alone does not prove query-result semantic support for the claim.
