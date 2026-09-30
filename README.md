# Metric Continuity

Audit whether a public-company non-GAAP measure or operating KPI remains comparable across reporting periods. It produces a source-linked ledger and fails closed when the issuer's basis is unresolved. It does not provide investment, legal, or accounting advice.

```bash
npx skills add g-denn/metric-continuity --skill metric-continuity
```

## Five-minute synthetic example

Give the skill two dated issuer disclosures and ask: “Compare Example Systems' adjusted service margin for FY2024 and FY2025.” The included [synthetic ledger](examples/happy-path.json) finds the same definition, scope, adjustment, unit, and population, then returns `comparable`. Validate it locally:

```bash
python scripts/validate.py examples/happy-path.json
```

If a disclosure changes the metric definition or leaves the basis unclear, the result is `directional_only`, `not_comparable`, or `unknown`—not a made-up normalization.

## What it does

- Compares definition, scope, adjustment set, unit, population, and issuer-disclosed recasts across two or more dated periods.
- Separates issuer facts, calculations, interpretation, and unknowns.
- Returns an evidence ledger with source URLs, dates, periods, and locators.

## What it does not do

It is not broad diligence, valuation, a trading tool, spreadsheet formula audit, private-data-room processor, compliance opinion, or an agent-created recast engine. See the skill instructions for the full boundary.

## Development

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

All examples are synthetic. No service, credentials, or third-party dependency is required.
