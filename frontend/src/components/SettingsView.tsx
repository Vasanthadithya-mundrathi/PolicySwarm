import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Moon, Sun, Globe, Server, Zap, Upload } from 'lucide-react';
import axios from 'axios';

const API_URL = "http://localhost:8000";

export default function SettingsView() {
    const [fastDemo, setFastDemo] = useState(false);
    const [loading, setLoading] = useState(false);
    const [uploadFile, setUploadFile] = useState<File | null>(null);

    useEffect(() => {
        // Fetch current config on mount
        axios.get(`${API_URL}/config`)
            .then(res => setFastDemo(res.data.fast_demo))
            .catch(err => console.error(err));
    }, []);

    const toggleFastDemo = async () => {
        setLoading(true);
        try {
            await axios.post(`${API_URL}/config`, null, { params: { fast_demo: !fastDemo } });
            setFastDemo(!fastDemo);
        } catch (e) {
            alert("Failed to update config");
        }
        setLoading(false);
    };

    const handleFileUpload = async () => {
        if (!uploadFile) return;
        setLoading(true);
        try {
            const formData = new FormData();
            formData.append('file', uploadFile);
            const content = await uploadFile.text();
            await axios.post(`${API_URL}/api/upload-policy`, null, {
                params: {
                    file: content,
                    filename: uploadFile.name
                }
            });
            alert(`Policy file "${uploadFile.name}" uploaded successfully!`);
        } catch (e) {
            alert("Failed to upload file");
        }
        setLoading(false);
    };

    return (
        <div className="max-w-2xl mx-auto p-4 space-y-6">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6"
            >
                <h3 className="text-xl font-bold text-slate-100 mb-6 flex items-center gap-2">
                    <Server className="w-5 h-5 text-blue-400" />
                    System Configuration
                </h3>

                <div className="space-y-6">
                    <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                        <div>
                            <h4 className="font-medium text-slate-200">LLM Provider</h4>
                            <p className="text-sm text-slate-400">Current Model: gemma3:12b (Ollama)</p>
                        </div>
                        <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-bold rounded-full border border-emerald-500/20">
                            Active
                        </span>
                    </div>

                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-amber-500/10 to-red-500/10 rounded-xl border border-amber-500/20">
                        <div>
                            <h4 className="font-medium text-slate-200 flex items-center gap-2">
                                <Zap className="w-4 h-4 text-amber-400" />
                                Fast Demo Mode
                            </h4>
                            <p className="text-sm text-slate-400">
                                {fastDemo
                                    ? "25 citizen + 5 Senate exchanges (~5-10 min)"
                                    : "100 citizen + 10 Senate exchanges (~45-60 min)"}
                            </p>
                        </div>
                        <button
                            onClick={toggleFastDemo}
                            disabled={loading}
                            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${fastDemo ? 'bg-amber-500' : 'bg-slate-700'
                                } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                            <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${fastDemo ? 'translate-x-6' : 'translate-x-1'
                                }`} />
                        </button>
                    </div>

                    <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                        <div className="flex-1">
                            <h4 className="font-medium text-slate-200 flex items-center gap-2">
                                <Upload className="w-4 h-4 text-blue-400" />
                                Upload Policy Document
                            </h4>
                            <p className="text-sm text-slate-400">Upload .md file for policy analysis</p>
                            {uploadFile && (
                                <p className="text-xs text-emerald-400 mt-1">Selected: {uploadFile.name}</p>
                            )}
                        </div>
                        <div className="flex gap-2">
                            <input
                                type="file"
                                accept=".md"
                                onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                                className="hidden"
                                id="policy-upload"
                            />
                            <label
                                htmlFor="policy-upload"
                                className="px-3 py-2 bg-blue-600 text-white text-xs rounded-lg cursor-pointer hover:bg-blue-700"
                            >
                                Choose File
                            </label>
                            {uploadFile && (
                                <button
                                    onClick={handleFileUpload}
                                    disabled={loading}
                                    className="px-3 py-2 bg-emerald-600 text-white text-xs rounded-lg hover:bg-emerald-700 disabled:opacity-50"
                                >
                                    Upload
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6"
            >
                <h3 className="text-xl font-bold text-slate-100 mb-6 flex items-center gap-2">
                    <Globe className="w-5 h-5 text-purple-400" />
                    Appearance
                </h3>

                <div className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                    <div>
                        <h4 className="font-medium text-slate-200">Theme</h4>
                        <p className="text-sm text-slate-400">Dark mode (default)</p>
                    </div>
                    <div className="flex gap-2 bg-slate-900 p-1 rounded-lg border border-slate-700">
                        <button className="p-2 bg-slate-700 rounded text-white"><Moon className="w-4 h-4" /></button>
                        <button className="p-2 text-slate-500 hover:text-slate-300"><Sun className="w-4 h-4" /></button>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
