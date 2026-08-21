class QualityAgent:
    name="quality"
    def run(self,c:dict)->dict:return {"quality":c.get("quality",{}),"reviewed":True}
