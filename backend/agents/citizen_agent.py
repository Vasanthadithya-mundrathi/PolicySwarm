import asyncio
from pydantic import BaseModel
from core.llm import get_llm_response

class CitizenPersona(BaseModel):
    name: str
    role: str
    background: str
    traits: list[str]

class CitizenAgent:
    def __init__(self, persona: CitizenPersona):
        self.persona = persona
        self.name = persona.name
        self.role = persona.role

    async def react_to_policy(self, policy_text: str):
        prompt = f"""
        You are {self.name}, a {self.role}.
        Background: {self.persona.background}
        Traits: {', '.join(self.persona.traits)}

        Current Policy Proposal:
        "{policy_text}"

        React to this policy.
        1. Give a 'satisfaction_score' (0-100) based on how much this benefits YOU.
           - 0 = Hate it, 100 = Love it.
        2. Write a short 'message' (under 30 words) expressing your opinion.

        Return JSON format:
        {{
            "satisfaction_score": 85,
            "message": "I love this because..."
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        
        return {
            "agent": self.name,
            "role": self.role,
            "message": response.get("message", "No comment."),
            "score": response.get("satisfaction_score", 50)
        }
    
    async def reply_to_conversation(self, policy_text: str, recent_messages: list, exchange_count: int):
        """Generate a contextual reply in an ongoing conversation"""
        recent_context = "\n".join([f"{m['agent']}: {m['message']}" for m in recent_messages[-5:]])
        
        prompt = f"""
        You are {self.name}, a {self.role}.
        Background: {self.persona.background}
        Traits: {', '.join(self.persona.traits)}

        Policy being discussed: "{policy_text}"

        Recent conversation:
        {recent_context}

        This is exchange #{exchange_count} of 100.
        
        IMPORTANT: Respond naturally as {self.name}:
        - Reference specific points made by others (e.g., "I hear what Tom is saying, but...")
        - Stay true to your character and concerns
        - Keep it under 40 words
        - If you've said enough (especially after 50+ exchanges) or have personal reasons to leave (e.g., Tom: "Need to check my fields"), include "should_exit": true and give a natural exit reason
        
        Return JSON:
        {{
            "message": "Your response here",
            "should_exit": false,
            "exit_reason": "" 
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        
        return {
            "agent": self.name,
            "role": self.role,
            "message": response.get("message", "..."),
            "should_exit": response.get("should_exit", False),
            "exit_reason": response.get("exit_reason", "")
        }
