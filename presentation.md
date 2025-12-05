# PolicySwarm
## Recursive Consensus Engine for Policy Testing
### Team H5X | ZYND AI-ckathon | Policy Navigator - Public Good

---

# Slide 1: Title

# PolicySwarm 🐝

**Multi-Agent Collaboration for Policy Testing**

Team H5X | Vasanthadithya Mundrathi

*ZYND AI-ckathon | Policy Navigator - Public Good*

---

# Slide 2: The ZYND Challenge

## "From Isolated Agents to Intelligent Networks"

> Participants will work on multi-agent collaboration using Zynd's interoperability framework.

**The Challenge:** Move beyond isolated AI agents to interconnected agent ecosystems that can:
- Coordinate autonomously
- Share verified information
- Act collectively

**Our Answer:** PolicySwarm

---

# Slide 3: The Problem

## Citizens Struggle with Government Policies

- **Complex language** nobody understands
- **Hidden eligibility criteria** 
- **Missed benefits** worth thousands
- **Bureaucratic opacity** erodes trust

> *Example: India Farm Laws 2020 → Repealed after massive protests*

---

# Slide 4: Our Solution

## PolicySwarm: AI Agent Network for Policy Testing

```
Policy Input
     ↓
Citizens (10 agents) ──debate──→ Consensus?
     ↓                              NO → Loop
Senate (3 agents) ──analyze──→ Viable?
     ↓                              NO → Loop
Architect ──revise──→ Final PDF ✅
```

---

# Slide 5: ZYND Feature 1 - Functional Agent Networks

## 14 Agents with DID & Credentials

| Agent DID | Role | Credentials |
|-----------|------|-------------|
| `did:ps:citizen:anjali` | Teacher | Verified, Low-income |
| `did:ps:citizen:raju` | Auto Driver | Verified, Informal sector |
| `did:ps:senate:trend` | Trend Analyst | Govt. Advisory |
| `did:ps:senate:econ` | Economic Advisor | Fiscal Expert |
| `did:ps:architect:main` | Synthesizer | Highest Trust |

---

# Slide 6: ZYND Feature 2 - Trust-Based Interoperability

## Agents Discover, Authenticate, Collaborate

**Discovery:**
- Citizens engage with policy
- Senate observes citizen concerns

**Authentication:**
- Each opinion tagged with agent identity
- Trust weights based on credentials

**Collaboration:**
- *"I agree with Raju's point about prices..."*
- Trust chains: Citizen → Senate → Architect

---

# Slide 7: ZYND Feature 3 - Decentralized AI Governance

## Why Local LLM (Ollama)?

| Approach | Data Risk |
|----------|-----------|
| Cloud LLM | Sent to external servers ❌ |
| **Ollama (Local)** | Stays on your machine ✅ |

**Policy documents are SENSITIVE before publication!**

- ✅ No central authority
- ✅ Each agent operates autonomously
- ✅ Works completely offline

---

# Slide 8: Agent Architecture Details

## Citizen Agents (Level 1)

**10 diverse Indian personas:**
- 👩‍🏫 Anjali - Single mother, teacher
- 🚗 Raju - Auto-rickshaw driver
- 🏭 Vikram - Factory owner
- 👵 Kamla Devi - Retired pensioner
- 🎓 Arjun - Engineering student

**Each has:** Memory | Emotions | Realistic traits

---

# Slide 9: Senate Agents (Level 2)

## Government Advisory Committee

| Advisor | Focus |
|---------|-------|
| **Trend Analyst** | Public sentiment |
| **Economic Advisor** | Fiscal impact |
| **Constitutional Expert** | Legal viability |

**Strategic debate:** 5-10 exchanges with citizen awareness

---

# Slide 10: Features Delivered

| Requirement | Implementation |
|-------------|----------------|
| **Policy Interpretation** | Citizens explain in own words |
| **Eligibility Verification** | Each persona evaluates |
| **Benefit Matching** | Citizens identify personal impact |
| **Citizen Advocacy** | Architect addresses concerns |

---

# Slide 11: Tech Stack

| Layer | Technology |
|-------|------------|
| **LLM** | Ollama (gemma3:12b) - Local |
| **Backend** | FastAPI (Python) |
| **Frontend** | Next.js 16 + React |
| **PDF** | ReportLab (Gazette format) |
| **Real-time** | Polling + State sync |

---

# Slide 12: Dashboard Demo

## Live Features

- 📤 **File Upload** - Drag & drop .md policies
- 💬 **Citizen Chat** - Real-time debate view
- 🏛️ **Senate Chat** - Strategic discussion
- 📊 **Consensus Graph** - Score tracking
- ⏸️ **Cycle Control** - Pause/Continue/Download
- 📄 **PDF Export** - Government-style document

---

# Slide 13: PDF Output

## Professional Government Document

**Structure:**
1. Consensus Status (trust-weighted scores)
2. Eligibility Criteria
3. Benefits Summary
4. Policy Interpretation
5. Citizen Advocacy
6. Government Response

*Indian Gazette format: A4, Times Roman*

---

# Slide 14: Validation Results

| Policy | Real Outcome | PolicySwarm |
|--------|--------------|-------------|
| India Farm Laws 2020 | Repealed | Low score ✓ |
| India CAA 2019 | Protests | Divisive ✓ |
| UK Poll Tax 1989 | Repealed | Failed ✓ |

---

# Slide 15: ZYND Alignment Summary

| Expected Outcome | Our Delivery |
|-----------------|--------------|
| **Functional Agent Networks** | 14 agents with DID + credentials |
| **Trust-Based Interoperability** | Agents reference each other |
| **Decentralized Governance** | Local LLM, no central authority |
| **Real-World Scenario** | Indian policy testing |

---

# Slide 16: Future Scope

- 🌐 **Multi-language** (Hindi, Tamil, Telugu)
- 📱 **Citizen mobile app**
- 🔗 **Blockchain versioning**
- 🏢 **Government pilot programs**

---

# Slide 17: Quick Start

```bash
# Clone
git clone https://github.com/Vasanthadithya-mundrathi/PolicySwarm.git

# Setup
./setup.sh

# Start Ollama (recommended: gemma3:12b)
ollama pull gemma3:12b && ollama serve

# Run
./start.sh
```

---

# Slide 18: Thank You

## PolicySwarm 🐝

> "Because every policy deserves to be stress-tested by the people it will affect."

**Team H5X**  
Vasanthadithya Mundrathi

🐙 github.com/Vasanthadithya-mundrathi/PolicySwarm
