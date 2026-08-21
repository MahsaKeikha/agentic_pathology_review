from AGENTS.specimen_workflow_agent import SpecimenWorkflowAgent
from AGENTS.metadata_validator_agent import MetadataValidatorAgent
from AGENTS.case_completeness_agent import CaseCompletenessAgent
from AGENTS.quality_agent import QualityAgent
from AGENTS.escalation_agent import EscalationAgent
from AGENTS.human_reviewer_agent import HumanReviewerAgent

def run_workflow(c:dict)->dict:
    agents=[SpecimenWorkflowAgent(),MetadataValidatorAgent(),CaseCompletenessAgent(),QualityAgent(),EscalationAgent(),HumanReviewerAgent()]
    return {a.name:a.run(c) for a in agents}
