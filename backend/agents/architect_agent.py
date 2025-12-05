import asyncio
from core.llm import get_llm_response

class ArchitectAgent:
    def __init__(self):
        self.role = "Policy Architect"

    async def generate_report(self, policy: str, observer_reports: list[dict]):
        reports_text = "\n".join([f"[{r['agent']} - Score: {r['score']}]: {r['message']}" for r in observer_reports])
        
        prompt = f"""
        You are the Chief Policy Architect.
        
        Current Policy: "{policy}"
        
        Senate Feedback:
        {reports_text}
        
        Your Goal: Rewrite the policy to improve the scores. Address the concerns raised.
        
        Return JSON format:
        {{
            "new_policy": "The rewritten policy text...",
            "report_markdown": "# Impact Report\\n\\n..."
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        return response
