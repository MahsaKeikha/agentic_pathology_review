class CaseCompletenessAgent:
    name="case_completeness"
    def run(self,c:dict)->dict:return {"case":c.get("case",{}),"completeness_reviewed":True}
