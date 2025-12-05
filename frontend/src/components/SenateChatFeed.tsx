import React, { useRef, useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Eye } from 'lucide-react';

interface SenateMessage {
    agent: string;
    role: string;
    message: string;
}

interface SenateChatFeedProps {
    logs: SenateMessage[];
}

export default function SenateChatFeed({ logs }: SenateChatFeedProps) {
    const containerRef = useRef<HTMLDivElement>(null);
    const [autoScroll, setAutoScroll] = useState(true);
    const prevLogsLength = useRef(logs.length);

    const handleScroll = () => {
        if (!containerRef.current) return;
        const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
        const isAtBottom = scrollHeight - scrollTop - clientHeight < 50;
        setAutoScroll(isAtBottom);
    };

    // Auto-scroll only within the container (not affecting page scroll)
    useEffect(() => {
        if (autoScroll && containerRef.current && logs.length > prevLogsLength.current) {
            // Use scrollTop instead of scrollIntoView to avoid hijacking page scroll
            containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
        prevLogsLength.current = logs.length;
    }, [logs, autoScroll]);

    return (
        <div
            ref={containerRef}
            onScroll={handleScroll}
            className="bg-slate-900/50 border border-emerald-500/30 rounded-2xl p-4 h-full overflow-y-auto custom-scrollbar relative"
        >
            <AnimatePresence mode='popLayout'>
                {logs.filter(l => l.agent !== "System").map((log, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.2 }}
                        className="mb-3"
                    >
                        <div className="p-3 rounded-xl bg-emerald-900/20 border border-emerald-500/30">
                            <div className="flex items-center gap-2 mb-1">
                                <Eye className="w-4 h-4 text-emerald-400" />
                                <span className="font-bold text-sm text-emerald-400">
                                    {log.agent}
                                </span>
                                <span className="text-[10px] text-slate-500 uppercase tracking-wider">
                                    {log.role}
                                </span>
                            </div>
                            <p className="text-slate-300 text-sm leading-relaxed">{log.message}</p>
                        </div>
                    </motion.div>
                ))}
            </AnimatePresence>

            {logs.filter(l => l.agent !== "System").length === 0 && (
                <div className="h-full flex items-center justify-center text-slate-500 text-sm">
                    <Eye className="w-6 h-6 mr-2 opacity-50" />
                    Senate debate will appear here...
                </div>
            )}
        </div>
    );
}
