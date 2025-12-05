import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ShieldCheck, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

interface ReportPanelProps {
    report: string;
    isRunning: boolean;
}

export default function ReportPanel({ report, isRunning }: ReportPanelProps) {
    return (
        <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-8 h-full overflow-y-auto custom-scrollbar shadow-xl relative flex flex-col">
            <div className="flex items-center gap-3 mb-6 sticky top-0 bg-slate-900/90 backdrop-blur p-2 -mx-2 -mt-2 z-10 shrink-0">
                <ShieldCheck className="w-6 h-6 text-emerald-400" />
                <h2 className="text-xl font-bold text-emerald-100">Architect's Final Decree</h2>
            </div>

            {report ? (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="prose prose-invert prose-sm max-w-none flex-grow overflow-y-auto"
                >
                    <ReactMarkdown>{report}</ReactMarkdown>
                </motion.div>
            ) : (
                <div className="h-full flex flex-col items-center justify-center text-slate-600 gap-4">
                    <Activity className={`w-12 h-12 ${isRunning ? "animate-pulse text-purple-500" : "text-slate-800"}`} />
                    <p className="font-medium">{isRunning ? "Synthesizing Consensus..." : "Awaiting Simulation Data"}</p>
                </div>
            )}
        </div>
    );
}
