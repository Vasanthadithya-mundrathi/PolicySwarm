import React from 'react';
import { motion } from 'framer-motion';
import { Play, Pause, Download, RefreshCw, Check } from 'lucide-react';
import axios from 'axios';

const API_URL = "http://localhost:8000";

interface CycleControlProps {
    isRunning: boolean;
    isPaused: boolean;
    isComplete: boolean;
    currentIteration: number;
    onRefresh?: () => void;
}

export default function CycleControl({ isRunning, isPaused, isComplete, currentIteration, onRefresh }: CycleControlProps) {

    const handlePause = async () => {
        try {
            await axios.post(`${API_URL}/api/pause-cycle`);
            if (onRefresh) onRefresh();
        } catch (e) {
            console.error("Failed to pause");
        }
    };

    const handleContinue = async () => {
        try {
            await axios.post(`${API_URL}/api/continue-cycle`);
            if (onRefresh) onRefresh();
        } catch (e) {
            console.error("Failed to continue");
        }
    };

    const handleStopAndDownload = async () => {
        try {
            const res = await axios.post(`${API_URL}/api/stop-and-download`);
            // Trigger download
            const blob = new Blob([res.data.policy], { type: 'text/markdown' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'policy_final.md';
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            if (onRefresh) onRefresh();
        } catch (e) {
            console.error("Failed to download");
        }
    };

    const handleDownloadOnly = async () => {
        try {
            const res = await axios.get(`${API_URL}/api/download-policy`);
            const blob = new Blob([res.data], { type: 'text/markdown' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'policy_final.md';
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (e) {
            console.error("Failed to download");
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-slate-900/50 border border-slate-800 rounded-2xl p-4 mb-4"
        >
            <div className="flex items-center justify-between flex-wrap gap-4">
                {/* Status Indicator */}
                <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${isComplete ? 'bg-emerald-500' :
                            isPaused ? 'bg-amber-500' :
                                isRunning ? 'bg-blue-500 animate-pulse' :
                                    'bg-slate-500'
                        }`} />
                    <span className="text-sm text-slate-300">
                        {isComplete ? '✓ Consensus Reached' :
                            isPaused ? 'Paused' :
                                isRunning ? `Iteration ${currentIteration}/3 Running...` :
                                    'Ready'}
                    </span>
                </div>

                {/* Control Buttons */}
                <div className="flex gap-2">
                    {isRunning && !isPaused && !isComplete && (
                        <button
                            onClick={handlePause}
                            className="flex items-center gap-2 px-4 py-2 bg-amber-600/20 border border-amber-500/50 rounded-xl text-amber-400 hover:bg-amber-600/30 transition-colors"
                        >
                            <Pause className="w-4 h-4" />
                            Pause
                        </button>
                    )}

                    {isPaused && (
                        <>
                            <button
                                onClick={handleContinue}
                                className="flex items-center gap-2 px-4 py-2 bg-emerald-600/20 border border-emerald-500/50 rounded-xl text-emerald-400 hover:bg-emerald-600/30 transition-colors"
                            >
                                <Play className="w-4 h-4" />
                                Continue Cycle
                            </button>
                            <button
                                onClick={handleStopAndDownload}
                                className="flex items-center gap-2 px-4 py-2 bg-purple-600/20 border border-purple-500/50 rounded-xl text-purple-400 hover:bg-purple-600/30 transition-colors"
                            >
                                <Download className="w-4 h-4" />
                                Stop & Download
                            </button>
                        </>
                    )}

                    {isComplete && (
                        <button
                            onClick={handleDownloadOnly}
                            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-emerald-600/30 to-blue-600/30 border border-emerald-500/50 rounded-xl text-emerald-400 hover:from-emerald-600/40 hover:to-blue-600/40 transition-colors"
                        >
                            <Download className="w-4 h-4" />
                            Download Final Policy
                        </button>
                    )}
                </div>
            </div>

            {/* Iteration Progress */}
            {isRunning && (
                <div className="mt-4">
                    <div className="flex justify-between text-xs text-slate-500 mb-1">
                        <span>Progress</span>
                        <span>{currentIteration}/3 iterations</span>
                    </div>
                    <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${(currentIteration / 3) * 100}%` }}
                            className="h-full bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full"
                        />
                    </div>
                </div>
            )}
        </motion.div>
    );
}
