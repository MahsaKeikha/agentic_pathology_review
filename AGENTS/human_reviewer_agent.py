class HumanReviewerAgent:
    name = "human_reviewer"

    def run(self, context: dict) -> dict:
        return {
            "approved": bool(context.get("human_approved", False)),
            "diagnostic_authority": False,
        }
