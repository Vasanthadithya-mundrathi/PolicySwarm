import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse
from agents.citizen_agent import CitizenAgent, CitizenPersona
from agents.observer_agent import ObserverAgent
from agents.architect_agent import ArchitectAgent
from core.pdf_generator import create_policy_pdf
import json

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
    "fast_demo": False,
    "max_exchanges": 100,
    "max_senate_exchanges": 10
}

# State
logs = []
debate_history = []
observer_reports = []
final_report = ""
metrics = []
policy_document = None
current_iteration = 0
simulation_paused = False
cycle_complete = False
current_policy = ""
revised_policy = ""
architect_logs = []  # Real-time architect analysis logs
senate_chat_logs = []  # Separate Senate chat logs

def log_event(agent_name: str, message: str, role: str = "System", log_type: str = "general"):
    print(f"[{agent_name}] {message}")
    log_entry = {"agent": agent_name, "role": role, "message": message, "type": log_type}
    logs.append(log_entry)
    
    # Route to specific log types
    if log_type == "senate":
        senate_chat_logs.append(log_entry)
    elif log_type == "architect":
        architect_logs.append(log_entry)

# Initialize Agents with realistic Indian personas
personas = [
    CitizenPersona(
        name="Anjali", role="Single Mother",
        background="35, PWD teacher in Mumbai, 2 kids. Relies on mid-day meal scheme for children.",
        traits=["Struggling with inflation", "Worried about education costs", "Skeptical of promises", "Prioritizes stability"]
    ),
    CitizenPersona(
        name="Raju", role="Auto Driver",
        background="42, Auto-rickshaw driver in Delhi. Paying EMI on vehicle. No health insurance.",
        traits=["Values freedom", "Hates sudden rule changes", "Cash-dependent", "Street smart but cynical"]
    ),
    CitizenPersona(
        name="Vikram", role="Business Owner",
        background="48, Owns textile factory in Surat. 200 employees. GST compliant.",
        traits=["Dislikes bureaucracy", "Focused on growth", "Pragmatic", "Votes for stability"]
    ),
    CitizenPersona(
        name="Kamla Devi", role="Retired Teacher",
        background="68, Retired government school teacher. Lives in Jaipur. Depends on pension.",
        traits=["Protective of pension", "Healthcare is priority", "Distrusts new schemes", "Votes consistently"]
    ),
    CitizenPersona(
        name="Arjun", role="College Student",
        background="21, Engineering student in Bangalore. Education loan. Climate activist.",
        traits=["Idealistic", "Anxious about jobs", "Active on social media", "Questions authority"]
    ),
    CitizenPersona(
        name="Lakshmi", role="Small Shop Owner",
        background="40, Runs kirana store in Chennai. Competes with online giants.",
        traits=["Hardworking", "Stressed about competition", "Community-focused", "Cash business"]
    ),
    CitizenPersona(
        name="Arun", role="IT Professional",
        background="29, Software engineer in Hyderabad. High earner but can't afford flat.",
        traits=["Ambitious", "Frustrated by housing costs", "Pro-digital", "Global outlook"]
    ),
    CitizenPersona(
        name="Bholaram", role="Factory Worker",
        background="45, Works in automobile plant in Pune. Union member. 25 years experience.",
        traits=["Values job security", "Loyal to union", "Skeptical of automation", "Traditional values"]
    ),
    CitizenPersona(
        name="Dr. Priya", role="Government Doctor",
        background="36, Works at district hospital in UP. Overworked. Posted in rural area.",
        traits=["Passionate about service", "Burned out", "Critical of health infrastructure", "Empathetic"]
    ),
    CitizenPersona(
        name="Ramesh", role="Farmer",
        background="55, Wheat farmer in Punjab. 10 acres. Worried about MSP and water.",
        traits=["Independent", "Worried about input costs", "Distrusts corporates", "Protective of land"]
    )
]

citizens = [CitizenAgent(p) for p in personas]

observers = [
    ObserverAgent(role="Trend Analyst", focus="Social Sentiment & Public Opinion"),
    ObserverAgent(role="Economic Advisor", focus="Fiscal Impact & Implementation Cost"),
    ObserverAgent(role="Constitutional Expert", focus="Legal Validity & Rights Protection")
]

architect = ArchitectAgent()

