import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ShieldCheck, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

interface ReportPanelProps {
    report: string;
}

export default function ReportPanel({ report }: ReportPanelProps) {
    return (
        <div className="h-full overflow-y-auto custom-scrollbar">
            {report ? (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="prose prose-invert prose-sm max-w-none 
                        prose-headings:text-emerald-400 prose-headings:font-bold prose-headings:border-b prose-headings:border-slate-700 prose-headings:pb-2 prose-headings:mb-4
                        prose-h1:text-2xl prose-h1:text-purple-400
                        prose-h2:text-xl prose-h2:text-emerald-400
                        prose-h3:text-lg prose-h3:text-blue-400
                        prose-p:text-slate-300 prose-p:leading-relaxed
                        prose-ul:text-slate-300
                        prose-li:marker:text-emerald-500
                        prose-strong:text-white
                        prose-code:bg-slate-800 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-code:text-amber-400
                        prose-pre:bg-slate-900 prose-pre:border prose-pre:border-slate-700"
                >
                    <ReactMarkdown>{report}</ReactMarkdown>
                </motion.div>
            ) : (
                <div className="h-full flex flex-col items-center justify-center text-slate-600 gap-4">
                    <Activity className="w-12 h-12 text-slate-700" />
                    <p className="font-medium text-sm">Awaiting analysis...</p>
                </div>
            )}
        </div>
    );
}
