# PolicySwarm 🐝
## Recursive Consensus Engine for Policy Testing

> **Team H5X | ZYND AI-ckathon | Track: Policy Navigator - Public Good**

[![ZYND](https://img.shields.io/badge/Protocol-ZYND-orange)]() [![Ollama](https://img.shields.io/badge/LLM-Ollama%20gemma3:12b-blue)]() [![Privacy](https://img.shields.io/badge/Privacy-Local%20First-green)]()

---

## 🎯 Problem Statement

> *"Create agent advocates that verify eligibility, interpret complex policies, and guide citizens with trust-backed recommendations—ending bureaucratic opacity."*

**The Challenge:** Citizens miss vital benefits because government policies are:
- Written in complex bureaucratic language
- Have hidden eligibility criteria
- Lack clear benefit explanations
- Published without public stress-testing

---

## 💡 Our Solution: PolicySwarm

A **multi-agent collaboration network** that stress-tests policies using ZYND Protocol's interoperability framework.

```
📄 Policy Input
       ↓
🧑‍🤝‍🧑 Level 1: Citizen Agent Network (10 authenticated agents debate)
       ↓
🏛️ Level 2: Senate Agent Network (3 credentialed advisors analyze)
       ↓
🏗️ Level 3: Architect Agent (synthesizes with verified trust chain)
       ↓
📊 Consensus Check → Loop or ✅ Final PDF
```

---

## 🔗 How We Use ZYND Protocol

### The ZYND Challenge: "From Isolated Agents to Intelligent Networks"

PolicySwarm directly addresses ZYND's core mission: **moving beyond isolated AI agents to interconnected agent ecosystems that coordinate autonomously.**

---

### 1. Functional Agent Networks (DID Model)

Each agent has a **Decentralized Identity (DID)** with defined credentials:

| Agent DID | Role | Credentials | Trust Level |
|-----------|------|-------------|-------------|
| `did:ps:citizen:anjali` | Single Mother | Teacher, PWD employee | Verified |
| `did:ps:citizen:raju` | Auto Driver | Self-employed, No insurance | Verified |
| `did:ps:senate:trend` | Trend Analyst | Govt. Advisory Role | High Trust |
| `did:ps:senate:econ` | Economic Advisor | Fiscal Policy Expert | High Trust |
| `did:ps:senate:law` | Constitutional Expert | Legal Review Authority | High Trust |
| `did:ps:architect:main` | Policy Architect | Final Synthesis Authority | Highest Trust |

**14 agents** work as a coordinated network, each with:
- ✅ Unique identity (name, role, background)
- ✅ Verifiable credentials (expertise, trust level)
- ✅ Persistent memory across sessions
- ✅ Emotional state tracking

---

### 2. Trust-Based Interoperability

Agents **discover, authenticate, and collaborate** following ZYND's principles:

**Discovery:**
- Citizens find and engage with the policy
- Senate discovers citizen concerns through observation
- Architect discovers synthesis opportunities

**Authentication:**
- Each agent's opinion is tagged with their identity
- Senate advisors have higher trust weight than individual citizens
- Architect verifies all inputs before synthesis

**Collaboration:**
- Agents reference each other: *"I agree with Raju's point..."*
- Trust chains form: Citizen → Senate → Architect
- Collective intelligence emerges from debate

```
Citizen:Anjali ──(debates)──→ Citizen:Raju
       ↓                           ↓
Senate:TrendAnalyst ←──(observes)──┘
       ↓
Senate:EconomicAdvisor ──(validates)──→ Senate:ConstitutionalExpert
       ↓
Architect ←──(synthesizes with trust weights)──┘
```

---

### 3. Decentralized AI Governance

**Why Local LLM (Ollama)?**

Policy documents are **SENSITIVE government data.** Before publication, policies must remain confidential.

| Approach | Data Location | Risk |
|----------|---------------|------|
| Cloud LLM (OpenAI/Gemini) | External servers | Data exposure |
| **ZYND + Ollama (Local)** | Your machine only | Zero exposure |

**Our decentralized approach:**
- ✅ No central authority controls the conversation
- ✅ Each agent operates autonomously with local inference
- ✅ Trust is computed through credential verification, not central servers
- ✅ Works completely offline

---

## ✅ Features Delivered (Problem → Solution)

| Requirement | Implementation |
|-------------|----------------|
| **Policy Interpretation** | Citizens explain policy in their own words |
| **Eligibility Verification** | Each persona evaluates based on their credentials |
| **Benefit Matching** | Citizens identify which aspects help them personally |
| **Citizen Advocacy** | Architect addresses concerns with trust-weighted synthesis |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Ollama** with `gemma3:12b` model (RECOMMENDED & TESTED)

### 1. Clone & Install
```bash
git clone https://github.com/Vasanthadithya-mundrathi/PolicySwarm.git
cd PolicySwarm
chmod +x setup.sh && ./setup.sh
```

### 2. Start Ollama
```bash
# Install Ollama (if not installed)
brew install ollama   # macOS
# or visit https://ollama.com

# Pull the recommended model (TESTED)
ollama pull gemma3:12b

# Start Ollama server
ollama serve
```

### 3. Run PolicySwarm
```bash
./start.sh
```

**Access:**
- 🖥️ **Frontend:** http://localhost:3000
- 🔌 **Backend API:** http://localhost:8000

### 4. Test with Sample Policy
Upload via dashboard:
```
sample_policies/india_farm_laws_2020.md
```

---

## ⚙️ LLM Configuration

Edit `backend/config.json`:

```json
{
    "llm_provider": "ollama",
    "ollama": { 
        "base_url": "http://localhost:11434",
        "model": "gemma3:12b" 
    },
    "openai": { "api_key": "sk-...", "model": "gpt-4o-mini" },
    "gemini": { "api_key": "...", "model": "gemini-1.5-flash" },
    "blaxel": { "api_key": "...", "workspace": "..." }
}
```

**✅ Recommended:** `gemma3:12b` via Ollama (tested & verified for this hackathon)

---

## 📁 Project Structure

```
PolicySwarm/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── config.json          # LLM provider config
│   ├── agents/
│   │   ├── citizen_agent.py # 10 citizen personas (DID: citizen:*)
│   │   ├── observer_agent.py # 3 senate advisors (DID: senate:*)
│   │   └── architect_agent.py # Policy synthesizer (DID: architect:main)
│   └── core/
│       ├── llm.py           # Multi-provider interface
│       └── pdf_generator.py # Gazette-style PDF
├── frontend/                # Next.js dashboard
├── sample_policies/         # Test policies
├── videoscript.md           # Demo video script
├── presentation.md          # Hackathon slides
├── setup.sh                 # Auto-install
└── start.sh                 # Launch servers
```

---

## 📄 Output: Professional PDF

Download generates a government-style PDF with:

1. **Consensus Status** - Trust-weighted scores
2. **Eligibility Criteria** - Who qualifies (from citizen feedback)
3. **Benefits Summary** - What citizens get
4. **Policy Interpretation** - Simplified language
5. **Citizen Advocacy** - Key concerns addressed
6. **Government Response** - Senate analysis

*Format: Indian Gazette style (A4, Times Roman, proper margins)*

---

## 🧪 Test Cases

| Policy | Real Outcome | PolicySwarm Prediction |
|--------|--------------|------------------------|
| India Farm Laws 2020 | Repealed | Low citizen score ✓ |
| India CAA 2019 | Protests | Divisive sentiment ✓ |
| UK Poll Tax 1989 | Repealed | Consensus failure ✓ |

---

## 🏆 ZYND Hackathon Alignment

### Expected Outcomes → Our Delivery

| ZYND Expectation | PolicySwarm Implementation |
|-----------------|---------------------------|
| **Functional Agent Networks** | 14 agents with DID, credentials, trust levels |
| **Trust-Based Interoperability** | Agents reference each other, weighted synthesis |
| **Decentralized AI Governance** | Local LLM, no central authority, offline capable |
| **Real-World Scenario** | Indian policy testing (Farm Laws, CAA, etc.) |

---

## 👥 Team H5X

**Vasanthadithya Mundrathi**  
Full Stack Developer

🐙 GitHub: [Vasanthadithya-mundrathi](https://github.com/Vasanthadithya-mundrathi)

---

## 📜 License

MIT License - Open for government and research use.

---

**PolicySwarm: Because every policy deserves to be stress-tested by the people it will affect.** 🐝
