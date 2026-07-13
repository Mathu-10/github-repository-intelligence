import React, { useState } from 'react';
import { Play, Clipboard, RotateCcw, AlertCircle } from 'lucide-react';
import { Timeline } from '../components/Timeline';

interface DashboardProps {
  onStartAnalysis: (repoUrl: string) => void;
  isLoading: boolean;
  loadingStepIndex: number;
  error: string | null;
  clearError: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({
  onStartAnalysis,
  isLoading,
  loadingStepIndex,
  error,
  clearError,
}) => {
  const [repoUrl, setRepoUrl] = useState('');
  const [saveTraining, setSaveTraining] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!repoUrl.trim()) return;
    onStartAnalysis(repoUrl.trim());
  };

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text.includes("github.com")) {
        setRepoUrl(text.trim());
        clearError();
      } else {
        alert("Clipboard content does not resemble a GitHub link.");
      }
    } catch {
      alert("Could not access clipboard. Please paste manually (Ctrl+V).");
    }
  };

  const handleClear = () => {
    setRepoUrl('');
    clearError();
  };

  const selectSuggestion = (url: string) => {
    setRepoUrl(url);
    clearError();
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center py-10 px-4 max-w-4xl mx-auto w-full">
      {isLoading ? (
        /* Progress Timeline Screen */
        <div className="w-full max-w-lg space-y-6">
          <div className="text-center space-y-2 select-none">
            <h2 className="text-xl font-bold text-zinc-200 animate-pulse">Running Codebase Diagnostics...</h2>
            <p className="text-xs text-zinc-500 font-mono">
              Analyzing repository structure and internal module graph imports.
            </p>
          </div>
          <Timeline status="loading" currentStepIndex={loadingStepIndex} />
        </div>
      ) : (
        /* Main console landing search input screen */
        <div className="w-full space-y-12">
          {/* Hero Section */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-white leading-tight">
              AI-Powered <span className="text-blue-500">GitHub Repository</span> Intelligence
            </h1>
            <p className="text-sm md:text-base text-zinc-400 max-w-2xl mx-auto leading-relaxed">
              Analyze GitHub repositories using static code analysis, structural page ranking, and a fine-tuned Large Language Model. Explore execution flows, file trees, dependencies, and automated explanations.
            </p>
          </div>

          {/* Repository URL Input Card */}
          <div className="bg-[#0f0f12] border border-zinc-800 rounded-xl p-6 md:p-8 shadow-2xl relative">
            <div className="absolute top-0 left-10 w-24 h-[1px] bg-gradient-to-right bg-blue-500/50" />
            
            {error && (
              <div className="mb-6 p-4 bg-red-950/30 border border-red-900/50 rounded-lg flex gap-3 text-left">
                <AlertCircle className="text-red-500 shrink-0 mt-0.5" size={16} />
                <div className="flex-1">
                  <h4 className="text-xs font-bold text-red-400 font-mono">Analysis Compilation Error</h4>
                  <p className="text-xs text-red-500/90 mt-1">{error}</p>
                </div>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6 text-left">
              <div className="flex flex-col gap-2">
                <label htmlFor="repoUrl" className="text-xs font-mono text-zinc-400 font-semibold uppercase tracking-wider">
                  GitHub Repository URL
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600 font-mono select-none">git:</span>
                  <input
                    id="repoUrl"
                    type="url"
                    required
                    placeholder="https://github.com/owner/repository"
                    value={repoUrl}
                    onChange={(e) => setRepoUrl(e.target.value)}
                    className="w-full pl-12 pr-28 py-3.5 bg-[#09090b] border border-zinc-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none rounded-lg text-sm font-mono text-zinc-300 transition-all placeholder:text-zinc-650"
                  />
                  <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1.5">
                    <button
                      type="button"
                      onClick={handlePaste}
                      className="p-1.5 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-900 rounded-md transition-colors"
                      title="Paste Clipboard"
                    >
                      <Clipboard size={14} />
                    </button>
                    <button
                      type="button"
                      onClick={handleClear}
                      className="p-1.5 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-900 rounded-md transition-colors"
                      title="Clear Input"
                    >
                      <RotateCcw size={14} />
                    </button>
                  </div>
                </div>
              </div>

              {/* Advanced Fine-Tuning controls */}
              <div className="flex items-center justify-between border-t border-zinc-900 pt-5">
                <label className="flex items-center gap-2.5 text-xs text-zinc-400 font-mono select-none cursor-pointer">
                  <input
                    type="checkbox"
                    checked={saveTraining}
                    onChange={(e) => setSaveTraining(e.target.checked)}
                    className="rounded bg-[#09090b] border-zinc-800 text-blue-500 focus:ring-0 focus:ring-offset-0 focus:outline-none w-3.5 h-3.5"
                  />
                  Save training sample in local fine-tuning dataset
                </label>

                <button
                  type="submit"
                  disabled={!repoUrl.trim()}
                  className="flex items-center justify-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:bg-zinc-800 disabled:text-zinc-500 disabled:cursor-not-allowed text-white text-xs font-semibold font-mono rounded-lg shadow-md hover:shadow-lg transition-all"
                >
                  <Play size={12} fill="currentColor" />
                  Analyze Repository
                </button>
              </div>
            </form>
          </div>

          {/* Quick Triggers Suggestion Panel */}
          <div className="space-y-3.5 text-left">
            <span className="text-xs font-mono text-zinc-500 uppercase tracking-widest block font-bold">
              Demo Repository Presets
            </span>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button
                onClick={() => selectSuggestion("https://github.com/Mathu-10/github-repository-intelligence")}
                className="bg-[#0f0f12] border border-zinc-850 hover:border-zinc-800 p-4 rounded-xl text-left hover:bg-zinc-900/30 transition-all flex flex-col group"
              >
                <span className="font-mono text-xs text-blue-400 font-bold group-hover:text-blue-300">
                  Mathu-10/github-repository-intelligence
                </span>
                <span className="text-xs text-zinc-500 mt-1.5 truncate">
                  FastAPI backend + Python static AST analysis parser.
                </span>
              </button>

              <button
                onClick={() => selectSuggestion("https://github.com/openai/openai-python")}
                className="bg-[#0f0f12] border border-zinc-850 hover:border-zinc-800 p-4 rounded-xl text-left hover:bg-zinc-900/30 transition-all flex flex-col group"
              >
                <span className="font-mono text-xs text-blue-400 font-bold group-hover:text-blue-300">
                  openai/openai-python
                </span>
                <span className="text-xs text-zinc-500 mt-1.5 truncate">
                  Official Python client library for querying OpenAI LLMs.
                </span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