async def run_simulation(initial_policy: str):
    global final_report, current_iteration, simulation_paused, cycle_complete
    global current_policy, revised_policy, architect_logs, senate_chat_logs
    
    current_policy = initial_policy
    cycle_complete = False
    
    for iteration in range(1, 4):
        current_iteration = iteration
        
        # Check if paused
        while simulation_paused:
            await asyncio.sleep(1)
        
        if cycle_complete:
            break
            
        log_event("System", f"═══════════════════════════════════════")
        log_event("System", f"  ITERATION {iteration}/3 STARTING")
        log_event("System", f"═══════════════════════════════════════")
        
        # LEVEL 1: Citizen Conversation
        log_event("System", "Phase 1: Citizen Swarm Debate", log_type="general")
        
        # Reset citizens for new iteration (but keep memory)
        if iteration > 1:
            for c in citizens:
                c.reset_for_new_iteration(current_policy, iteration)
        
        # Initial reactions
        tasks = [c.react_to_policy(current_policy, iteration) for c in citizens]
        reactions = await asyncio.gather(*tasks)
        
        citizen_scores = []
        conversation_messages = []
        citizen_feedback = []
        
        for r in reactions:
            emotional = r.get('emotional_state', 'neutral')
            msg = f"[{emotional.upper()}] {r['message']} (Score: {r['score']})"
            log_event(r["agent"], msg, r["role"])
            conversation_messages.append({"agent": r["agent"], "role": r["role"], "message": r['message']})
            debate_history.append(r)
            citizen_scores.append(r['score'])
            citizen_feedback.append(r)
            await asyncio.sleep(0.1)
        
        # Conversational debate
        max_exchanges = config["max_exchanges"]
        log_event("System", f"Citizens engaging in conversation ({max_exchanges} exchanges)...")
        
        import random
        active_citizens = list(citizens)
        exchange_count = len(reactions)
        
        while exchange_count < max_exchanges and len(active_citizens) > 2:
            if simulation_paused or cycle_complete:
                break
                
            speaker = random.choice(active_citizens)
            
            reply_data = await speaker.reply_to_conversation(
                current_policy, 
                conversation_messages, 
                exchange_count,
                iteration
            )
            
            if reply_data["should_exit"]:
                exit_msg = f"{reply_data['message']} [Leaving: {reply_data['exit_reason']}]"
                log_event(speaker.name, exit_msg, speaker.role)
                conversation_messages.append({"agent": speaker.name, "role": speaker.role, "message": exit_msg})
                active_citizens.remove(speaker)
                log_event("System", f"👋 {speaker.name} has left the conversation.")
            else:
                log_event(speaker.name, reply_data['message'], speaker.role)
                conversation_messages.append({"agent": speaker.name, "role": speaker.role, "message": reply_data['message']})
                debate_history.append({"agent": speaker.name, "role": speaker.role, "message": reply_data['message']})
            
            exchange_count += 1
            await asyncio.sleep(0.3)
        
        log_event("System", f"Citizen debate concluded: {exchange_count} exchanges.")
        avg_citizen_score = sum(citizen_scores) / len(citizen_scores) if citizen_scores else 0
        log_event("System", f"📊 Average Citizen Satisfaction: {avg_citizen_score:.1f}%")
        
        # LEVEL 2: Senate Strategic Debate
        log_event("System", "Phase 2: Senate Strategic Debate", log_type="senate")
        senate_chat_logs = []  # Clear for new iteration
        
        # Reset observers for new iteration
        if iteration > 1:
            citizen_summary = " ".join([f['message'][:50] for f in citizen_feedback[:5]])
            for o in observers:
                o.reset_for_new_iteration(current_policy, citizen_summary, iteration)
        
        # Initial Senate analysis
        full_conversation = "\n".join([f"{m['agent']}: {m['message']}" for m in conversation_messages[:20]])
        
        tasks = [o.analyze_debate(current_policy, citizen_feedback, iteration) for o in observers]
        initial_reports = await asyncio.gather(*tasks)
        
        senate_scores = []
        senate_messages = []
        
        for r in initial_reports:
            msg = f"[INITIAL] {r['message']} (Viability: {r['score']}%, Recommendation: {r.get('recommendation', 'pending')})"
            log_event(r["agent"], msg, r["focus"], log_type="senate")
            senate_messages.append({"agent": r["agent"], "role": r["focus"], "message": r['message']})
            senate_scores.append(r['score'])
            observer_reports.append(r)
            await asyncio.sleep(0.3)
        
        # Senate conversation
        max_senate_exchanges = config["max_senate_exchanges"]
        log_event("System", f"Senate strategic discussion ({max_senate_exchanges} exchanges)...", log_type="senate")
        
        senate_exchange_count = 0
        while senate_exchange_count < max_senate_exchanges:
            if simulation_paused or cycle_complete:
                break
                
            speaker = random.choice(observers)
            
            reply_data = await speaker.reply_to_senate_debate(
                current_policy,
                full_conversation,
                senate_messages,
                senate_exchange_count,
                iteration
            )
            
            log_event(speaker.role, reply_data['message'], speaker.focus, log_type="senate")
            senate_messages.append({"agent": speaker.role, "role": speaker.focus, "message": reply_data['message']})
            
            senate_exchange_count += 1
            await asyncio.sleep(0.4)
        
        # Final verdict from each Senate member
        log_event("System", "Senate finalizing verdicts...", log_type="senate")
        
        tasks = [o.final_verdict(current_policy, senate_messages, avg_citizen_score, iteration) for o in observers]
        final_verdicts = await asyncio.gather(*tasks)
        
        senate_scores = []
        for v in final_verdicts:
            log_event(v["agent"], v['message'], v["focus"], log_type="senate")
            senate_scores.append(v['score'])
            observer_reports.append(v)
            await asyncio.sleep(0.3)
        
        avg_senate_score = sum(senate_scores) / len(senate_scores) if senate_scores else 0
        log_event("System", f"📊 Average Senate Viability: {avg_senate_score:.1f}%", log_type="senate")
        
        # Record metrics
        metrics.append({
            "iteration": iteration,
            "citizen_score": round(avg_citizen_score, 1),
            "senate_score": round(avg_senate_score, 1)
        })
        
        # Check consensus
        if avg_citizen_score >= 75 and avg_senate_score >= 80:
            log_event("System", "🎉 CONSENSUS REACHED!")
            cycle_complete = True
            final_report = architect.get_downloadable_policy(current_policy, metrics)
            break
        
        # LEVEL 3: Architect Analysis & Revision
        log_event("System", "Phase 3: Architect Analysis", log_type="architect")
        architect_logs = []  # Clear for new iteration
        
        log_event("Architect", "Beginning step-by-step policy analysis...", "Policy Architect", log_type="architect")
        
        # Run architect analysis
        synthesis = await architect.generate_report(
            current_policy, 
            observer_reports, 
            citizen_feedback, 
            iteration
        )
        
        # Log architect's steps
        for step_log in architect.get_analysis_logs():
            log_event("Architect", f"[{step_log['step']}] {step_log['content'][:200]}...", "Analysis", log_type="architect")
            await asyncio.sleep(0.2)
        
        # Update policy for next iteration
        revised_policy = synthesis.get("new_policy", current_policy)
        final_report = synthesis.get("report_markdown", "")
        
        log_event("System", f"Policy revised for iteration {iteration + 1}")
        log_event("Architect", f"Changes: {json.dumps(synthesis.get('diff', {}).get('summary', 'Policy updated'))}", "Policy Architect", log_type="architect")
        
        current_policy = revised_policy
    
    if not cycle_complete:
        log_event("System", "⚠️ Max iterations reached. Best effort policy generated.")
        final_report = architect.get_downloadable_policy(current_policy, metrics)
    
    cycle_complete = True
    log_event("System", "Simulation complete. Policy ready for download.")

