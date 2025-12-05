import React from 'react';
import { motion } from 'framer-motion';

export default function ArchitectView({ logs }: { logs: { agent: string, role: string, message: string, score?: number }[] }) {
    const architectLogs = logs.filter(l => l.role && l.role.toLowerCase().includes('architect'));
    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-4 bg-slate-900/50 rounded-xl h-full overflow-y-auto custom-scrollbar">
            <h2 className="text-2xl font-bold text-slate-100 mb-4">Architect Synthesis</h2>
            {architectLogs.length === 0 ? (
                <p className="text-slate-400">No architect output yet.</p>
            ) : (
                architectLogs.map((log, i) => (
                    <div key={i} className="mb-4 border-b border-slate-800 pb-2">
                        <h3 className="text-lg font-semibold text-emerald-400">{log.agent}</h3>
                        <p className="text-slate-200">{log.message}</p>
                        {log.score !== undefined && (
                            <span className="text-xs text-slate-500">Score: {log.score}</span>
                        )}
                    </div>
                ))
            )}
        </motion.div>
    );
}
