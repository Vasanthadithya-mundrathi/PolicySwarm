# PolicySwarm - Recursive Consensus Engine

## 🎯 What It Does
Stress-tests government policies through **3 levels of AI debate** before they reach humans.

---

## 🔄 The 3-Level Loop

### **Level 1: Citizen Swarm** 🗣️
- **100 conversational exchanges** between 10 realistic UK personas
- Agents respond to each other naturally ("Tom, I hear your point, but...")
- Natural exits when appropriate ("Need to check my fields now")
- **Output**: Citizen Satisfaction Score (0-100%)

### **Level 2: Senate Strategic Debate** 🏛️
- **10 strategic exchanges** between 3 government observers
- Debate from viability/implementation perspective
- Reference each other's points professionally
- **Output**: Senate Viability Score (0-100%)

### **Level 3: Architect Synthesis** 🏗️
- Synthesizes citizen concerns + Senate analysis
- Rewrites policy to address issues
- **Output**: Revised Policy → back to Level 1

### **Consensus Criteria**
✅ **Success**: Citizen Score > 75% AND Senate Score > 80%  
🔄 **Repeat**: If not met, loop back (max 3 iterations)  
📤 **Result**: Final policy shared with humans

---

## 🚀 Quick Start

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Backend
cd backend
source virtualpyenv/bin/activate
python main.py

# Terminal 3: Frontend
cd frontend
npm run dev

# Browser: http://localhost:3001
```

---

## 🧪 Test Case: UK Poll Tax (1990)

**Input Policy:**
```
Replace property taxes with a flat-rate 'Community Charge' 
payable by every adult, regardless of income or property value.
```

**Expected Result (3 iterations):**
1. **Iteration 1**: Massive citizen backlash → Architect adds rebates
2. **Iteration 2**: Still controversial → Architect pivots to income bands
3. **Iteration 3**: Consensus reached! → Property-band system approved ✅

---

## 💡 Key Features

✅ **Real Conversations**: 100 citizen + 10 Senate exchanges (all LLM-generated)  
✅ **Contextual**: Agents reference each other's specific points  
✅ **Natural Behavior**: Agents can exit conversations appropriately  
✅ **Government Perspective**: Senate debates viability/implementation  
✅ **Iterative Refinement**: Policy improves across iterations  
✅ **Local & Private**: Runs on Ollama (gemma3:12b) - zero API costs  
✅ **Premium UI**: Next.js dashboard with real-time updates  

---

## 📁 Project Structure

```
ZYND project/
├── backend/
│   ├── main.py                    # 3-level simulation loop
│   ├── agents/
│   │   ├── citizen_agent.py       # Level 1: Conversational citizens
│   │   ├── observer_agent.py      # Level 2: Strategic Senate
│   │   └── architect_agent.py     # Level 3: Policy synthesis
│   └── core/llm.py               # Ollama integration
├── frontend/
│   ├── src/app/page.tsx          # Main dashboard
│   └── src/components/
│       ├── DebateFeed.tsx        # Live debate log
│       ├── SenateView.tsx        # Senate analysis view
│       ├── ArchitectView.tsx     # Architect synthesis view
│       └── ...
└── walkthrough.md                # Detailed guide
```

---

## 🎨 UI Views

1. **Dashboard** - Policy input + live debate + metrics + report
2. **Agents** - View all 10 citizen personas
3. **Senate** - Dedicated Senate debate view
4. **Architect** - Policy evolution tracker
5. **Settings** - Configuration (placeholder)

---

## ⚙️ Tech Stack

**Backend**: FastAPI + Python + Ollama (gemma3:12b)  
**Frontend**: Next.js 14 + TypeScript + Tailwind + Framer Motion  
**Charts**: Recharts  
**Markdown**: ReactMarkdown  

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Exchanges per iteration | ~110 (100 citizen + 10 Senate) |
| Full 3-iteration simulation | ~45-60 minutes |
| Total LLM calls | ~330 |
| Unique personas | 14 (10 citizens + 3 senators + 1 architect) |

**Tip**: Reduce `MAX_EXCHANGES = 100` to `25` in `main.py` for faster testing

---

## 🐛 Troubleshooting

**Backend not updating?**  
→ Restart backend: `Ctrl+C` then `python main.py`

**Frontend not showing new data?**  
→ Clear cache and refresh (Cmd+Shift+R)

**Simulation too slow?**  
→ Reduce exchange counts in `main.py` (lines 125, 190)

**Ollama not responding?**  
→ Check `ollama serve` is running  
→ Verify `ollama list` shows `gemma3:12b`

---

## 📚 Documentation

- [walkthrough.md](walkthrough.md) - Quick start guide
- [FINAL_IMPLEMENTATION.md](.gemini/.../FINAL_IMPLEMENTATION.md) - Complete technical summary
- [project_summary.md](.gemini/.../project_summary.md) - Detailed feature list

---

## 🏆 What Makes This Special

This isn't a demo or simulation with placeholder data. **Every single message is generated in real-time by AI agents** that:
- Have unique personalities and backgrounds
- Reference each other's points contextually
- Debate from different perspectives (citizen vs. government)
- Iteratively refine policies until consensus is reached

It's democracy at scale, tested before it reaches humans. 🚀

---

## 👨‍💻 Built With

- **Ollama** (Local LLM inference)
- **Google Gemma 3** (12B parameter model)
- **FastAPI** (Python backend)
- **Next.js** (React frontend)
- **Tailwind CSS** (Styling)
- **Framer Motion** (Animations)

---

**Ready to test your first policy? Fire up the servers and watch the swarm debate! 🐝**
