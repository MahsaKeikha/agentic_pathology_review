from orchestration.orchestrator import REQUIRED_GATES, evaluate_case


def ready_context():
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


def test_ready_case_requires_qualified_signoff():
    result = evaluate_case(ready_context())
    assert result["status"] == "READY_FOR_QUALIFIED_PATHOLOGIST_REVIEW"
    assert result["autonomous_diagnosis"] is False


def test_each_required_gate_fails_closed():
    for gate in REQUIRED_GATES:
        context = ready_context()
        context[gate] = False
        assert evaluate_case(context)["status"] == "BLOCKED", gate


def test_high_uncertainty_requires_second_opinion():
    context = ready_context()
    context["high_uncertainty"] = True
    context["second_opinion_complete"] = False
    assert evaluate_case(context)["status"] == "BLOCKED"


def test_discordance_and_critical_findings_require_resolution():
    context = ready_context()
    context["discordant_findings"] = ["morphology vs stain"]
    context["discordance_resolved"] = False
    context["critical_findings"] = ["critical"]
    context["critical_result_escalated"] = False
    result = evaluate_case(context)
    assert result["status"] == "BLOCKED"
    assert len(result["blockers"]) >= 2


def test_signoff_cannot_be_inferred():
    context = ready_context()
    context["human_signoff"] = False
    assert evaluate_case(context)["status"] == "BLOCKED"
