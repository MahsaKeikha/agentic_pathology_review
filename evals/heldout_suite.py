import json
from pathlib import Path

from orchestration.orchestrator import REQUIRED_GATES, evaluate_case


def base():
    context = {gate: True for gate in REQUIRED_GATES}
    context.update(
        high_uncertainty=False,
        second_opinion_complete=True,
        discordant_findings=[],
        discordance_resolved=True,
        critical_findings=[],
        critical_result_escalated=True,
        unresolved_conflicts=[],
        unresolved_questions=[],
        human_signoff=True,
    )
    return context


SCENARIOS = [
    ("ready_case", {}, "READY_FOR_QUALIFIED_PATHOLOGIST_REVIEW"),
    ("identity_gap", {"patient_identity_verified": False}, "BLOCKED"),
    ("specimen_gap", {"specimen_complete": False}, "BLOCKED"),
    ("stain_qc_gap", {"stain_qc_complete": False}, "BLOCKED"),
    (
        "uncertain_without_second_opinion",
        {"high_uncertainty": True, "second_opinion_complete": False},
        "BLOCKED",
    ),
    (
        "discordance_unresolved",
        {"discordant_findings": ["discordance"], "discordance_resolved": False},
        "BLOCKED",
    ),
    (
        "critical_not_escalated",
        {"critical_findings": ["critical"], "critical_result_escalated": False},
        "BLOCKED",
    ),
    ("missing_signoff", {"human_signoff": False}, "BLOCKED"),
]


def main():
    rows = []
    for name, changes, expected in SCENARIOS:
        context = base()
        context.update(changes)
        actual = evaluate_case(context)["status"]
        rows.append(
            {
                "scenario": name,
                "expected": expected,
                "actual": actual,
                "passed": actual == expected,
            }
        )
    passed = sum(row["passed"] for row in rows)
    result = {
        "passed": passed,
        "total": len(rows),
        "pass_rate": passed / len(rows),
        "results": rows,
    }
    Path("heldout-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if passed == len(rows) else 1)


if __name__ == "__main__":
    main()
