# PolicySwarm - Recursive Consensus Engine

## Project Overview
**PolicySwarm** is an AI-powered multi-agent simulation that stress-tests government policies before they are released. It uses a **Recursive Consensus Engine** to debate, analyze, and rewrite policies until they meet a satisfaction threshold.

### Key Features
*   **3-Level Recursive Loop**:
    1.  **Citizen Swarm (Level 1)**: 10 AI agents with realistic UK personas (e.g., Single Mom, Gig Worker, CEO, Farmer) engage in a **rich conversational debate** (up to 100 exchanges). Agents respond to each other's points naturally, and can exit the conversation when appropriate (e.g., "Tom: Need to check my fields now").
    2.  **Senate Strategic Debate (Level 2)**: Observer agents (Trend Watcher, Strategy Lead, Ethics Guardian) analyze the **full citizen conversation**, then engage in a **10-exchange strategic debate** from government/company viability perspectives before finalizing their scores.
    3.  **Architect Synthesis (Level 3)**: The Chief Architect rewrites the policy based on Senate feedback and citizen concerns, then feeds it back to Level 1 for another iteration until consensus is reached.
*   **Local AI**: Powered by **Ollama (`gemma3:12b`)** for privacy and zero cost.
*   **Premium Dashboard**: Next.js UI with real-time "Consensus Graph", animated debate feed, and glassmorphism design.

## How to Run
1.  **Start Ollama**: `ollama serve`
2.  **Start Backend**: `cd backend && source virtualpyenv/bin/activate && python main.py`
3.  **Start Frontend**: `cd frontend && npm run dev`
4.  **Open App**: [http://localhost:3001](http://localhost:3001)

## Real-World Test Case: The "Poll Tax" (1990)
To see the engine in action, we simulate the infamous UK Community Charge.

**Input Policy:**
> "Replace property taxes with a flat-rate 'Community Charge' payable by every adult, regardless of income or property value."

**Expected Outcome:**
1.  **Iteration 1**: Massive backlash from low-income agents (Sarah, Jamal). Scores drop below 30%.
2.  **Iteration 2**: Architect attempts to add rebates, but the core "flat rate" issue remains.
3.  **Iteration 3**: Architect pivots to a property-band system (like Council Tax). Consensus reached!

## Troubleshooting
*   **Hydration Error?**: Fixed. If seen, refresh the page.
*   **Input Scrolling?**: Fixed. Input bar is now sticky at the top.
