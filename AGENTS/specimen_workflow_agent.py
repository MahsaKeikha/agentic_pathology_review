class SpecimenWorkflowAgent:
    name="specimen_workflow"
    def run(self,c:dict)->dict:return {"specimens":c.get("specimens",[]),"tracked":True}
