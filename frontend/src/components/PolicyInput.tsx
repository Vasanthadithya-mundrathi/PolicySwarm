import React, { useState, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Send, Upload, FileText, X } from 'lucide-react';
import axios from 'axios';

const API_URL = "http://localhost:8000";

interface PolicyInputProps {
    policy: string;
    setPolicy: (policy: string) => void;
    onSubmit: () => void;
    isRunning: boolean;
}

export default function PolicyInput({ policy, setPolicy, onSubmit, isRunning }: PolicyInputProps) {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [uploadLoading, setUploadLoading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.name.endsWith('.md') || file.name.endsWith('.txt')) {
                setSelectedFile(file);
                // Read file content
                const reader = new FileReader();
                reader.onload = (event) => {
                    if (event.target?.result) {
                        setPolicy(event.target.result as string);
                    }
                };
                reader.readAsText(file);
            } else {
                alert('Please upload a .md or .txt file');
            }
        }
    }, [setPolicy]);

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setSelectedFile(file);
            const reader = new FileReader();
            reader.onload = (event) => {
                if (event.target?.result) {
                    setPolicy(event.target.result as string);
                }
            };
            reader.readAsText(file);
        }
    };

    const handleFileUpload = async () => {
        if (!selectedFile) return;

        setUploadLoading(true);
        try {
            const content = await selectedFile.text();
            await axios.post(`${API_URL}/api/upload-policy`, null, {
                params: {
                    file: content,
                    filename: selectedFile.name
                }
            });
            alert(`Policy "${selectedFile.name}" uploaded and simulation started!`);
        } catch (e) {
            alert('Failed to upload file');
        }
        setUploadLoading(false);
    };

    const clearFile = () => {
        setSelectedFile(null);
        setPolicy('');
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6"
        >
            {/* File Drop Zone */}
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-xl p-6 mb-4 transition-all ${isDragging
                        ? 'border-blue-500 bg-blue-500/10'
                        : 'border-slate-700 hover:border-slate-600'
                    }`}
            >
                <div className="flex flex-col items-center text-center">
                    <Upload className={`w-8 h-8 mb-2 ${isDragging ? 'text-blue-400' : 'text-slate-500'}`} />
                    <p className="text-sm text-slate-400 mb-2">
                        Drag & drop a policy file here, or
                    </p>
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".md,.txt"
                        onChange={handleFileSelect}
                        className="hidden"
                    />
                    <button
                        onClick={() => fileInputRef.current?.click()}
                        className="text-sm text-blue-400 hover:text-blue-300 underline"
                    >
                        browse files
                    </button>
                    <p className="text-xs text-slate-600 mt-2">
                        Supports: .md, .txt files
                    </p>
                </div>
            </div>

            {/* Selected File Indicator */}
            {selectedFile && (
                <div className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-xl mb-4">
                    <FileText className="w-5 h-5 text-emerald-400" />
                    <span className="text-sm text-slate-300 flex-1">{selectedFile.name}</span>
                    <button
                        onClick={clearFile}
                        className="text-slate-500 hover:text-red-400"
                    >
                        <X className="w-4 h-4" />
                    </button>
                </div>
            )}

            {/* Text Input */}
            <div className="relative">
                <textarea
                    value={policy}
                    onChange={(e) => setPolicy(e.target.value)}
                    placeholder="Or type/paste your policy here...

Example: Replace property taxes with a flat-rate 'Community Charge' payable by every adult, regardless of income or property value."
                    className="w-full h-32 bg-slate-800/50 border border-slate-700 rounded-xl p-4 text-slate-200 placeholder-slate-500 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500"
                    disabled={isRunning}
                />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 mt-4">
                {selectedFile ? (
                    <button
                        onClick={handleFileUpload}
                        disabled={isRunning || uploadLoading}
                        className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-emerald-600 to-emerald-500 text-white font-bold py-3 px-6 rounded-xl hover:from-emerald-500 hover:to-emerald-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Upload className="w-5 h-5" />
                        {uploadLoading ? 'Uploading...' : 'Upload & Start Simulation'}
                    </button>
                ) : (
                    <button
                        onClick={onSubmit}
                        disabled={!policy || isRunning}
                        className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white font-bold py-3 px-6 rounded-xl hover:from-blue-500 hover:to-blue-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send className="w-5 h-5" />
                        {isRunning ? 'Running...' : 'Deploy to Swarm'}
                    </button>
                )}
            </div>
        </motion.div>
    );
}
