"use client";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Users, LayoutDashboard, Settings, Eye, Building2, HelpCircle, Play, Pause, Download } from 'lucide-react';
import DebateFeed from '@/components/DebateFeed';
import SenateChatFeed from '@/components/SenateChatFeed';
import ConsensusGraph from '@/components/ConsensusGraph';
import ReportPanel from '@/components/ReportPanel';
import PolicyInput from '@/components/PolicyInput';
import AgentsView from '@/components/AgentsView';
import SettingsView from '@/components/SettingsView';
import AboutView from '@/components/AboutView';

const API_URL = "http://localhost:8000";

type View = 'dashboard' | 'agents' | 'settings' | 'senate' | 'architect' | 'about';

export default function Home() {
  const [activeView, setActiveView] = useState<View>('dashboard');
  const [policy, setPolicy] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [currentIteration, setCurrentIteration] = useState(0);
  const [citizenLogs, setCitizenLogs] = useState<{ agent: string, role: string, message: string }[]>([]);
  const [senateLogs, setSenateLogs] = useState<{ agent: string, role: string, message: string }[]>([]);
  const [architectLogs, setArchitectLogs] = useState<{ agent: string, role: string, message: string }[]>([]);
  const [metrics, setMetrics] = useState<{ iteration: number, citizen_score: number, senate_score: number }[]>([]);
  const [report, setReport] = useState("");

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const [citizenRes, senateRes, architectRes, metricRes, reportRes, statusRes] = await Promise.all([
          axios.get(`${API_URL}/citizen-logs`),
          axios.get(`${API_URL}/senate-logs`),
          axios.get(`${API_URL}/architect-logs`),
          axios.get(`${API_URL}/metrics`),
          axios.get(`${API_URL}/report`),
          axios.get(`${API_URL}/status`)
        ]);

        setCitizenLogs(citizenRes.data);
        setSenateLogs(senateRes.data);
        setArchitectLogs(architectRes.data);
        setMetrics(metricRes.data);
        setCurrentIteration(statusRes.data.iteration);
        setIsPaused(statusRes.data.paused);
        setIsComplete(statusRes.data.complete);

        if (statusRes.data.iteration > 0 && !statusRes.data.complete) {
          setIsRunning(true);
        }

        if (reportRes.data.report) {
          setReport(reportRes.data.report);
          if (statusRes.data.complete) {
            setIsRunning(false);
          }
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
    setIsComplete(false);
    setCitizenLogs([]);
    setSenateLogs([]);
    setArchitectLogs([]);
    setMetrics([]);
    setReport("");
    try {
      await axios.post(`${API_URL}/api/submit-policy`, null, { params: { policy } });
    } catch (e) {
      alert("Failed to start simulation. Is backend running?");
      setIsRunning(false);
    }
  };

  const handlePause = async () => {
    await axios.post(`${API_URL}/api/pause-cycle`);
  };

  const handleContinue = async () => {
    await axios.post(`${API_URL}/api/continue-cycle`);
  };

  const handleDownload = async () => {
    try {
      const res = await axios.get(`${API_URL}/api/download-policy`, {
        responseType: 'blob'
      });
      const blob = new Blob([res.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'PolicySwarm_Report.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      alert("Download failed");
    }
  };

  const navItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { id: 'agents', icon: Users, label: 'Agents' },
    { id: 'senate', icon: Eye, label: 'Senate' },
    { id: 'architect', icon: Building2, label: 'Architect' },
    { id: 'settings', icon: Settings, label: 'Settings' },
    { id: 'about', icon: HelpCircle, label: 'About' },
  ];

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-200 font-sans">

      {/* Sidebar - Fixed Position */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 p-6 flex flex-col flex-shrink-0 fixed h-full hidden lg:flex z-20">
        <div className="mb-8">
          <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
            PolicySwarm
          </h1>
          <p className="text-xs text-slate-500 mt-1">v2.0 - Recursive Consensus</p>
        </div>

        <nav className="space-y-2 flex-1">
          {navItems.map(({ id, icon: Icon, label }) => (
            <button
              key={id}
              onClick={() => setActiveView(id as View)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${activeView === id
                ? "bg-blue-600/20 text-blue-400 border border-blue-600/30"
                : "text-slate-400 hover:bg-slate-800"
                }`}
            >
              <Icon className="w-5 h-5" /> {label}
            </button>
          ))}
        </nav>

        <div className="pt-4 border-t border-slate-800 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isComplete ? 'bg-emerald-500' : isRunning ? 'bg-blue-500 animate-pulse' : 'bg-slate-600'}`} />
            {isComplete ? '✓ Complete' : isRunning ? `Iteration ${currentIteration}/3` : 'Ready'}
          </div>
        </div>
      </aside>

      {/* Main Content - Scrollable with margin for sidebar */}
      <main className="flex-1 lg:ml-64 min-h-screen overflow-y-auto">
        <div className="p-6 max-w-6xl mx-auto pb-20">

          {activeView === 'dashboard' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-slate-100">Policy Dashboard</h2>

              {/* CYCLE CONTROL BAR */}
              <div className="bg-slate-900/90 border border-slate-700 rounded-2xl p-4 backdrop-blur-sm">
                <div className="flex items-center justify-between flex-wrap gap-4">
                  <div className="flex items-center gap-3">
                    <div className={`w-4 h-4 rounded-full ${isComplete ? 'bg-emerald-500' :
                      isPaused ? 'bg-amber-500' :
                        isRunning ? 'bg-blue-500 animate-pulse' :
                          'bg-slate-600'
                      }`} />
                    <span className="font-medium">
                      {isComplete ? '✓ Consensus Reached' :
                        isPaused ? '⏸ Paused' :
                          isRunning ? `🔄 Iteration ${currentIteration}/3 Running...` :
                            '⏹ Ready to Start'}
                    </span>
                    {metrics.length > 0 && (
                      <span className="text-sm text-slate-400 ml-4">
                        Last: Citizen {metrics[metrics.length - 1]?.citizen_score}%, Senate {metrics[metrics.length - 1]?.senate_score}%
                      </span>
                    )}
                  </div>

                  <div className="flex gap-3">
                    {isRunning && !isPaused && !isComplete && (
                      <button onClick={handlePause} className="flex items-center gap-2 px-4 py-2 bg-amber-600/20 border border-amber-500/50 rounded-xl text-amber-400 hover:bg-amber-600/30 transition-colors">
                        <Pause className="w-4 h-4" /> Pause
                      </button>
                    )}

                    {isPaused && (
                      <button onClick={handleContinue} className="flex items-center gap-2 px-4 py-2 bg-emerald-600/20 border border-emerald-500/50 rounded-xl text-emerald-400 hover:bg-emerald-600/30 transition-colors">
                        <Play className="w-4 h-4" /> Continue
                      </button>
                    )}

                    {(isComplete || metrics.length > 0) && (
                      <button onClick={handleDownload} className="flex items-center gap-2 px-4 py-2 bg-purple-600/20 border border-purple-500/50 rounded-xl text-purple-400 hover:bg-purple-600/30 transition-colors">
                        <Download className="w-4 h-4" /> Download Policy
                      </button>
                    )}
                  </div>
                </div>

                {isRunning && (
                  <div className="mt-3">
                    <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full transition-all duration-500"
                        style={{ width: `${(currentIteration / 3) * 100}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Policy Input */}
              <PolicyInput policy={policy} setPolicy={setPolicy} onSubmit={handleSubmit} isRunning={isRunning} />

              {/* Split View: Citizens + Senate - Fixed Heights */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-bold text-blue-400 mb-3 flex items-center gap-2">
                    <Users className="w-5 h-5" /> Citizen Debate ({citizenLogs.length} msgs)
                  </h3>
                  <div className="h-80 overflow-hidden">
                    <DebateFeed logs={citizenLogs} />
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-emerald-400 mb-3 flex items-center gap-2">
                    <Eye className="w-5 h-5" /> Senate Debate ({senateLogs.length} msgs)
                  </h3>
                  <div className="h-80 overflow-hidden">
                    <SenateChatFeed logs={senateLogs} />
                  </div>
                </div>
              </div>

              {/* Graph + Report */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-bold text-slate-300 mb-3">Consensus Progress</h3>
                  <div className="h-64 bg-slate-900/50 border border-slate-800 rounded-2xl p-4">
                    <ConsensusGraph data={metrics} />
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-300 mb-3">Architect Report</h3>
                  <div className="h-64 bg-slate-900/50 border border-slate-800 rounded-2xl p-4 overflow-y-auto">
                    <ReportPanel report={report} />
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeView === 'agents' && (
            <div>
              <h2 className="text-3xl font-bold text-slate-100 mb-8">Agent Directory</h2>
              <AgentsView />
            </div>
          )}

          {activeView === 'senate' && (
            <div className="space-y-4">
              <h2 className="text-3xl font-bold text-emerald-400 flex items-center gap-3">
                <Eye className="w-8 h-8" /> Senate Strategic Debate
              </h2>
              <p className="text-slate-400">Real-time strategic discussion between government advisors.</p>
              <div className="h-[70vh]">
                <SenateChatFeed logs={senateLogs} />
              </div>
            </div>
          )}

          {activeView === 'architect' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold text-purple-400 flex items-center gap-3">
                <Building2 className="w-8 h-8" /> Architect Analysis
              </h2>

              <div className="bg-purple-900/20 border border-purple-500/30 rounded-2xl p-6">
                <h3 className="text-xl font-bold text-purple-400 mb-4">📊 Analysis Steps</h3>
                {architectLogs.length === 0 ? (
                  <p className="text-slate-500">Analysis will appear during simulation...</p>
                ) : (
                  <div className="space-y-3 max-h-72 overflow-y-auto">
                    {architectLogs.map((log, i) => (
                      <div key={i} className="p-3 bg-slate-900/50 rounded-lg border-l-4 border-purple-500">
                        <div className="text-xs text-purple-400 font-mono mb-1">{log.role}</div>
                        <div className="text-sm text-slate-300">{log.message}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
                <h3 className="text-xl font-bold text-slate-300 mb-4">📄 Policy Report</h3>
                <div className="max-h-96 overflow-y-auto">
                  <ReportPanel report={report} />
                </div>
              </div>
            </div>
          )}

          {activeView === 'settings' && (
            <div>
              <h2 className="text-3xl font-bold text-slate-100 mb-8">Settings</h2>
              <SettingsView />
            </div>
          )}

          {activeView === 'about' && <AboutView />}
        </div>
      </main>
    </div>
  );
}
