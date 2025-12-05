import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from agents.citizen_agent import CitizenAgent, CitizenPersona
from agents.observer_agent import ObserverAgent
from agents.architect_agent import ArchitectAgent

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
config = {
    "fast_demo": False,  # Toggle for fast demo mode
    "max_exchanges": 100,
    "max_senate_exchanges": 10
}

# State
logs = []
debate_history = []
observer_reports = []
final_report = ""
metrics = []
policy_document = None  # Store uploaded policy document

def log_event(agent_name: str, message: str, role: str = "System"):
    print(f"[{agent_name}] {message}")
    logs.append({"agent": agent_name, "role": role, "message": message})

# Initialize Agents
personas = [
    CitizenPersona(
        name="Sarah", role="Single Mom",
        background="34, Part-time nurse, 2 kids. Receives Universal Credit.",
        traits=["Struggling with cost of living", "Worried about childcare", "Skeptical of politicians", "Prioritizes NHS and stability"]
    ),
    CitizenPersona(
        name="Jamal", role="Gig Worker",
        background="26, Uber driver & Deliveroo rider. Renting in Zone 4.",
        traits=["Values flexibility but hates instability", "No sick pay", "Anxious about rent", "Tech-savvy but cynical"]
    ),
    CitizenPersona(
        name="Richard", role="CEO",
        background="52, CEO of a mid-sized logistics firm. Homeowner.",
        traits=["Concerned about interest rates", "Dislikes red tape", "Focused on growth & stability", "Pragmatic"]
    ),
    CitizenPersona(
        name="Elsie", role="Retiree",
        background="74, Retired teacher. Owns home outright. Relies on state pension.",
        traits=["Protective of Triple Lock pension", "NHS is #1 priority", "Resistant to radical change", "Votes consistently"]
    ),
    CitizenPersona(
        name="Chloe", role="Student",
        background="19, University student. High debt. Climate activist.",
        traits=["Idealistic", "Anxious about climate & housing", "Feels ignored by politics", "Socially liberal"]
    ),
    CitizenPersona(
        name="Dave", role="Small Business Owner",
        background="45, Runs a local bakery. Struggling with energy bills.",
        traits=["Hardworking", "Stressed about costs", "Community-focused", "Hates tax hikes"]
    ),
    CitizenPersona(
        name="Priya", role="Tech Lead",
        background="31, Software Engineer. High earner but priced out of housing market.",
        traits=["Ambitious", "Frustrated by housing crisis", "Pro-innovation", "Global outlook"]
    ),
    CitizenPersona(
        name="Gavin", role="Factory Worker",
        background="50, Auto plant worker. Union member. Worried about automation.",
        traits=["Values job security", "Loyal to community", "Skeptical of green policies if they cost jobs", "Traditional"]
    ),
    CitizenPersona(
        name="Maria", role="NHS Doctor",
        background="38, Junior Doctor. Overworked and underpaid.",
        traits=["Passionate about public service", "Burned out", "Critical of government management", "Empathetic"]
    ),
    CitizenPersona(
        name="Tom", role="Farmer",
        background="60, Sheep farmer. Struggling with post-Brexit subsidies.",
        traits=["Independent", "Worried about rural crime & costs", "Feels misunderstood by city folk", "Conservative"]
    )
]

citizens = [CitizenAgent(p) for p in personas]

observers = [
    ObserverAgent(role="Trend Watcher", focus="Social Sentiment & Future Trends"),
    ObserverAgent(role="Strategy Lead", focus="Economic Viability & Implementation"),
    ObserverAgent(role="Ethics Guardian", focus="Fairness & Human Rights")
]

architect = ArchitectAgent()

