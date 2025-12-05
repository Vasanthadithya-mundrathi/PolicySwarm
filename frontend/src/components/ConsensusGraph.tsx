import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, ReferenceLine } from 'recharts';
import { TrendingUp } from 'lucide-react';

interface Metric {
    iteration: number;
    citizen_score: number;
    senate_score: number;
}

interface ConsensusGraphProps {
    data: Metric[];
}

export default function ConsensusGraph({ data }: ConsensusGraphProps) {
    // Add placeholder data if empty to show targets
    const displayData = data.length > 0 ? data : [
        { iteration: 0, citizen_score: 0, senate_score: 0 }
    ];

    return (
        <div className="h-full w-full flex flex-col">
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-purple-400" />
                    <span className="text-sm font-bold text-slate-300">Consensus Trajectory</span>
                </div>
                <div className="flex gap-4 text-xs">
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-0.5 bg-blue-400 rounded"></span>
                        <span className="text-slate-400">Citizens (Target: 75%)</span>
                    </span>
                    <span className="flex items-center gap-1">
                        <span className="w-3 h-0.5 bg-emerald-400 rounded"></span>
                        <span className="text-slate-400">Senate (Target: 80%)</span>
                    </span>
                </div>
            </div>
            <div className="flex-1 min-h-0">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={displayData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis
                            dataKey="iteration"
                            stroke="#94a3b8"
                            tickFormatter={(v) => `R${v}`}
                            fontSize={12}
                        />
                        <YAxis domain={[0, 100]} stroke="#94a3b8" fontSize={12} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                            itemStyle={{ color: '#e2e8f0' }}
                            labelFormatter={(v) => `Iteration ${v}`}
                        />
                        {/* Target lines */}
                        <ReferenceLine y={75} stroke="#60a5fa" strokeDasharray="5 5" strokeOpacity={0.5} />
                        <ReferenceLine y={80} stroke="#34d399" strokeDasharray="5 5" strokeOpacity={0.5} />
                        <Line
                            type="monotone"
                            dataKey="citizen_score"
                            name="Citizen %"
                            stroke="#60a5fa"
                            strokeWidth={3}
                            dot={{ r: 6, fill: '#60a5fa' }}
                            activeDot={{ r: 8 }}
                            isAnimationActive={true}
                        />
                        <Line
                            type="monotone"
                            dataKey="senate_score"
                            name="Senate %"
                            stroke="#34d399"
                            strokeWidth={3}
                            dot={{ r: 6, fill: '#34d399' }}
                            activeDot={{ r: 8 }}
                            isAnimationActive={true}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
            {data.length === 0 && (
                <div className="text-center text-xs text-slate-500 mt-2">
                    Graph updates after each iteration completes
                </div>
            )}
        </div>
    );
}
