import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { User, Briefcase, Eye, Building2 } from 'lucide-react';

interface Agent {
    name: string;
    role: string;
    background: string;
    traits: string[];
}

const API_URL = "http://localhost:8000";

// Senate and Architect agents (hardcoded as they're system agents)
const systemAgents = [
    {
        name: "Trend Watcher",
        role: "Senate Observer",
        background: "Analyzes social sentiment and future trends from a government policy perspective.",
        traits: ["Social Impact Analysis", "Future Forecasting", "Public Opinion Expert"],
        type: "senate"
    },
    {
        name: "Strategy Lead",
        role: "Senate Observer",
        background: "Evaluates economic viability and implementation feasibility of policies.",
        traits: ["Economic Analysis", "Implementation Planning", "Risk Assessment"],
        type: "senate"
    },
    {
        name: "Ethics Guardian",
        role: "Senate Observer",
        background: "Ensures policies uphold fairness, human rights, and ethical standards.",
        traits: ["Fairness Advocate", "Human Rights Focus", "Equity Analysis"],
        type: "senate"
    },
    {
        name: "Chief Architect",
        role: "Policy Architect",
        background: "Synthesizes feedback from citizens and Senate to rewrite and improve policies iteratively.",
        traits: ["Strategic Synthesis", "Policy Design", "Consensus Building"],
        type: "architect"
    }
];

export default function AgentsView() {
    const [citizenAgents, setCitizenAgents] = useState<Agent[]>([]);

    useEffect(() => {
        axios.get(`${API_URL}/agents`).then(res => setCitizenAgents(res.data)).catch(console.error);
    }, []);

    return (
        <div className="space-y-8">
            {/* Citizens Section */}
            <div>
                <h3 className="text-2xl font-bold text-slate-100 mb-4 flex items-center gap-2">
                    <User className="w-6 h-6 text-blue-400" />
                    Level 1: Citizen Swarm (10 Personas)
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {citizenAgents.map((agent, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 hover:border-blue-500/50 transition-colors group"
                        >
                            <div className="flex items-center gap-4 mb-4">
                                <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 group-hover:bg-blue-500 group-hover:text-white transition-colors">
                                    <User className="w-6 h-6" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-slate-100">{agent.name}</h3>
                                    <p className="text-sm text-blue-400 font-medium">{agent.role}</p>
                                </div>
                            </div>

                            <div className="space-y-3">
                                <div className="flex items-start gap-2 text-slate-400 text-sm">
                                    <Briefcase className="w-4 h-4 mt-0.5 shrink-0" />
                                    <p>{agent.background}</p>
                                </div>
                                <div className="flex flex-wrap gap-2 mt-4">
                                    {agent.traits.map((trait, j) => (
                                        <span key={j} className="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded-md border border-slate-700">
                                            {trait}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Senate Section */}
            <div>
                <h3 className="text-2xl font-bold text-slate-100 mb-4 flex items-center gap-2">
                    <Eye className="w-6 h-6 text-emerald-400" />
                    Level 2: Senate (3 Strategic Observers)
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {systemAgents.filter(a => a.type === "senate").map((agent, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.5 + i * 0.1 }}
                            className="bg-gradient-to-br from-emerald-900/20 to-slate-900/50 border border-emerald-500/30 rounded-2xl p-6 hover:border-emerald-500/50 transition-colors group"
                        >
                            <div className="flex items-center gap-4 mb-4">
                                <div className="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 group-hover:bg-emerald-500 group-hover:text-white transition-colors">
                                    <Eye className="w-6 h-6" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-slate-100">{agent.name}</h3>
                                    <p className="text-sm text-emerald-400 font-medium">{agent.role}</p>
                                </div>
                            </div>

                            <div className="space-y-3">
                                <p className="text-slate-400 text-sm">{agent.background}</p>
                                <div className="flex flex-wrap gap-2 mt-4">
                                    {agent.traits.map((trait, j) => (
                                        <span key={j} className="text-xs bg-emerald-900/30 text-emerald-300 px-2 py-1 rounded-md border border-emerald-700">
                                            {trait}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Architect Section */}
            <div>
                <h3 className="text-2xl font-bold text-slate-100 mb-4 flex items-center gap-2">
                    <Building2 className="w-6 h-6 text-purple-400" />
                    Level 3: Architect (Policy Synthesizer)
                </h3>
                <div className="grid grid-cols-1 gap-6">
                    {systemAgents.filter(a => a.type === "architect").map((agent, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.8 }}
                            className="bg-gradient-to-br from-purple-900/20 to-slate-900/50 border border-purple-500/30 rounded-2xl p-6 hover:border-purple-500/50 transition-colors group max-w-2xl mx-auto"
                        >
                            <div className="flex items-center gap-4 mb-4">
                                <div className="w-16 h-16 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 group-hover:bg-purple-500 group-hover:text-white transition-colors">
                                    <Building2 className="w-8 h-8" />
                                </div>
                                <div>
                                    <h3 className="text-2xl font-bold text-slate-100">{agent.name}</h3>
                                    <p className="text-sm text-purple-400 font-medium">{agent.role}</p>
                                </div>
                            </div>

                            <div className="space-y-3">
                                <p className="text-slate-300 text-base">{agent.background}</p>
                                <div className="flex flex-wrap gap-2 mt-4">
                                    {agent.traits.map((trait, j) => (
                                        <span key={j} className="text-xs bg-purple-900/30 text-purple-300 px-3 py-1.5 rounded-md border border-purple-700">
                                            {trait}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </div>
    );
}
