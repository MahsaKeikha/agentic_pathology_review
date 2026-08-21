class EscalationAgent:
    name="escalation"
    def run(self,c:dict)->dict:return {"flags":c.get("flags",[]),"escalate":bool(c.get("flags"))}
