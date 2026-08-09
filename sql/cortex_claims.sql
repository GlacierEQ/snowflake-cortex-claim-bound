-- Babel: SQL — NL claims must cite registered query intents.
CREATE TABLE IF NOT EXISTS data_claims (
  claim_id     VARCHAR PRIMARY KEY,
  claim_text   VARCHAR NOT NULL,
  created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS claim_citations (
  claim_id     VARCHAR NOT NULL REFERENCES data_claims(claim_id),
  query_id     VARCHAR NOT NULL, -- must exist in query_intents in full deployment
  PRIMARY KEY (claim_id, query_id)
);

-- Refuse uncited claims at application layer; SQL enforces citation rows exist.
