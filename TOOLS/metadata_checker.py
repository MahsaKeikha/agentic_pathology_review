def check(metadata: dict, required: list[str]) -> dict:
    return {"missing": [field for field in required if not metadata.get(field)]}
