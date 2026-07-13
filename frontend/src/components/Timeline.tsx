import React from 'react';
import { CheckCircle2, Loader2, RefreshCw, Code, Network, Cpu, Sparkles, FileSearch } from 'lucide-react';

export interface TimelineStep {
  title: string;
  description: string;
  icon: React.ReactNode;
}

interface TimelineProps {
  status: 'loading' | 'completed' | 'failed';
  currentStepIndex?: number; // 0 to 5 for active state in loading
}

export const Timeline: React.FC<TimelineProps> = ({ status, currentStepIndex = 0 }) => {
  const steps: TimelineStep[] = [
    {
      title: "Repository Fetch",
      description: "Fetching repository details, tree structure, and reading metadata files.",
      icon: <FileSearch size={16} />
    },
    {
      title: "Code Parsing",
      description: "Downloading and reading source code components for primary modules.",
      icon: <Code size={16} />
    },
    {
      title: "AST Analysis",
      description: "Parsing Python/TS code into Abstract Syntax Trees to extract functions and classes.",
      icon: <Cpu size={16} />
    },
    {
      title: "Dependency Extraction",
      description: "Analyzing package bindings to identify internal modules and external libraries.",
      icon: <Network size={16} />
    },
    {
      title: "Architecture Detection",
      description: "Inferring structural patterns (layered modules, APIs, MVC patterns).",
      icon: <RefreshCw size={16} />
    },
    {
      title: "AI Summary Generation",
      description: "Feeding structural facts to fine-tuned code models to generate insights.",
      icon: <Sparkles size={16} />
    }
  ];

  const getStepStatus = (index: number) => {
    if (status === 'completed') return 'done';
    if (status === 'failed' && index >= currentStepIndex) return 'error';
    if (index < currentStepIndex) return 'done';
    if (index === currentStepIndex && status === 'loading') return 'active';
    return 'pending';
  };

  return (
    <div className="relative border border-zinc-800 bg-[#0f0f12]/80 rounded-xl p-6 select-none shadow-xl">
      <h3 className="font-semibold text-lg text-zinc-100 mb-6 flex items-center gap-2">
        {status === 'loading' ? (
          <Loader2 size={18} className="animate-spin text-blue-500" />
        ) : (
          <CheckCircle2 size={18} className="text-emerald-500" />
        )}
        Analysis Timeline
      </h3>

      <div className="relative pl-8 border-l border-zinc-800 space-y-6 ml-4">
        {steps.map((step, idx) => {
          const stepStatus = getStepStatus(idx);
          
          return (
            <div key={`step-${idx}`} className="relative group">
              {/* Connector line light effect */}
              {idx < steps.length - 1 && (
                <div 
                  className={`absolute left-[-33px] top-[26px] w-[1px] h-[calc(100%+24px)] transition-all duration-500 ${
                    stepStatus === 'done' ? 'bg-emerald-500' : 'bg-zinc-800'
                  }`} 
                />
              )}

              {/* Icon Marker */}
              <div 
                className={`absolute left-[-42px] top-[1.5px] w-5 h-5 rounded-full flex items-center justify-center border transition-all duration-300 ${
                  stepStatus === 'done'
                    ? 'bg-emerald-500/10 border-emerald-500 text-emerald-500'
                    : stepStatus === 'active'
                    ? 'bg-blue-500/15 border-blue-500 text-blue-400 shadow-[0_0_10px_rgba(59,130,246,0.3)] animate-pulse'
                    : stepStatus === 'error'
                    ? 'bg-red-500/10 border-red-500 text-red-500'
                    : 'bg-[#09090b] border-zinc-800 text-zinc-600'
                }`}
              >
                {stepStatus === 'active' ? (
                  <Loader2 size={12} className="animate-spin" />
                ) : stepStatus === 'done' ? (
                  <CheckCircle2 size={12} />
                ) : (
                  step.icon
                )}
              </div>

              {/* Text Meta */}
              <div className="flex flex-col text-left">
                <span 
                  className={`font-mono text-xs font-semibold tracking-wide transition-colors ${
                    stepStatus === 'done' 
                      ? 'text-emerald-400' 
                      : stepStatus === 'active' 
                      ? 'text-blue-400' 
                      : 'text-zinc-400'
                  }`}
                >
                  {step.title}
                </span>
                <span className="text-[11px] text-zinc-500 mt-1 max-w-md group-hover:text-zinc-400 transition-colors">
                  {step.description}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
