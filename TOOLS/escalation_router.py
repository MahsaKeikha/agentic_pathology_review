def route(flags: list[str]) -> dict:
    destination = "qualified_human" if flags else "routine_review"
    return {"destination": destination, "flags": flags}
