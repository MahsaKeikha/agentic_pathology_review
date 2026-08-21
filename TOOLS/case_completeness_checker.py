def check(case:dict,required:list[str])->dict:return {"missing":[x for x in required if not case.get(x)]}