# API Endpoints
@app.get("/logs")
def get_logs():
    return logs

@app.get("/citizen-logs")
def get_citizen_logs():
    """Get only Citizen debate logs (excludes senate and architect)"""
    return [l for l in logs if l.get("type", "general") not in ["senate", "architect"]]

@app.get("/senate-logs")
def get_senate_logs():
    """Get only Senate conversation logs"""
    return senate_chat_logs

@app.get("/architect-logs")
def get_architect_logs():
    """Get real-time Architect analysis logs"""
    return architect_logs

@app.get("/metrics")
def get_metrics():
    return metrics

@app.get("/agents")
def get_agents():
    return [p.dict() for p in personas]

@app.get("/report")
def get_report():
    return {"report": final_report}

@app.get("/status")
def get_status():
    """Get current simulation status"""
    return {
        "iteration": current_iteration,
        "paused": simulation_paused,
        "complete": cycle_complete,
        "current_policy": current_policy[:200] if current_policy else ""
    }

@app.get("/config")
def get_config():
    return config

@app.post("/config")
async def update_config(fast_demo: bool):
    global config
    config["fast_demo"] = fast_demo
    if fast_demo:
        config["max_exchanges"] = 25
        config["max_senate_exchanges"] = 5
    else:
        config["max_exchanges"] = 100
        config["max_senate_exchanges"] = 10
    return {"status": "Config updated", "config": config}

