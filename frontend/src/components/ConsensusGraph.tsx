import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp } from 'lucide-react';

interface Metric {
    iteration: number;
    citizen_score: number;
    senate_score: number;
}

interface ConsensusGraphProps {
    metrics: Metric[];
}

export default function ConsensusGraph({ metrics }: ConsensusGraphProps) {
    return (
        <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 h-[300px] shadow-xl flex flex-col">
            <div className="flex items-center gap-3 mb-4">
                <TrendingUp className="w-6 h-6 text-purple-400" />
                <h2 className="text-xl font-bold text-purple-100">Consensus Trajectory</h2>
            </div>
            <div className="flex-1 w-full min-h-0">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={metrics}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="iteration" stroke="#94a3b8" label={{ value: 'Iteration', position: 'insideBottom', offset: -5 }} />
                        <YAxis domain={[0, 100]} stroke="#94a3b8" />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                            itemStyle={{ color: '#e2e8f0' }}
                        />
                        <Line type="monotone" dataKey="citizen_score" name="Citizen Satisfaction" stroke="#60a5fa" strokeWidth={3} dot={{ r: 6 }} activeDot={{ r: 8 }} />
                        <Line type="monotone" dataKey="senate_score" name="Gov Viability" stroke="#34d399" strokeWidth={3} dot={{ r: 6 }} activeDot={{ r: 8 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
