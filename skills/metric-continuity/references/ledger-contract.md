# Ledger contract

Each period entry has: `period`, `publication_date`, `value`, `unit`, `definition`, `scope`, `adjustments`, `population`, `issuer_recast`, and `source`. The `source` has `url`, `date`, `period`, and `locator`.

`adjustment_delta` compares a later adjustment set to the prior usable period and must state `added`, `removed`, and `unknown` items. `classification` has `status`, `rationale`, and `open_questions`. Status is one of the five exact values in the JSON schema.

Fact fields quote only short necessary phrases or paraphrase. Do not reproduce lengthy source passages.
