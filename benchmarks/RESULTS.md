# F57 Held-Out Reproducibility Results

Gold Standard validation was executed from a clean GitHub Actions checkout.

- Evidence run: `32558738074`
- Head: `4ae2028edc699ab003eb42fa9de22441aa38dc63`
- Python: 3.10, 3.11, 3.12 all green
- Held-out pathology review scenarios: 8/8 passed
- Pass rate: 1.0
- Artifact: `f57-heldout-results`
- Artifact digest: `sha256:4f18a45936f51bf5a6307360de03e806dc8eb5db06e11461e95092a6aeed0f75`

The suite validates fail-closed handling for identity gaps, incomplete specimens, stain-QC failures, unresolved diagnostic uncertainty, unresolved discordance, critical-result escalation, and missing qualified pathologist sign-off. L3 does not represent autonomous diagnosis or replacement of qualified pathology judgment.
