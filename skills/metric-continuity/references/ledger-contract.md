# Ledger contract

Each classified ledger has `issuer`, `metric`, `material_authorization`, `source_coverage`, at least two period entries, a non-empty `adjustment_delta`, a `classification`, and at least two source-index entries. Each period entry has a non-empty `period`, a real calendar `publication_date`, non-empty `value`, `unit`, `definition`, `scope`, `adjustments`, `population`, `issuer_recast`, and `source`. `adjustments` is an array of strings. The `source` has non-empty `url`, real calendar `date`, non-empty `period`, and non-empty `locator`.

`adjustment_delta` compares a later adjustment set to the prior usable period. Every entry has `from_period`, `to_period`, and `added`, `removed`, and `unknown` arrays of strings. `classification` has `status`, `rationale`, and `open_questions`. Status is one of the five exact values in the JSON schema. `Research incomplete` is a stop response, not a classified ledger and therefore does not validate against this schema.

Fact fields quote only short necessary phrases or paraphrase. Do not reproduce lengthy source passages.
