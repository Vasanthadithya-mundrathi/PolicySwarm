import React from 'react';
import { motion } from 'framer-motion';

export default function SenateView({ logs }: { logs: { agent: string, role: string, message: string, score?: number }[] }) {
    const observerLogs = logs.filter(l => l.role && (l.role.includes('Trend') || l.role.includes('Strategy') || l.role.includes('Ethics')));
    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-4 bg-slate-900/50 rounded-xl h-full overflow-y-auto custom-scrollbar">
            <h2 className="text-2xl font-bold text-slate-100 mb-4">Senate Analysis</h2>
            {observerLogs.length === 0 ? (
                <p className="text-slate-400">No analysis yet.</p>
            ) : (
                observerLogs.map((log, i) => (
                    <div key={i} className="mb-4 border-b border-slate-800 pb-2">
                        <h3 className="text-lg font-semibold text-blue-400">{log.agent} ({log.role})</h3>
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
