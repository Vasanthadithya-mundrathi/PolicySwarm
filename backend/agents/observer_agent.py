import asyncio
from core.llm import get_llm_response
import random

class ObserverAgent:
    def __init__(self, role: str, focus: str):
        self.role = role
        self.focus = focus
        # MEMORY SYSTEM for Senate
        self.conversation_memory = []
        self.iteration_memory = []
        self.stance = "neutral"  # supportive, critical, neutral, cautious
        self.key_insights = []
        self.engagement_level = 100
    
    def get_senate_personality(self):
        """Get personality traits for each Senate member"""
        personalities = {
            "Trend Watcher": {
                "style": "data-driven, references polls and social media trends",
                "quirks": ["the data suggests", "public sentiment shows", "trending concern"],
                "bias": "leans toward popular opinion"
            },
            "Strategy Lead": {
                "style": "pragmatic, focuses on implementation feasibility and costs",
                "quirks": ["bottom line", "operationally speaking", "budget implications"],
                "bias": "leans toward government capacity"
            },
            "Ethics Guardian": {
                "style": "principled, references human rights and fairness",
                "quirks": ["fundamentally", "morally speaking", "constitutional concern"],
                "bias": "leans toward citizen protection"
            }
        }
        return personalities.get(self.role, {"style": "analytical", "quirks": [], "bias": "neutral"})
    
    def add_to_iteration_memory(self, policy: str, citizen_feedback_summary: str, iteration: int):
        """Store previous iteration analysis"""
        self.iteration_memory.append({
            "iteration": iteration,
            "policy_summary": policy[:300],
            "citizen_concerns": citizen_feedback_summary[:200]
        })
    
    async def analyze_debate(self, policy: str, debate_logs: list[dict], iteration: int = 1):
        """Initial analysis of citizen debate"""
        debate_text = "\n".join([f"{log['agent']} ({log['role']}): {log['message']} (Score: {log.get('score', 'N/A')})" for log in debate_logs[:20]])
        
        personality = self.get_senate_personality()
        
        # Build iteration context
        prev_context = ""
        if self.iteration_memory:
            prev_context = f"""
            PREVIOUS ITERATION ANALYSIS:
            In iteration {self.iteration_memory[-1]['iteration']}, citizens were concerned about: {self.iteration_memory[-1]['citizen_concerns']}
            Your previous insight was: {self.key_insights[-1] if self.key_insights else 'general concerns'}
            
            Has the new policy addressed these? Evaluate progress.
            """
        
        prompt = f"""
        You are the {self.role}, a Senate observer. Your focus is {self.focus}.
        Your analytical style: {personality['style']}
        Your natural bias: {personality['bias']}
        
        {prev_context}
        
        POLICY (Iteration {iteration}): "{policy[:500]}"
        
        CITIZEN FEEDBACK:
        {debate_text}
        
        Analyze this as a government advisor:
        1. Give a 'viability_score' (0-100) based on your focus area:
           - {self.focus} perspective
           - Implementation feasibility
           - Political risk assessment
        2. Write a 'message' (under 60 words) summarizing key findings
        3. Use your style: {', '.join(personality['quirks'][:2])}
        4. Identify the biggest implementation risk
        
        Be realistic - governments need:
        - Political feasibility (will it pass?)
        - Economic viability (can we afford it?)
        - Public acceptance (will there be backlash?)

        Return JSON format:
        {{
            "viability_score": 60,
            "message": "Your analysis here...",
            "key_risk": "Main implementation risk",
            "recommendation": "approve/modify/reject"
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        
        # Store insight
        if response.get("key_risk"):
            self.key_insights.append(response.get("key_risk"))
        
        # Update stance
        score = response.get("viability_score", 50)
        if score > 70:
            self.stance = "supportive"
        elif score < 40:
            self.stance = "critical"
        else:
            self.stance = "cautious"
        
        return {
            "agent": self.role,
            "focus": self.focus,
            "message": response.get("message", "Analysis pending."),
            "score": score,
            "recommendation": response.get("recommendation", "modify"),
            "stance": self.stance
        }
    
    async def reply_to_senate_debate(self, policy: str, citizen_conversation: str, recent_senate_messages: list, exchange_count: int, iteration: int = 1):
        """Generate a contextual reply in the Senate strategic debate"""
        recent_context = "\n".join([f"{m['agent']}: {m['message']}" for m in recent_senate_messages[-4:]])
        
        personality = self.get_senate_personality()
        
        # Decrease engagement
        self.engagement_level = max(30, self.engagement_level - random.randint(2, 5))
        
        prompt = f"""
        You are the {self.role}, focusing on {self.focus}.
        Your style: {personality['style']}
        Your current stance: {self.stance}
        
        ITERATION {iteration}
        
        Policy being evaluated: "{policy[:400]}"
        
        Summary of citizen concerns:
        {citizen_conversation[:600]}
        
        Recent Senate discussion:
        {recent_context}
        
        Exchange #{exchange_count} of 10.
        
        RESPOND AS A REAL GOVERNMENT ADVISOR:
        1. Reference points made by colleagues (Trend Watcher, Strategy Lead, Ethics Guardian)
        2. Bring your {self.focus} expertise
        3. Use your phrases: {', '.join(personality['quirks'][:2])}
        4. Show agreement OR respectful disagreement with other senators
        5. Consider: Can this actually be implemented? What are the risks?
        6. Keep it under 50 words
        7. Be professional but show personality
        
        If exchange is 8+, start moving toward consensus or clear disagreement.
        
        Return JSON:
        {{
            "message": "Your strategic response",
            "agrees_with": "name of senator you agree with or empty",
            "disagrees_with": "name of senator you disagree with or empty",
            "new_insight": "any new point you're raising"
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        
        self.conversation_memory.append({
            "exchange": exchange_count,
            "message": response.get("message", "...")
        })
        
        return {
            "agent": self.role,
            "focus": self.focus,
            "message": response.get("message", "..."),
            "stance": self.stance
        }
    
    async def final_verdict(self, policy: str, senate_discussion: list, citizen_score: float, iteration: int = 1):
        """Give final verdict after Senate discussion"""
        discussion_summary = "\n".join([f"{m['agent']}: {m['message']}" for m in senate_discussion[-5:]])
        
        prompt = f"""
        You are the {self.role}. The Senate discussion is concluding.
        
        ITERATION {iteration}
        Policy: "{policy[:400]}"
        
        Citizen Satisfaction Score: {citizen_score}%
        
        Senate Discussion Summary:
        {discussion_summary}
        
        Provide your FINAL VERDICT:
        1. Final viability_score (0-100) for your focus area
        2. A concise final_message (under 40 words)
        3. Your recommendation: approve / modify / reject
        4. Key condition for approval (if any)
        
        Return JSON:
        {{
            "viability_score": 65,
            "final_message": "Your final assessment",
            "recommendation": "modify",
            "condition": "Only if X is addressed"
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        
        return {
            "agent": self.role,
            "focus": self.focus,
            "message": f"[FINAL VERDICT] {response.get('final_message', 'Assessment complete.')}",
            "score": response.get("viability_score", 50),
            "recommendation": response.get("recommendation", "modify"),
            "condition": response.get("condition", "None")
        }
    
    def reset_for_new_iteration(self, policy: str, citizen_summary: str, iteration: int):
        """Reset for new iteration while preserving memory"""
        self.add_to_iteration_memory(policy, citizen_summary, iteration - 1)
        self.engagement_level = 100
        self.conversation_memory = []
        # stance and key_insights preserved