async def run_simulation(initial_policy: str):
    global final_report
    current_policy = initial_policy
    
    for iteration in range(1, 4): # Max 3 iterations
        log_event("System", f"--- Iteration {iteration}/3 ---")
        log_event("System", f"Current Policy: {current_policy}")
        
        # LEVEL 1: Citizen Conversation (The \"Chat\")
        log_event("System", "Phase 1: Citizen Swarm Debate (Level 1)")
        conversation_log = []
        
        # Initial reactions to policy
        tasks = [c.react_to_policy(current_policy) for c in citizens]
        reactions = await asyncio.gather(*tasks)
        
        citizen_scores = []
        conversation_messages = []  # Track all messages for context
        
        for r in reactions:
            log_event(r["agent"], f"{r['message']} (Score: {r['score']})", r["role"])
            conversation_log.append(f"{r['agent']} ({r['role']}): {r['message']}")
            conversation_messages.append({"agent": r["agent"], "role": r["role"], "message": r['message']})
            debate_history.append(r)
            citizen_scores.append(r['score'])
            await asyncio.sleep(0.1)
            
        # RICH CONVERSATIONAL DEBATE: Uses config for exchange count
        max_exchanges = config["max_exchanges"]
        log_event("System", f"Citizens are now engaging in deep conversation (up to {max_exchanges} exchanges)...")
        
        import random
        active_citizens = list(citizens)  # Track who's still in the conversation
        exchange_count = len(reactions)  # Start counting from initial reactions
        
        MAX_EXCHANGES = max_exchanges
        
        while exchange_count < MAX_EXCHANGES and len(active_citizens) > 2:
            # Pick a random active citizen to speak
            speaker = random.choice(active_citizens)
            
            # Generate contextual reply
            reply_data = await speaker.reply_to_conversation(
                current_policy, 
                conversation_messages, 
                exchange_count
            )
            
            # Log the message
            if reply_data["should_exit"]:
                exit_msg = f"{reply_data['message']} [{reply_data['exit_reason']}]"
                log_event(speaker.name, exit_msg, speaker.role)
                conversation_messages.append({"agent": speaker.name, "role": speaker.role, "message": exit_msg})
                debate_history.append({"agent": speaker.name, "role": speaker.role, "message": exit_msg})
                active_citizens.remove(speaker)
                log_event("System", f"{speaker.name} has left the conversation.")
            else:
                log_event(speaker.name, reply_data['message'], speaker.role)
                conversation_messages.append({"agent": speaker.name, "role": speaker.role, "message": reply_data['message']})
                debate_history.append({"agent": speaker.name, "role": speaker.role, "message": reply_data['message']})
            
            conversation_log.append(f"{speaker.name}: {reply_data['message']}")
            exchange_count += 1
            
            # Small delay to avoid overwhelming the LLM
            await asyncio.sleep(0.3)
        
        log_event("System", f"Conversation concluded after {exchange_count} exchanges.")

        avg_citizen_score = sum(citizen_scores) / len(citizen_scores) if citizen_scores else 0
        log_event("System", f"Average Citizen Satisfaction: {avg_citizen_score:.1f}%")

        # LEVEL 2: Senate Strategic Debate (10 exchanges)
        log_event("System", "Phase 2: Senate Strategic Debate (Level 2)")
        log_event("System", "Senate observers are analyzing the citizen conversation and debating viability...")
        
        # First, get initial analysis from each observer
        full_conversation_text = "\n".join(conversation_log)
        
        tasks = [o.analyze_debate(current_policy, [{"agent": "Conversation", "role": "Log", "message": full_conversation_text}]) for o in observers]
        initial_reports = await asyncio.gather(*tasks)
        
        senate_scores = []
        senate_messages = []  # Track Senate conversation
        
        # Log initial analysis
        for r in initial_reports:
            log_event(r["agent"], f"[Initial Analysis] {r['message']} (Score: {r['score']})", r["focus"])
            senate_messages.append({"agent": r["agent"], "role": r["focus"], "message": f"[Initial] {r['message']}"})
            debate_history.append({"agent": r["agent"], "role": r["focus"], "message": f"[Initial] {r['message']}", "score": r['score']})
            senate_scores.append(r['score'])
            await asyncio.sleep(0.3)
        
        # SENATE CONVERSATION: Uses config for exchange count
        max_senate_exchanges = config["max_senate_exchanges"]
        log_event("System", f"Senate is now engaging in strategic discussion ({max_senate_exchanges} exchanges)...")
        
        senate_exchange_count = 0
        MAX_SENATE_EXCHANGES = max_senate_exchanges
        
        while senate_exchange_count < MAX_SENATE_EXCHANGES:
            # Pick a random observer to speak
            import random
            speaker = random.choice(observers)
            
            # Generate strategic reply
            reply_data = await speaker.reply_to_senate_debate(
                current_policy,
                full_conversation_text,
                senate_messages,
                senate_exchange_count
            )
            
            # Log the message
            log_event(speaker.role, reply_data['message'], speaker.focus)
            senate_messages.append({"agent": speaker.role, "role": speaker.focus, "message": reply_data['message']})
            debate_history.append({"agent": speaker.role, "role": speaker.focus, "message": reply_data['message']})
            
            senate_exchange_count += 1
            await asyncio.sleep(0.4)
        
        log_event("System", f"Senate debate concluded after {senate_exchange_count} exchanges.")
        
        # Final Senate conclusion: re-score after discussion
        log_event("System", "Senate is finalizing viability scores after discussion...")
        tasks = [o.analyze_debate(current_policy, [{"agent": "Conversation", "role": "Log", "message": full_conversation_text}]) for o in observers]
        final_reports = await asyncio.gather(*tasks)
        
        observer_reports = final_reports  # Store for architect
        senate_scores = []  # Recalculate after debate
        
        for r in final_reports:
            log_event(r["agent"], f"[Final Score] {r['message']} (Score: {r['score']})", r["focus"])
            debate_history.append({"agent": r["agent"], "role": r["focus"], "message": f"[Final] {r['message']}", "score": r['score']})
            senate_scores.append(r['score'])
            await asyncio.sleep(0.3)

        avg_senate_score = sum(senate_scores) / len(senate_scores) if senate_scores else 0
        log_event("System", f"Average Senate Viability Score: {avg_senate_score:.1f}%")
        
        # Record Metrics
        metrics.append({
            "iteration": iteration,
            "citizen_score": round(avg_citizen_score, 1),
            "senate_score": round(avg_senate_score, 1)
        })
        
        # Check Thresholds
        if avg_citizen_score > 75 and avg_senate_score > 80:
            log_event("System", "✅ Consensus Reached! Policy Ratified.")
            # Final Level 3 Synthesis for the "Win" state
            synthesis = await architect.generate_report(current_policy, reports)
            final_report = synthesis.get("report_markdown", "Error generating report.")
            break
            
        if iteration < 3:
            log_event("System", "⚠️ Consensus Not Met. Level 3 Architect rewriting policy...")
            # LEVEL 3: Architect Synthesis (The "Rewrite")
            synthesis = await architect.generate_report(current_policy, reports)
            current_policy = synthesis.get("new_policy", current_policy)
            final_report = synthesis.get("report_markdown", "Error generating report.")
        else:
            log_event("System", "🛑 Max Iterations Reached. Finalizing best effort.")
            synthesis = await architect.generate_report(current_policy, reports)
            final_report = synthesis.get("report_markdown", "Error generating report.")

    log_event("Architect", "Final Report Generated.", "System")

