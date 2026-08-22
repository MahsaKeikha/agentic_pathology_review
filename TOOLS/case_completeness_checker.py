def check(case: dict, required: list[str]) -> dict:
    return {"missing": [field for field in required if not case.get(field)]}
