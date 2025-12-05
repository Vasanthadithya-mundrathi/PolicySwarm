import asyncio
from core.llm import get_llm_response

class ObserverAgent:
    def __init__(self, role: str, focus: str):
        self.role = role
        self.focus = focus # e.g., "Economic Impact", "Social Sentiment"

    async def analyze_debate(self, policy: str, debate_logs: list[dict]):
        debate_text = "\n".join([f"{log['agent']} ({log['role']}): {log['message']} (Score: {log.get('score', 0)})" for log in debate_logs])
        
        prompt = f"""
        You are the {self.role}. Your focus is {self.focus}.
        
        Policy: "{policy}"
        
        Citizen Feedback:
        {debate_text}
        
        Analyze this.
        1. Give a 'viability_score' (0-100) based on your focus (Economic/Social/Ethical stability).
        2. Write a short 'message' (bullet point style) summarizing the key issue.

        Return JSON format:
        {{
            "viability_score": 60,
            "message": "Economic risk is high because..."
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        
        return {
            "agent": self.role,
            "focus": self.focus,
            "message": response.get("message", "Analysis failed."),
            "score": response.get("viability_score", 50)
        }
    
    async def reply_to_senate_debate(self, policy: str, citizen_conversation: str, recent_senate_messages: list, exchange_count: int):
        """Generate a contextual reply in the Senate strategic debate"""
        recent_context = "\n".join([f"{m['agent']}: {m['message']}" for m in recent_senate_messages[-3:]])
        
        prompt = f"""
        You are the {self.role}, focusing on {self.focus}.
        
        Policy being evaluated: "{policy}"
        
        The citizens have debated this policy extensively. Here's a summary of their concerns:
        {citizen_conversation[:1000]}... [conversation continues]
        
        Recent Senate discussion:
        {recent_context}
        
        This is Senate exchange #{exchange_count} of 10.
        
        IMPORTANT: Respond as a government/corporate strategist:
        - Discuss viability from YOUR perspective ({self.focus})
        - Reference points made by other senators (Trend Watcher, Strategy Lead, Ethics Guardian)
        - Consider: Can this policy be implemented? What are the risks?
        - Keep it under 50 words
        - Stay professional and strategic
        
        Return JSON:
        {{
            "message": "Your strategic analysis here"
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        
        return {
            "agent": self.role,
            "focus": self.focus,
            "message": response.get("message", "...")
        }

