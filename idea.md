# PolicySwarm: The Civic Intelligence Grid
**Project Design Reference (PDR) & Master Plan**

## 1. Executive Summary
**PolicySwarm** is a multi-agent simulation where "Citizen Agents" debate new government policies in real-time. "Observer Agents" analyze these debates to refine the policy, ensuring it meets the needs of all stakeholders before implementation.

*   **Theme**: Policy Navigator (Public Good)
*   **Core Innovation**: Swarm Intelligence for Democratic Feedback.
*   **Wow Factor**: Visualizing 10+ agents with distinct personas (Single Mom, CEO, Student) arguing over a policy, while a "Super-Agent" synthesizes the chaos into a perfect law.

---

## 2. The Problem
1.  **Disconnect**: Policymakers rarely understand the on-the-ground impact of laws until it's too late.
2.  **Complexity**: Policies are too complex for average citizens to digest.
3.  **Echo Chambers**: Feedback is usually limited to lobbyists or angry social media mobs.

## 3. The Solution: PolicySwarm (Recursive Consensus Engine)
A self-correcting feedback loop that evolves policy until everyone is satisfied.

### The 3-Layer Loop
1.  **Layer 1: The Citizens (The Swarm)**
    *   10 Agents react and output a **Satisfaction Score (0-100)**.
    *   *Goal*: Maximize personal benefit.
2.  **Layer 2: The Observers (The Senate)**
    *   Analyze Citizen feedback vs. National Strategy.
    *   Output a **Viability Score (0-100)**.
    *   *Goal*: Ensure economic/legal stability.
3.  **Layer 3: The Architect (The Optimizer)**
    *   Synthesizes feedback.
    *   **Rewrites the Policy** to improve scores.
    *   *Action*: Sends the *new* policy back to Layer 1.

### The "Equilibrium" Goal
The loop continues until:
*   **Citizen Satisfaction > 75%** AND **Gov Viability > 80%**
*   OR **Max Iterations (3)** reached.

---

## 4. Architecture (Recursive)

```mermaid
graph TD
    Input[User Proposal] --> Architect
    
    subgraph "The Iteration Loop"
        Architect -->|Draft v1| Swarm[L1: Citizens]
        Swarm -->|Feedback & Scores| Senate[L2: Observers]
        Senate -->|Strategy & Scores| Architect[L3: Architect]
    end
    
    Architect -->|Threshold Met?| Check{Done?}
    Check -- No -->|Refine Policy| Architect
    Check -- Yes --> Final[Final Optimized Policy]
```

### Tech Stack
*   **Backend**: FastAPI with a `while` loop managing the debate cycles.
*   **Metrics**: Agents now return JSON with `{ "message": "...", "score": 85 }`.
*   **Frontend**: Visualizes the **"Consensus Graph"** rising over time.

---

## 5. Detailed User Flow (The Demo)

### Phase 1: The Bad Proposal
1.  User: "Ban all cars in the city."
2.  **Iteration 1**:
    *   *Citizens*: "I can't get to work!" (Score: 20%)
    *   *Senate*: "Economic collapse imminent." (Score: 10%)
    *   *Architect*: "Rewriting to: Ban *gas* cars, invest in public transit."

### Phase 2: The Improvement
1.  **Iteration 2**:
    *   *Citizens*: "Better, but transit is slow." (Score: 50%)
    *   *Senate*: "Expensive, but sustainable." (Score: 60%)
    *   *Architect*: "Rewriting to: Phase out gas cars over 10 years, subsidize EVs."

### Phase 3: The Consensus
1.  **Iteration 3**:
    *   *Citizens*: "Fair enough." (Score: 80%)
    *   *Senate*: "Manageable transition." (Score: 85%)
    *   *Result*: **Loop Ends. Policy Ratified.**

---

## 6. Project Structure
```
/policyswarm
  /frontend          # Next.js Dashboard
  /backend
    /agents
      citizen_agent.py
      observer_agent.py
      architect_agent.py
    /core
      orchestrator.py
    main.py
  requirements.txt
```

## 7. Instructions for Judges
1.  `git clone <repo>`
2.  `cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
3.  `python main.py`
4.  `cd frontend && npm install && npm run dev`
5.  Open `localhost:3000`, enter a policy, and watch the swarm think!
