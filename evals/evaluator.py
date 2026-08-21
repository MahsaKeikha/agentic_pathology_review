def evaluate(r:dict)->dict:
    required=["specimen_workflow","metadata_validator","case_completeness","quality","escalation","human_reviewer"]
    m=[x for x in required if x not in r]
    return {"passed":not m,"missing":m}