@app.get("/logs")
def get_logs():
    return logs

@app.get("/metrics")
def get_metrics():
    return metrics

@app.get("/agents")
def get_agents():
    return [p.dict() for p in personas]

@app.get("/report")
def get_report():
    return {"report": final_report}

@app.get("/config")
def get_config():
    """Get current configuration"""
    return config

@app.post("/config")
async def update_config(fast_demo: bool):
    """Toggle fast demo mode"""
    global config
    config["fast_demo"] = fast_demo
    if fast_demo:
        config["max_exchanges"] = 25
        config["max_senate_exchanges"] = 5
    else:
        config["max_exchanges"] = 100
        config["max_senate_exchanges"] = 10
    return {"status": "Config updated", "config": config}

@app.post("/api/upload-policy")
async def upload_policy_file(file: bytes, filename: str, background_tasks: BackgroundTasks):
    """Upload a markdown policy file"""
    global policy_document
    try:
        content = file.decode('utf-8')
        policy_document = {"filename": filename, "content": content}
        
        # Extract policy summary (first paragraph or heading)
        lines = content.split('\n')
        policy_summary = '\n'.join(lines[:10])  # First 10 lines as summary
        
        # Reset state
        global logs, debate_history, observer_reports, final_report, metrics
        logs = []
        debate_history = []
        observer_reports = []
        final_report = ""
        metrics = []
        
        background_tasks.add_task(run_simulation, content)
        return {"status": "Policy file uploaded and simulation started", "filename": filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/submit-policy")
async def submit_policy(policy: str, background_tasks: BackgroundTasks):
    # Reset state
    global logs, debate_history, observer_reports, final_report, metrics
    logs = []
    debate_history = []
    observer_reports = []
    final_report = ""
    metrics = []
    
    background_tasks.add_task(run_simulation, policy)
    return {"status": "Simulation Started"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
