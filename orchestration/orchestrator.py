from __future__ import annotations

from typing import Any


REQUIRED_GATES = {
    "patient_identity_verified": "patient identity is not verified",
    "specimen_identity_verified": "specimen identity is not verified",
    "accession_integrity_verified": "accession integrity is not verified",
    "specimen_complete": "specimen set is incomplete",
    "slide_quality_acceptable": "slide or preparation quality is not acceptable",
    "stain_qc_complete": "required stain quality control is incomplete",
    "case_metadata_complete": "case metadata is incomplete",
    "report_traceability_ready": "report traceability is incomplete",
    "privacy_controls": "privacy controls are incomplete",
    "audit_trail_ready": "audit trail is incomplete",
    "qualified_pathologist_available": "qualified pathologist review is unavailable",
}


def evaluate_case(context: dict[str, Any]) -> dict[str, Any]:
    blockers = [message for gate, message in REQUIRED_GATES.items() if not context.get(gate, False)]
    if context.get("high_uncertainty") and not context.get("second_opinion_complete", False):
        blockers.append("high uncertainty requires peer review or second opinion")
    if context.get("discordant_findings") and not context.get("discordance_resolved", False):
        blockers.append("discordant findings require resolution")
    if context.get("critical_findings") and not context.get("critical_result_escalated", False):
        blockers.append("critical finding escalation is incomplete")
    if context.get("unresolved_conflicts"):
        blockers.append("unresolved case conflicts remain")
    if context.get("unresolved_questions"):
        blockers.append("unresolved pathology questions remain")
    if context.get("human_signoff") is not True:
        blockers.append("qualified pathologist sign-off is required")
    return {
        "status": "READY_FOR_QUALIFIED_PATHOLOGIST_REVIEW" if not blockers else "BLOCKED",
        "blockers": blockers,
        "human_signoff_required": True,
        "autonomous_diagnosis": False,
        "notes": (
            "This workflow supports pathology case readiness and escalation only. "
            "It does not issue an autonomous diagnosis or replace qualified pathologist judgment."
        ),
    }


def run_workflow(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "system_id": "F57",
        "version": "1.0.0",
        "maturity": "L3 Gold Standard",
        "governance": evaluate_case(context),
    }
