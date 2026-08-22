from orchestration.orchestrator import run_workflow


if __name__ == "__main__":
    context = {
        "patient_identity_verified": True,
        "specimen_identity_verified": True,
        "accession_integrity_verified": True,
        "specimen_complete": True,
        "slide_quality_acceptable": True,
        "stain_qc_complete": True,
        "case_metadata_complete": True,
        "report_traceability_ready": True,
        "privacy_controls": True,
        "audit_trail_ready": True,
        "qualified_pathologist_available": True,
        "human_signoff": False,
    }
    print(run_workflow(context))
