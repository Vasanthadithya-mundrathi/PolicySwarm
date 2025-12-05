import React, { useRef, useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Log {
    agent: string;
    role: string;
    message: string;
}

interface DebateFeedProps {
    logs: Log[];
}

export default function DebateFeed({ logs }: DebateFeedProps) {
    const logsEndRef = useRef<HTMLDivElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);
    const [autoScroll, setAutoScroll] = useState(true);

    // Detect user scroll
    const handleScroll = () => {
        if (!containerRef.current) return;
        const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
        const isAtBottom = scrollHeight - scrollTop - clientHeight < 50;
        setAutoScroll(isAtBottom);
    };

    // Auto-scroll only if user hasn't manually scrolled up
    useEffect(() => {
        if (autoScroll) {
            logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
        }
    }, [logs, autoScroll]);

    return (
        <div
            ref={containerRef}
            onScroll={handleScroll}
            className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 h-full overflow-y-auto custom-scrollbar relative shadow-inner"
        >
            <AnimatePresence mode='popLayout'>
                {logs.filter(l => l.role !== "System").map((log, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, x: log.role.includes("Guardian") ? 50 : -50, scale: 0.8 }}
                        animate={{ opacity: 1, x: 0, scale: 1 }}
                        layout
                        className={`flex flex-col mb-4 ${["Trend Watcher", "Strategy Lead", "Ethics Guardian"].includes(log.agent)
                            ? "items-end"
                            : "items-start"
                            }`}
                    >
                        <div className={`max-w-[85%] p-4 rounded-2xl shadow-lg backdrop-blur-sm ${["Trend Watcher", "Strategy Lead", "Ethics Guardian"].includes(log.agent)
                            ? "bg-emerald-900/20 border border-emerald-500/30 rounded-tr-none"
                            : "bg-blue-900/20 border border-blue-500/30 rounded-tl-none"
                            }`}>
                            <div className="flex items-center gap-2 mb-2">
                                <span className={`font-bold text-sm ${["Trend Watcher", "Strategy Lead", "Ethics Guardian"].includes(log.agent)
                                    ? "text-emerald-400"
                                    : "text-blue-400"
                                    }`}>
                                    {log.agent}
                                </span>
                                <span className="text-[10px] text-slate-500 uppercase tracking-wider border border-slate-700 px-1.5 py-0.5 rounded">
                                    {log.role}
                                </span>
                            </div>
                            <p className="text-slate-300 text-sm leading-relaxed">{log.message}</p>
                        </div>
                    </motion.div>
                ))}
            </AnimatePresence>
            <div ref={logsEndRef} />
        </div>
    );
}
