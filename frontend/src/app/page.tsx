"use client";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Users, LayoutDashboard, Settings, LogOut, HelpCircle } from 'lucide-react';
import DebateFeed from '@/components/DebateFeed';
import ConsensusGraph from '@/components/ConsensusGraph';
import ReportPanel from '@/components/ReportPanel';
import PolicyInput from '@/components/PolicyInput';
import AgentsView from '@/components/AgentsView';
import SettingsView from '@/components/SettingsView';
import SenateView from '@/components/SenateView';
import ArchitectView from '@/components/ArchitectView';
import AboutView from '@/components/AboutView';

const API_URL = "http://localhost:8000";

type View = 'dashboard' | 'agents' | 'settings' | 'senate' | 'architect' | 'about';

export default function Home() {
  const [activeView, setActiveView] = useState<View>('dashboard');
  const [policy, setPolicy] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<{ agent: string, role: string, message: string }[]>([]);
  const [metrics, setMetrics] = useState<{ iteration: number, citizen_score: number, senate_score: number }[]>([]);
  const [report, setReport] = useState("");

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const [logRes, metricRes, reportRes] = await Promise.all([
          axios.get(`${API_URL}/logs`),
          axios.get(`${API_URL}/metrics`),
          axios.get(`${API_URL}/report`)
        ]);

        setLogs(logRes.data);
        setMetrics(metricRes.data);

        if (reportRes.data.report) {
          setReport(reportRes.data.report);
          setIsRunning(false);
        }
      } catch (e) {
        console.error("Polling error", e);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async () => {
    if (!policy) return;
    setIsRunning(true);
    setLogs([]);
    setMetrics([]);
    setReport("");
    try {
      await axios.post(`${API_URL}/api/submit-policy`, null, { params: { policy } });
    } catch (e) {
      alert("Failed to start simulation. Is backend running?");
      setIsRunning(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 font-sans selection:bg-blue-500/30 overflow-hidden">

      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 p-6 flex flex-col hidden lg:flex">
        <div className="mb-10">
          <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight">
            PolicySwarm
          </h1>
          <p className="text-xs text-slate-500 mt-1">Recursive Consensus Engine</p>
        </div>

        <nav className="space-y-2 flex-1">
          <button
            onClick={() => setActiveView('dashboard')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${activeView === 'dashboard'
              ? "bg-blue-600/10 text-blue-400 border border-blue-600/20"
              : "text-slate-400 hover:bg-slate-800"
              }`}
          >
            <LayoutDashboard className="w-5 h-5" />
            Dashboard
          </button>
          <button
            onClick={() => setActiveView('agents')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${activeView === 'agents'
              ? "bg-blue-600/10 text-blue-400 border border-blue-600/20"
              : "text-slate-400 hover:bg-slate-800"
              }`}
          >
            <Users className="w-5 h-5" />
            Agents
          </button>
          <button
            onClick={() => setActiveView('settings')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${activeView === 'settings'
              ? "bg-blue-600/10 text-blue-400 border border-blue-600/20"
              : "text-slate-400 hover:bg-slate-800"
              }`}
          >
            <Settings className="w-5 h-5" />
            Settings
          </button>
          <button
            onClick={() => setActiveView('senate')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${activeView === 'senate' ? "bg-blue-600/10 text-blue-400 border border-blue-600/20" : "text-slate-400 hover:bg-slate-800"}`}
          >
            <Users className="w-5 h-5" /> Senate
          </button>
          <button
            onClick={() => setActiveView('architect')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${activeView === 'architect' ? "bg-blue-600/10 text-blue-400 border border-blue-600/20" : "text-slate-400 hover:bg-slate-800"}`}
          >
            <LayoutDashboard className="w-5 h-5" /> Architect
          </button>
          <button
            onClick={() => setActiveView('about')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${activeView === 'about' ? "bg-blue-600/10 text-blue-400 border border-blue-600/20" : "text-slate-400 hover:bg-slate-800"}`}
          >
            <HelpCircle className="w-5 h-5" /> About
          </button>
        </nav>

        <button className="flex items-center gap-3 px-4 py-3 text-slate-500 hover:text-red-400 transition-colors mt-auto">
          <LogOut className="w-5 h-5" />
          Disconnect
        </button>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-hidden relative">
        {/* Background Glow */}
        <div className="absolute top-0 left-0 w-full h-96 bg-blue-500/5 blur-[120px] pointer-events-none" />

        {/* Fixed Header Section (Dashboard Only) */}
        {activeView === 'dashboard' && (
          <div className="p-8 pb-0 shrink-0 z-10">
            <div className="max-w-3xl mx-auto text-center">
              <motion.h2
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-3xl font-bold text-slate-100 mb-6"
              >
                Deploy a Policy for Consensus
              </motion.h2>
              <PolicyInput
                policy={policy}
                setPolicy={setPolicy}
                handleSubmit={handleSubmit}
                isRunning={isRunning}
              />
            </div>
          </div>
        )}

        {/* Scrollable Content Area */}
        <div className="flex-1 overflow-y-auto p-8 custom-scrollbar min-h-0">
          <div className="max-w-[1600px] mx-auto h-full">

            {activeView === 'dashboard' && (
              /* Dashboard Grid - Takes full remaining height */
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-full min-h-[600px]">

                {/* Left Column: Debate Feed */}
                <div className="lg:col-span-5 flex flex-col h-full min-h-0">
                  <div className="flex items-center justify-between mb-4 shrink-0">
                    <h3 className="text-lg font-semibold text-slate-300 flex items-center gap-2">
                      <Users className="w-5 h-5 text-blue-400" />
                      Live Swarm Debate
                    </h3>
                    <span className="text-xs bg-blue-500/10 text-blue-400 px-2 py-1 rounded-full border border-blue-500/20">
                      {logs.length} Events
                    </span>
                  </div>
                  <div className="flex-1 min-h-0 relative">
                    {/* Absolute positioning to ensure scroll works within flex item */}
                    <div className="absolute inset-0">
                      <DebateFeed logs={logs} />
                    </div>
                  </div>
                </div>

                {/* Right Column: Metrics & Report */}
                <div className="lg:col-span-7 flex flex-col gap-6 h-full min-h-0">

                  {/* Top: Graph */}
                  <div className="h-[300px] shrink-0">
                    <ConsensusGraph metrics={metrics} />
                  </div>

                  {/* Bottom: Report */}
                  <div className="flex-1 min-h-0 flex flex-col">
                    <ReportPanel report={report} isRunning={isRunning} />
                  </div>

                </div>
              </div>
            )}

            {activeView === 'agents' && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-3xl font-bold text-slate-100 mb-8">Active Citizen Personas</h2>
                <AgentsView />
              </motion.div>
            )}

            {activeView === 'settings' && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-3xl font-bold text-slate-100 mb-8">System Settings</h2>
                <SettingsView />
              </motion.div>
            )}

            {activeView === 'senate' && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-3xl font-bold text-slate-100 mb-8">Senate Analysis</h2>
                <SenateView logs={logs} />
              </motion.div>
            )}

            {activeView === 'architect' && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-3xl font-bold text-slate-100 mb-8">Architect Synthesis</h2>
                <ArchitectView logs={logs} />
              </motion.div>
            )}

            {activeView === 'about' && (
              <AboutView />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
