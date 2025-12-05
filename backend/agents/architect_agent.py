import asyncio
from core.llm import get_llm_response
import json

class ArchitectAgent:
    def __init__(self):
        self.role = "Chief Policy Architect"
        self.iteration_history = []
        self.analysis_logs = []  # For streaming real-time logs
        self.current_analysis = ""
    
    def log_step(self, step: str, content: str):
        """Log analysis step for real-time streaming"""
        log_entry = {"step": step, "content": content}
        self.analysis_logs.append(log_entry)
        return log_entry
    
    def get_analysis_logs(self):
        """Get all logged analysis steps"""
        return self.analysis_logs
    
    def clear_logs(self):
        """Clear logs for new analysis"""
        self.analysis_logs = []
    
    async def analyze_step_by_step(self, policy: str, citizen_feedback: list, senate_reports: list, iteration: int = 1):
        """Generate step-by-step analysis logs in real-time"""
        self.clear_logs()
        
        # Step 1: Summarize citizen concerns
        self.log_step("CITIZEN_ANALYSIS", "Analyzing citizen feedback...")
        
        citizen_summary = "\n".join([f"- {f['agent']} ({f.get('emotional_state', 'neutral')}): {f['message']}" for f in citizen_feedback[:15]])
        avg_citizen_score = sum(f.get('score', 50) for f in citizen_feedback) / len(citizen_feedback) if citizen_feedback else 50
        
        prompt_citizens = f"""
        Analyze these citizen responses to the policy:
        {citizen_summary}
        
        Average satisfaction: {avg_citizen_score:.1f}%
        
        Identify in JSON:
        {{
            "top_3_concerns": ["concern1", "concern2", "concern3"],
            "emotional_temperature": "angry/frustrated/mixed/hopeful",
            "key_affected_groups": ["group1", "group2"],
            "suggested_fixes": ["fix1", "fix2"]
        }}
        """
        from core.llm import get_json_response
        citizen_analysis = await asyncio.to_thread(get_json_response, prompt_citizens)
        
        self.log_step("CITIZEN_FINDINGS", json.dumps(citizen_analysis, indent=2))
        await asyncio.sleep(0.3)  # Simulate processing time
        
        # Step 2: Summarize Senate analysis
        self.log_step("SENATE_ANALYSIS", "Analyzing Senate recommendations...")
        
        senate_summary = "\n".join([f"- {r['agent']} (Score: {r.get('score', 'N/A')}): {r['message']}" for r in senate_reports])
        avg_senate_score = sum(r.get('score', 50) for r in senate_reports) / len(senate_reports) if senate_reports else 50
        
        prompt_senate = f"""
        Analyze these Senate observer reports:
        {senate_summary}
        
        Average viability score: {avg_senate_score:.1f}%
        
        Identify in JSON:
        {{
            "consensus_areas": ["area1", "area2"],
            "disagreement_areas": ["area1"],
            "implementation_risks": ["risk1", "risk2"],
            "political_feasibility": "high/medium/low"
        }}
        """
        senate_analysis = await asyncio.to_thread(get_json_response, prompt_senate)
        
        self.log_step("SENATE_FINDINGS", json.dumps(senate_analysis, indent=2))
        await asyncio.sleep(0.3)
        
        # Step 3: Identify conflicts
        self.log_step("CONFLICT_ANALYSIS", "Identifying citizen vs government conflicts...")
        
        prompt_conflicts = f"""
        Citizen concerns: {json.dumps(citizen_analysis.get('top_3_concerns', []))}
        Senate concerns: {json.dumps(senate_analysis.get('implementation_risks', []))}
        
        Identify conflicts in JSON:
        {{
            "conflicts": [
                {{"citizen_want": "X", "government_concern": "Y", "resolution_approach": "Z"}}
            ],
            "aligned_areas": ["area1", "area2"],
            "impossible_to_reconcile": ["item1"] or []
        }}
        """
        conflict_analysis = await asyncio.to_thread(get_json_response, prompt_conflicts)
        
        self.log_step("CONFLICTS_IDENTIFIED", json.dumps(conflict_analysis, indent=2))
        await asyncio.sleep(0.3)
        
        return {
            "citizen_analysis": citizen_analysis,
            "senate_analysis": senate_analysis,
            "conflict_analysis": conflict_analysis,
            "avg_citizen_score": avg_citizen_score,
            "avg_senate_score": avg_senate_score
        }
    
    async def generate_revised_policy(self, original_policy: str, analysis: dict, iteration: int = 1):
        """Generate revised policy based on analysis"""
        self.log_step("POLICY_REVISION", f"Drafting revised policy for iteration {iteration + 1}...")
        
        prompt = f"""
        You are the Chief Policy Architect. Based on the analysis, revise the policy.
        
        ORIGINAL POLICY:
        {original_policy}
        
        CITIZEN CONCERNS: {json.dumps(analysis.get('citizen_analysis', {}).get('top_3_concerns', []))}
        SUGGESTED FIXES: {json.dumps(analysis.get('citizen_analysis', {}).get('suggested_fixes', []))}
        SENATE RISKS: {json.dumps(analysis.get('senate_analysis', {}).get('implementation_risks', []))}
        CONFLICTS: {json.dumps(analysis.get('conflict_analysis', {}).get('conflicts', []))}
        
        Current Scores:
        - Citizen Satisfaction: {analysis.get('avg_citizen_score', 50):.1f}%
        - Senate Viability: {analysis.get('avg_senate_score', 50):.1f}%
        
        TARGET: Citizen > 75%, Senate > 80%
        
        Write a revised policy that:
        1. Addresses the top citizen concerns
        2. Maintains government viability
        3. Resolves identified conflicts
        4. Is specific and actionable
        
        Return JSON:
        {{
            "revised_policy": "The complete revised policy text (200-400 words)...",
            "changes_summary": ["Change 1", "Change 2", "Change 3"],
            "expected_citizen_improvement": "+X%",
            "expected_senate_improvement": "+X%"
        }}
        """
        from core.llm import get_json_response
        revision = await asyncio.to_thread(get_json_response, prompt)
        
        self.log_step("REVISION_COMPLETE", json.dumps({
            "changes": revision.get("changes_summary", []),
            "expected_improvements": {
                "citizen": revision.get("expected_citizen_improvement", "N/A"),
                "senate": revision.get("expected_senate_improvement", "N/A")
            }
        }, indent=2))
        
        return revision
    
    async def generate_diff(self, original_policy: str, revised_policy: str):
        """Generate diff-style comparison"""
        self.log_step("DIFF_GENERATION", "Generating policy diff...")
        
        prompt = f"""
        Compare these two policies and generate a diff summary:
        
        ORIGINAL:
        {original_policy[:500]}
        
        REVISED:
        {revised_policy[:500]}
        
        Return JSON:
        {{
            "removed": ["Text removed 1", "Text removed 2"],
            "added": ["Text added 1", "Text added 2"],
            "modified": ["Original -> New text"],
            "summary": "One sentence summary of key changes"
        }}
        """
        from core.llm import get_json_response
        diff = await asyncio.to_thread(get_json_response, prompt)
        
        self.log_step("DIFF_COMPLETE", json.dumps(diff, indent=2))
        
        return diff
    
    async def generate_report(self, policy: str, observer_reports: list[dict], citizen_feedback: list = None, iteration: int = 1):
        """Complete analysis and report generation"""
        # Store in history
        self.iteration_history.append({
            "iteration": iteration,
            "policy": policy[:300],
            "citizen_score": sum(f.get('score', 50) for f in citizen_feedback) / len(citizen_feedback) if citizen_feedback else 0,
            "senate_score": sum(r.get('score', 50) for r in observer_reports) / len(observer_reports) if observer_reports else 0
        })
        
        # Run step-by-step analysis
        analysis = await self.analyze_step_by_step(policy, citizen_feedback or [], observer_reports, iteration)
        
        # Generate revised policy
        revision = await self.generate_revised_policy(policy, analysis, iteration)
        
        # Generate diff
        diff = await self.generate_diff(policy, revision.get("revised_policy", policy))
        
        # Generate final markdown report
        self.log_step("REPORT_GENERATION", "Generating final report...")
        
        report_md = f"""# Policy Analysis Report - Iteration {iteration}

## 📊 Current Scores
- **Citizen Satisfaction**: {analysis['avg_citizen_score']:.1f}%
- **Senate Viability**: {analysis['avg_senate_score']:.1f}%
- **Target**: Citizen > 75%, Senate > 80%

## 🔍 Key Findings

### Citizen Concerns
{chr(10).join(['- ' + c for c in analysis.get('citizen_analysis', {}).get('top_3_concerns', ['N/A'])])}

### Senate Assessment
{chr(10).join(['- ' + r for r in analysis.get('senate_analysis', {}).get('implementation_risks', ['N/A'])])}

## 📝 Policy Changes Made
{chr(10).join(['- ' + c for c in revision.get('changes_summary', ['No changes'])])}

## 📄 Revised Policy
{revision.get('revised_policy', 'No revision generated.')}

## 📈 Expected Impact
- Citizen Score: {revision.get('expected_citizen_improvement', 'N/A')}
- Senate Score: {revision.get('expected_senate_improvement', 'N/A')}

---
*Generated by PolicySwarm Architect Agent*
"""
        
        self.log_step("COMPLETE", "Analysis complete. Ready for next iteration or download.")
        
        return {
            "new_policy": revision.get("revised_policy", policy),
            "report_markdown": report_md,
            "diff": diff,
            "analysis": analysis,
            "iteration": iteration
        }
    
    def get_downloadable_policy(self, final_policy: str, iteration_history: list = None):
        """Generate downloadable markdown policy document"""
        history = iteration_history or self.iteration_history
        
        iterations_md = ""
        for h in history:
            iterations_md += f"- Iteration {h['iteration']}: Citizen {h['citizen_score']:.1f}%, Senate {h['senate_score']:.1f}%\n"
        
        return f"""# Final Policy Document
*Generated by PolicySwarm - Recursive Consensus Engine*

## Policy Status: CONSENSUS REACHED ✓

## Iteration History
{iterations_md}

## Final Policy
{final_policy}

---
*This policy has been stress-tested through {len(history)} iterations of citizen and government debate.*
"""
