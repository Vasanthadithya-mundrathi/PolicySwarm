import React from 'react';
import { motion } from 'framer-motion';
import { Send } from 'lucide-react';

interface PolicyInputProps {
    policy: string;
    setPolicy: (policy: string) => void;
    handleSubmit: () => void;
    isRunning: boolean;
}

export default function PolicyInput({ policy, setPolicy, handleSubmit, isRunning }: PolicyInputProps) {
    return (
        <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="max-w-3xl mx-auto mb-8 flex gap-4 relative z-10"
        >
            <input
                type="text"
                value={policy}
                onChange={(e) => setPolicy(e.target.value)}
                placeholder="Enter a controversial policy..."
                className="flex-1 bg-slate-900/80 backdrop-blur-md border border-slate-700 rounded-2xl p-5 text-lg focus:ring-2 focus:ring-blue-500 outline-none shadow-xl transition-all"
                disabled={isRunning}
            />
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSubmit}
                disabled={isRunning || !policy}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 rounded-2xl font-bold flex items-center gap-2 shadow-lg shadow-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
            >
                <Send className="w-5 h-5" />
                {isRunning ? "Swarm Active" : "Deploy"}
            </motion.button>
        </motion.div>
    );
}
