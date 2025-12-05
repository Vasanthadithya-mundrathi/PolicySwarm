import asyncio
from pydantic import BaseModel
from core.llm import get_llm_response
import random

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
        # MEMORY SYSTEM
        self.conversation_memory = []  # Stores previous messages
        self.iteration_memory = []  # Stores previous policy iterations
        self.emotional_state = "neutral"  # neutral, frustrated, hopeful, confused, angry
        self.engagement_level = 100  # Decreases over time
        self.key_concerns = []  # Extracted from conversations
    
    def update_emotional_state(self, score):
        """Update emotional state based on satisfaction score"""
        if score < 20:
            self.emotional_state = random.choice(["angry", "frustrated"])
        elif score < 40:
            self.emotional_state = "frustrated"
        elif score < 60:
            self.emotional_state = random.choice(["confused", "neutral"])
        elif score < 80:
            self.emotional_state = "hopeful"
        else:
            self.emotional_state = "excited"
    
    def get_human_quirks(self):
        """Get human-like speech quirks based on persona"""
        quirks = {
            "Sarah": ["...", "honestly", "look", "I mean", "for god's sake"],
            "Jamal": ["bro", "like", "ngl", "lowkey", "fr"],
            "Richard": ["frankly", "bottom line", "strategically", "in my experience"],
            "Elsie": ["well dear", "in my day", "I remember when", "bless"],
            "Chloe": ["literally", "like", "actually", "okay but", "bruh"],
            "Dave": ["mate", "right", "at the end of the day", "innit"],
            "Priya": ["technically", "logically", "to be fair", "objectively"],
            "Gavin": ["look here", "working class", "unions", "factory floor"],
            "Maria": ["from a healthcare perspective", "patients", "NHS", "exhausted"],
            "Tom": ["out in the fields", "rural folk", "farming", "livestock"]
        }
        return quirks.get(self.name, ["..."])
    
    def add_to_iteration_memory(self, policy_text: str, iteration: int):
        """Store previous policy for context"""
        self.iteration_memory.append({
            "iteration": iteration,
            "policy": policy_text[:500]  # Store summary
        })
    
    async def react_to_policy(self, policy_text: str, iteration: int = 1):
        # Build context from previous iterations
        prev_context = ""
        if self.iteration_memory:
            prev_context = f"""
            PREVIOUS POLICY VERSIONS YOU'VE SEEN:
            {chr(10).join([f"Iteration {m['iteration']}: {m['policy'][:200]}..." for m in self.iteration_memory[-2:]])}
            
            YOU REMEMBER your previous concerns. Has this new version addressed them?
            """
        
        quirks = self.get_human_quirks()
        quirk_instruction = f"Occasionally use phrases like: {', '.join(quirks[:3])}"
        
        prompt = f"""
        You are {self.name}, a {self.role}.
        Background: {self.persona.background}
        Traits: {', '.join(self.persona.traits)}
        
        Your current emotional state: {self.emotional_state}
        
        {prev_context}
        
        CURRENT POLICY PROPOSAL (Iteration {iteration}):
        "{policy_text}"

        React to this policy AS A REAL HUMAN WOULD:
        1. Give a 'satisfaction_score' (0-100) based on how much this benefits YOU personally
        2. Write a 'message' (under 50 words) expressing your genuine opinion
        3. Include human touches: {quirk_instruction}
        4. If this is iteration 2+, reference whether your previous concerns were addressed
        5. Express your emotional_state: {self.emotional_state}
        
        Be REALISTIC - include:
        - Personal anecdotes from your background
        - Real concerns from your daily life
        - Occasional typos or informal speech if it fits your character
        - Uncertainty where appropriate ("I'm not sure if...")

        Return JSON format:
        {{
            "satisfaction_score": 45,
            "message": "Your genuine human response here",
            "key_concern": "One main worry in 5 words",
            "emotional_reaction": "angry/frustrated/neutral/hopeful/excited"
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        
        score = response.get("satisfaction_score", 50)
        self.update_emotional_state(score)
        
        # Store key concern
        if response.get("key_concern"):
            self.key_concerns.append(response.get("key_concern"))
        
        return {
            "agent": self.name,
            "role": self.role,
            "message": response.get("message", "No comment."),
            "score": score,
            "emotional_state": response.get("emotional_reaction", self.emotional_state)
        }
    
    async def reply_to_conversation(self, policy_text: str, recent_messages: list, exchange_count: int, iteration: int = 1):
        """Generate a contextual reply in an ongoing conversation with memory"""
        recent_context = "\n".join([f"{m['agent']}: {m['message']}" for m in recent_messages[-5:]])
        
        # Build iteration context
        prev_context = ""
        if self.iteration_memory and iteration > 1:
            prev_context = f"""
            You've seen previous versions of this policy. In iteration {iteration-1}, your main concern was: 
            {self.key_concerns[-1] if self.key_concerns else 'general doubts'}
            
            Has the new policy addressed this? Reference this in your response if relevant.
            """
        
        quirks = self.get_human_quirks()
        
        # Decrease engagement over time (more likely to exit)
        self.engagement_level = max(20, self.engagement_level - random.randint(1, 3))
        exit_likelihood = "high" if self.engagement_level < 40 else "medium" if self.engagement_level < 70 else "low"
        
        prompt = f"""
        You are {self.name}, a {self.role}.
        Background: {self.persona.background}
        Traits: {', '.join(self.persona.traits)}
        Current emotional state: {self.emotional_state}
        Energy level: {self.engagement_level}% (exit likelihood: {exit_likelihood})
        
        {prev_context}

        Policy being discussed: "{policy_text[:300]}..."

        Recent conversation:
        {recent_context}

        This is exchange #{exchange_count}.
        
        IMPORTANT - Respond as a REAL HUMAN would:
        1. Reference specific points made by others (e.g., "I hear what Tom is saying, but...")
        2. Stay true to your character, background, and current emotional state
        3. Use phrases natural to you: {', '.join(quirks[:2])}
        4. Show fatigue if engagement is low
        5. Include human imperfections: slight tangents, interruptions, personal stories
        6. Keep it under 50 words
        
        Natural exit criteria (if energy is low OR you've made your point):
        - {self.name}-specific exit: work, family, personal reasons
        - Express satisfaction/frustration with how discussion went
        
        Return JSON:
        {{
            "message": "Your natural human response",
            "should_exit": false,
            "exit_reason": "",
            "references_other": "name of person you're responding to or empty",
            "introduces_new_point": false
        }}
        """
        from core.llm import get_json_response
        response = await asyncio.to_thread(get_json_response, prompt)
        
        # Store in conversation memory
        self.conversation_memory.append({
            "exchange": exchange_count,
            "message": response.get("message", "...")
        })
        
        return {
            "agent": self.name,
            "role": self.role,
            "message": response.get("message", "..."),
            "should_exit": response.get("should_exit", False),
            "exit_reason": response.get("exit_reason", ""),
            "emotional_state": self.emotional_state
        }
    
    def reset_for_new_iteration(self, previous_policy: str, iteration: int):
        """Reset agent state for a new iteration while preserving memory"""
        self.add_to_iteration_memory(previous_policy, iteration - 1)
        self.engagement_level = 100  # Fresh energy for new iteration
        self.conversation_memory = []  # Clear conversation (new topic)
        # emotional_state and key_concerns preserved