@app.post("/api/pause-cycle")
async def pause_cycle():
    """Pause the current simulation"""
    global simulation_paused
    simulation_paused = True
    return {"status": "Simulation paused"}

@app.post("/api/continue-cycle")
async def continue_cycle():
    """Continue the paused simulation"""
    global simulation_paused
    simulation_paused = False
    return {"status": "Simulation resumed"}

@app.post("/api/stop-and-download")
async def stop_and_download():
    """Stop simulation and return downloadable policy"""
    global cycle_complete, simulation_paused
    cycle_complete = True
    simulation_paused = False
    
    download_content = architect.get_downloadable_policy(current_policy, metrics)
    return {"status": "Cycle stopped", "policy": download_content}

@app.get("/api/download-policy")
def download_policy():
    """Download the final policy as professional PDF"""
    # Gather data for PDF
    citizen_score = metrics[-1]["citizen_score"] if metrics else 50.0
    senate_score = metrics[-1]["senate_score"] if metrics else 50.0
    
    # Extract citizen feedback summary from logs
    citizen_msgs = [l["message"] for l in logs if l.get("type") != "senate" and l.get("type") != "architect" and l["role"] != "System"][:5]
    citizen_summary = "\n".join([f"• {msg[:150]}..." for msg in citizen_msgs]) if citizen_msgs else "No citizen feedback recorded."
    
    # Extract senate analysis from logs
    senate_msgs = [l["message"] for l in senate_chat_logs if l["agent"] != "System"][:3]
    senate_summary = "\n".join([f"• {msg[:150]}..." for msg in senate_msgs]) if senate_msgs else "No senate analysis recorded."
    
    # Generate PDF
    pdf_buffer = create_policy_pdf(
        policy_title=policy_document.get("filename", "Policy Document").replace(".md", "").replace("_", " ").title() if policy_document else "Policy Proposal",
        original_policy=current_policy or "No original policy provided.",
        revised_policy=architect.revised_policy if hasattr(architect, 'revised_policy') and architect.revised_policy else "Policy revision pending completion of consensus process.",
        citizen_feedback_summary=citizen_summary,
        senate_analysis=senate_summary,
        eligibility_criteria=[
            "All citizens affected by the policy provisions",
            "Registered taxpayers and benefit recipients",
            "Small business owners and entrepreneurs",
            "Vulnerable groups including senior citizens and low-income families",
            "Additional criteria as specified in policy sections"
        ],
        benefits_summary=[
            "Simplified access to government services",
            "Transparent eligibility verification process",
            "Reduced bureaucratic delays in benefit delivery",
            "Digital-first approach for faster processing",
            "Grievance redressal mechanism with defined timelines"
        ],
        citizen_score=citizen_score,
        senate_score=senate_score,
        iteration_count=current_iteration
    )
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=PolicySwarm_Report.pdf"}
    )

@app.post("/api/upload-policy")
async def upload_policy_file(file: str, filename: str, background_tasks: BackgroundTasks):
    """Upload a markdown policy file"""
    global policy_document, logs, debate_history, observer_reports, final_report, metrics
    global current_iteration, simulation_paused, cycle_complete, architect_logs, senate_chat_logs
    
    try:
        policy_document = {"filename": filename, "content": file}
        
        # Reset all state
        logs = []
        debate_history = []
        observer_reports = []
        final_report = ""
        metrics = []
        current_iteration = 0
        simulation_paused = False
        cycle_complete = False
        architect_logs = []
        senate_chat_logs = []
        
        background_tasks.add_task(run_simulation, file)
        return {"status": "Policy file uploaded and simulation started", "filename": filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/submit-policy")
async def submit_policy(policy: str, background_tasks: BackgroundTasks):
    global logs, debate_history, observer_reports, final_report, metrics
    global current_iteration, simulation_paused, cycle_complete, architect_logs, senate_chat_logs
    
    # Reset all state
    logs = []
    debate_history = []
    observer_reports = []
    final_report = ""
    metrics = []
    current_iteration = 0
    simulation_paused = False
    cycle_complete = False
    architect_logs = []
    senate_chat_logs = []
    
    background_tasks.add_task(run_simulation, policy)
    return {"status": "Simulation Started"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
