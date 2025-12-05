import React from 'react';
import { motion } from 'framer-motion';
import { Book, Github, FileText, Zap, Users, Eye, Building2, HelpCircle } from 'lucide-react';

export default function AboutView() {
    return (
        <div className="max-w-4xl mx-auto p-6 space-y-8">
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center"
            >
                <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 mb-4">
                    PolicySwarm
                </h1>
                <p className="text-xl text-slate-300">Recursive Consensus Engine for Policy Testing</p>
            </motion.div>

            {/* What is PolicySwarm */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6"
            >
                <h2 className="text-2xl font-bold text-slate-100 mb-4 flex items-center gap-2">
                    <Book className="w-6 h-6 text-blue-400" />
                    What is PolicySwarm?
                </h2>
                <p className="text-slate-300 leading-relaxed mb-4">
                    PolicySwarm is an AI-powered multi-agent simulation that stress-tests government policies
                    before they are released to the public. Using a <strong>3-level recursive consensus engine</strong>,
                    the system iteratively refines policies through democratic debate until they meet both citizen
                    satisfaction and government viability thresholds.
                </p>
                <p className="text-slate-300 leading-relaxed">
                    Powered by <strong>local AI</strong> (Ollama with Gemma 3 12B), PolicySwarm ensures complete
                    privacy and zero API costs while delivering realistic policy analysis through genuine
                    conversational debate between AI agents.
                </p>
            </motion.div>

            {/* How It Works */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6"
            >
                <h2 className="text-2xl font-bold text-slate-100 mb-6 flex items-center gap-2">
                    <Zap className="w-6 h-6 text-amber-400" />
                    How It Works: 3-Level Architecture
                </h2>

                <div className="space-y-6">
                    {/* Level 1 */}
                    <div className="flex gap-4">
                        <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 shrink-0">
                            <Users className="w-6 h-6" />
                        </div>
                        <div>
                            <h3 className="text-lg font-bold text-blue-400 mb-2">Level 1: Citizen Swarm</h3>
                            <p className="text-slate-300 text-sm leading-relaxed">
                                10 AI agents with realistic UK personas (e.g., Single Mom, Gig Worker, CEO, Farmer)
                                engage in <strong>100 conversational exchanges</strong>. Agents respond to each other
                                naturally, reference specific points, and can exit the conversation when appropriate.
                            </p>
                            <p className="text-slate-400 text-xs mt-2">
                                Output: Citizen Satisfaction Score (0-100%)
                            </p>
                        </div>
                    </div>

                    {/* Level 2 */}
                    <div className="flex gap-4">
                        <div className="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
                            <Eye className="w-6 h-6" />
                        </div>
                        <div>
                            <h3 className="text-lg font-bold text-emerald-400 mb-2">Level 2: Senate Strategic Debate</h3>
                            <p className="text-slate-300 text-sm leading-relaxed">
                                3 observer agents (Trend Watcher, Strategy Lead, Ethics Guardian) analyze the full citizen
                                conversation, then engage in <strong>10 strategic exchanges</strong> debating implementation
                                risks and viability from a government perspective.
                            </p>
                            <p className="text-slate-400 text-xs mt-2">
                                Output: Senate Viability Score (0-100%)
                            </p>
                        </div>
                    </div>

                    {/* Level 3 */}
                    <div className="flex gap-4">
                        <div className="w-12 h-12 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 shrink-0">
                            <Building2 className="w-6 h-6" />
                        </div>
                        <div>
                            <h3 className="text-lg font-bold text-purple-400 mb-2">Level 3: Architect Synthesis</h3>
                            <p className="text-slate-300 text-sm leading-relaxed">
                                The Chief Architect synthesizes feedback from both citizens and Senate, then rewrites
                                the policy to address concerns. The revised policy is fed back to Level 1 for another
                                iteration.
                            </p>
                            <p className="text-slate-400 text-xs mt-2">
                                Output: Revised Policy → Loops back to Level 1
                            </p>
                        </div>
                    </div>
                </div>

                <div className="mt-6 p-4 bg-blue-900/20 border border-blue-500/30 rounded-xl">
                    <p className="text-sm text-blue-300">
                        <strong>Consensus Criteria:</strong> The loop repeats until <strong>Citizen Satisfaction {">"} 75%</strong> AND
                        <strong> Senate Viability {">"} 80%</strong>, or a maximum of 3 iterations is reached.
                    </p>
                </div>
            </motion.div>

            {/* Key Features */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6"
            >
                <h2 className="text-2xl font-bold text-slate-100 mb-4">Key Features</h2>
                <ul className="space-y-3 text-slate-300">
                    <li className="flex items-start gap-3">
                        <span className="text-emerald-400 mt-1">✓</span>
                        <span><strong>Real AI Conversations:</strong> 110+ LLM-generated exchanges per iteration (not scripted)</span>
                    </li>
                    <li className="flex items-start gap-3">
                        <span className="text-emerald-400 mt-1">✓</span>
                        <span><strong>Contextual Understanding:</strong> Agents reference each other's specific points</span>
                    </li>
                    <li className="flex items-start gap-3">
                        <span className="text-emerald-400 mt-1">✓</span>
                        <span><strong>Natural Behavior:</strong> Agents can exit conversations appropriately</span>
                    </li>
                    <li className="flex items-start gap-3">
                        <span className="text-emerald-400 mt-1">✓</span>
                        <span><strong>Fast Demo Mode:</strong> 5-10 min simulations for quick testing</span>
                    </li>
                    <li className="flex items-start gap-3">
                        <span className="text-emerald-400 mt-1">✓</span>
                        <span><strong>Local & Private:</strong> Runs on Ollama - zero API costs, full privacy</span>
                    </li>
                    <li className="flex items-start gap-3">
                        <span className="text-emerald-400 mt-1">✓</span>
                        <span><strong>Iterative Refinement:</strong> Policies genuinely improve across iterations</span>
                    </li>
                </ul>
            </motion.div>

            {/* Resources */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6"
            >
                <h2 className="text-2xl font-bold text-slate-100 mb-4 flex items-center gap-2">
                    <FileText className="w-6 h-6 text-purple-400" />
                    Documentation & Resources
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <a
                        href="https://github.com/YOUR_USERNAME/policyswarm"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 p-4 bg-slate-800/50 rounded-xl border border-slate-700 hover:border-purple-500/50 transition-colors group"
                    >
                        <Github className="w-6 h-6 text-purple-400 group-hover:text-purple-300" />
                        <div>
                            <h3 className="font-bold text-slate-200">GitHub Repository</h3>
                            <p className="text-xs text-slate-400">Source code & contributions</p>
                        </div>
                    </a>

                    <div className="flex items-center gap-3 p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                        <FileText className="w-6 h-6 text-blue-400" />
                        <div>
                            <h3 className="font-bold text-slate-200">Setup Guide</h3>
                            <p className="text-xs text-slate-400">See SETUP.md in project root</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3 p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                        <Book className="w-6 h-6 text-emerald-400" />
                        <div>
                            <h3 className="font-bold text-slate-200">Walkthrough</h3>
                            <p className="text-xs text-slate-400">See walkthrough.md for detailed guide</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3 p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                        <HelpCircle className="w-6 h-6 text-amber-400" />
                        <div>
                            <h3 className="font-bold text-slate-200">Get Help</h3>
                            <p className="text-xs text-slate-400">Check README.md for support</p>
                        </div>
                    </div>
                </div>
            </motion.div>

            {/* Quick Start */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="bg-gradient-to-br from-blue-900/20 to-emerald-900/20 border border-blue-500/30 rounded-2xl p-6"
            >
                <h2 className="text-2xl font-bold text-slate-100 mb-4">Quick Start Testing</h2>
                <ol className="space-y-3 text-slate-300">
                    <li><strong>1.</strong> Navigate to <span className="text-blue-400">Settings</span> and toggle <strong>Fast Demo Mode</strong> ON</li>
                    <li><strong>2.</strong> Go to <span className="text-blue-400">Dashboard</span> and enter a policy (or use the sample Poll Tax policy)</li>
                    <li><strong>3.</strong> Click <strong>"Deploy to Swarm"</strong> and watch the simulation</li>
                    <li><strong>4.</strong> Navigate between <span className="text-blue-400">Senate</span> and <span className="text-blue-400">Architect</span> views to see all 3 levels</li>
                    <li><strong>5.</strong> Review the final report after consensus is reached!</li>
                </ol>
            </motion.div>

            {/* Footer */}
            <div className="text-center text-slate-500 text-sm">
                <p>Built with Next.js, FastAPI, and Ollama</p>
                <p className="mt-2">© 2025 PolicySwarm | Open Source</p>
            </div>
        </div>
    );
}
