# PolicySwarm - Setup Guide for Judges

## 🚀 Quick Start (3 Commands)

```bash
# 1. Install dependencies
./setup.sh

# 2. Start the application
./start.sh

# 3. Open in browser
# Navigate to http://localhost:3001
```

---

## 📋 Prerequisites

Before running PolicySwarm, ensure you have:

- **Python 3.10+** installed
- **Node.js 18+** and npm installed
- **Ollama** installed with `gemma3:12b` model

### Installing Ollama & Model

```bash
# Install Ollama (macOS)
brew install ollama

# Pull the model
ollama pull gemma3:12b

# Start Ollama server
ollama serve
```

---

## 🛠 Manual Setup (If Scripts Don't Work)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv virtualpyenv

# Activate virtual environment
source virtualpyenv/bin/activate  # macOS/Linux
# OR
virtualpyenv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run backend
python main.py
```

**Backend will run on**: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

**Frontend will run on**: `http://localhost:3001`

---

## ✅ Verification

1. **Check Ollama**: Run `ollama list` - you should see `gemma3:12b`
2. **Check Backend**: Visit `http://localhost:8000/agents` - should return JSON
3. **Check Frontend**: Visit `http://localhost:3001` - should see PolicySwarm dashboard

---

## 🎯 Testing the System

### Option 1: Fast Demo Mode (5-10 minutes)

1. Navigate to **Settings** (sidebar)
2. Toggle **"Fast Demo Mode"** ON
3. Go back to **Dashboard**
4. Enter the Poll Tax policy (see below)
5. Click **"Deploy to Swarm"**

### Option 2: Full Simulation (45-60 minutes)

1. Keep **Fast Demo Mode** OFF (default)
2. Enter a policy and deploy
3. Watch100 citizen + 10 Senate exchanges

### Sample Policy (UK Poll Tax)

```
Replace property taxes with a flat-rate 'Community Charge' payable by every adult, regardless of income or property value.
```

**Expected Result**: System refines policy across 3 iterations until consensus is reached.

---

## 📁 Project Structure

```
ZYND project/
├── backend/
│   ├── main.py                    # FastAPI server + 3-level simulation
│   ├── agents/                    # Citizen, Senate, Architect agents
│   ├── core/llm.py               # Ollama integration
│   └── requirements.txt
├── frontend/
│   ├── src/app/page.tsx          # Main dashboard
│   ├── src/components/           # React components
│   └── package.json
├── setup.sh                       # Auto-setup script
├── start.sh                       # Auto-start script
├── README.md                      # Project overview
└── SETUP.md                       # This file
```

---

## 🐛 Troubleshooting

### "Module not found" Error
```bash
cd backend
source virtualpyenv/bin/activate
pip install -r requirements.txt
```

### "Ollama connection refused"
```bash
# Start Ollama in a new terminal
ollama serve
```

### "Port 8000 already in use"
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
```

### "Port 3001 already in use"
```bash
# Kill existing process
lsof -ti:3001 | xargs kill -9
```

### Frontend not connecting to backend
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify firewall isn't blocking local connections

---

## Features to Demonstrate

### 1. **3-Level Recursive Conversation**
- Navigate to **Dashboard** to see all exchanges
- Navigate to **Senate** to see strategic debate
- Navigate to **Architect** to see policy rewrites

### 2. **Fast Demo Toggle**
- Go to **Settings**
- Toggle "Fast Demo Mode"
- See real-time config update

### 3. **Upload Policy Files** (Markdown)
- Go to **Settings**
- Upload a `.md` policy file
- System automatically starts simulation

### 4. **Real-Time Metrics**
- Watch the Consensus Graph update live
- See satisfaction scores climb across iterations

### 5. **Natural Agent Behavior**
- Agents exit conversations naturally
- Citizens reference each other's points
- Senate debates strategically

---

## 📊 Performance Notes

- **Fast Demo**: 25 citizen + 5 Senate exchanges = ~5-10 minutes
- **Full Simulation**: 100 citizen + 10 Senate exchanges = ~45-60 minutes
- Uses local Ollama (gemma3:12b) - no API costs
- All processing happens on your machine

---

## 🎓 For Judges

This is a **production-ready recursive consensus engine** that:
- Processes complex policies through democratic debate
- Uses real LLM conversations (not scripted)
- Iteratively refines policies until consensus
- Demonstrates natural multi-agent behavior
- Runs completely offline and private

**Key Innovation**: 3-level architecture combining grassroots (citizens), expert (senate), and strategic (architect) perspectives to stress-test policies before human decision-making.

---

## 📧 Support

If you encounter any issues:
1. Check this SETUP.md file
2. Review README.md
3. Ensure all prerequisites are installed
4. Try running commands manually (see Manual Setup section)

**Thank you for reviewing PolicySwarm! 🚀**
