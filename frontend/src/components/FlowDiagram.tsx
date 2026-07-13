import React, { useState } from 'react';
import { GitCommit, ArrowRight, ArrowDown, HelpCircle, Code, Server, Database } from 'lucide-react';
import type { AnalysisResult, ExecutionFlowStep } from '../types';

interface FlowDiagramProps {
  result: AnalysisResult;
}

export const FlowDiagram: React.FC<FlowDiagramProps> = ({ result }) => {
  const [activeStep, setActiveStep] = useState<number | null>(null);

  const rawFlow = result.target_output.execution_flow;

  // Convert execution flow to structured steps if it is a list of strings
  const steps: ExecutionFlowStep[] = React.useMemo(() => {
    if (!rawFlow || rawFlow.length === 0) {
      // Default fallback match
      return [
        { source: "User Request", target: "API Router", relationship: "HTTP Request", starts_from_entry_point: true },
        { source: "API Router", target: "Business Logic", relationship: "Controller Dispatch", starts_from_entry_point: false },
        { source: "Business Logic", target: "Database", relationship: "SQL Query / ORM Fetch", starts_from_entry_point: false },
        { source: "Database", target: "API Response", relationship: "JSON Payload", starts_from_entry_point: false }
      ];
    }

    if (typeof rawFlow[0] === 'string') {
      const stringList = rawFlow as string[];
      const computed: ExecutionFlowStep[] = [];
      for (let i = 0; i < stringList.length; i++) {
        computed.push({
          source: stringList[i],
          target: stringList[i + 1] || "Response Cycle",
          relationship: i === 0 ? "Initial Execution" : "Calls next module",
          starts_from_entry_point: i === 0
        });
      }
      return computed;
    }

    return rawFlow as ExecutionFlowStep[];
  }, [rawFlow]);

  // Extract unique stages to display
  const uniqueStages = React.useMemo(() => {
    const stages: string[] = [];
    steps.forEach(step => {
      if (!stages.includes(step.source)) {
        stages.push(step.source);
      }
      if (!stages.includes(step.target)) {
        stages.push(step.target);
      }
    });
    return stages;
  }, [steps]);

  const getStageIcon = (stage: string) => {
    const lower = stage.toLowerCase();
    if (lower.includes("request") || lower.includes("client") || lower.includes("user")) {
      return <Code className="text-blue-400 shrink-0" size={16} />;
    }
    if (lower.includes("db") || lower.includes("database") || lower.includes("model")) {
      return <Database className="text-purple-400 shrink-0" size={16} />;
    }
    if (lower.includes("api") || lower.includes("route") || lower.includes("controller") || lower.includes("server")) {
      return <Server className="text-emerald-400 shrink-0" size={16} />;
    }
    return <Code className="text-zinc-400 shrink-0" size={16} />;
  };

  return (
    <div className="bg-[#0f0f12] border border-zinc-800 rounded-xl p-6">
      <div className="mb-6">
        <h3 className="font-semibold text-lg text-zinc-100 flex items-center gap-2">
          <GitCommit className="text-blue-500 rotate-90" size={18} />
          Execution Flow Path
        </h3>
        <p className="text-xs text-zinc-500 mt-1">
          Interactive workflow visualization showing code execution paths and layer transitions. Click on connecting paths to view relationship constraints.
        </p>
      </div>

      {/* Horizontal Flow layout for desktop */}
      <div className="hidden md:flex flex-col gap-8 py-4 overflow-x-auto">
        <div className="flex items-center justify-between gap-2 min-w-[700px] px-4">
          {uniqueStages.map((stage, index) => {
            const isLast = index === uniqueStages.length - 1;
            const correspondingStep = steps.find(s => s.source === stage);
            const relation = correspondingStep?.relationship || "Response callback";

            return (
              <React.Fragment key={`stage-${index}`}>
                {/* Node Box */}
                <div 
                  className={`flex flex-col items-center justify-center p-3 rounded-lg border text-center transition-all min-w-[120px] max-w-[160px] h-20 ${
                    activeStep !== null && steps[activeStep]?.source === stage
                      ? 'border-blue-500 bg-blue-500/10 text-white shadow-[0_0_15px_-3px_rgba(37,99,235,0.4)]'
                      : 'border-zinc-800 bg-[#09090b] text-zinc-300 hover:border-zinc-700'
                  }`}
                >
                  <div className="mb-1.5">{getStageIcon(stage)}</div>
                  <span className="font-mono text-xs font-semibold truncate w-full px-1">{stage.split('/').pop()}</span>
                  <span className="text-[9px] text-zinc-500 truncate w-full px-1">{stage.includes('/') ? stage : 'runtime context'}</span>
                </div>

                {/* Arrow Connector */}
                {!isLast && (
                  <div 
                    className="flex-1 flex flex-col items-center justify-center cursor-pointer group"
                    onClick={() => setActiveStep(index)}
                  >
                    <span className="text-[10px] text-zinc-500 group-hover:text-blue-400 transition-colors truncate max-w-[120px] mb-1">
                      {relation.split(' ').slice(0, 2).join(' ')}...
                    </span>
                    <div className="flex items-center w-full justify-center">
                      <div className={`h-0.5 flex-1 transition-all ${
                        activeStep === index ? 'bg-blue-500' : 'bg-zinc-800 group-hover:bg-zinc-600'
                      }`} />
                      <ArrowRight 
                        size={14} 
                        className={`mx-1 transition-all shrink-0 ${
                          activeStep === index ? 'text-blue-500' : 'text-zinc-700 group-hover:text-zinc-500'
                        }`} 
                      />
                    </div>
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>

      {/* Vertical Flow layout for mobile/small laptop screens */}
      <div className="flex md:hidden flex-col gap-4 py-2">
        {uniqueStages.map((stage, index) => {
          const isLast = index === uniqueStages.length - 1;
          const correspondingStep = steps.find(s => s.source === stage);
          const relation = correspondingStep?.relationship || "Response callback";

          return (
            <div key={`stage-v-${index}`} className="flex flex-col items-center">
              <div 
                className={`flex items-center gap-3 p-3 w-full max-w-sm rounded-lg border transition-all ${
                  activeStep !== null && steps[activeStep]?.source === stage
                    ? 'border-blue-500 bg-blue-500/10 text-white'
                    : 'border-zinc-800 bg-[#09090b] text-zinc-300'
                }`}
              >
                {getStageIcon(stage)}
                <div className="flex flex-col text-left">
                  <span className="font-mono text-xs font-semibold">{stage}</span>
                </div>
              </div>

              {!isLast && (
                <div 
                  className="flex flex-col items-center my-2 gap-1 cursor-pointer"
                  onClick={() => setActiveStep(index)}
                >
                  <ArrowDown size={16} className={activeStep === index ? 'text-blue-500' : 'text-zinc-700'} />
                  <span className="text-[10px] text-zinc-500 font-mono italic">{relation}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Selected Relationship Detail panel */}
      <div className="mt-6 bg-[#09090b] border border-zinc-800 rounded-lg p-4 text-xs">
        {activeStep !== null && steps[activeStep] ? (
          <div>
            <div className="flex items-center gap-2 mb-2 text-blue-400 font-semibold font-mono">
              <span>Connector Action Detail</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-zinc-400">
              <div>
                <span className="text-zinc-500 block text-[10px] uppercase">From Source Node</span>
                <span className="font-semibold text-zinc-300 font-mono break-all">{steps[activeStep].source}</span>
              </div>
              <div>
                <span className="text-zinc-500 block text-[10px] uppercase">Connection Details</span>
                <span className="font-bold text-zinc-200 block border-b border-zinc-900 pb-1">{steps[activeStep].relationship}</span>
                <span className="text-[10px] text-zinc-500 italic">
                  {steps[activeStep].starts_from_entry_point ? "Initiated from main application entry point" : "Implicit module import sequence"}
                </span>
              </div>
              <div>
                <span className="text-zinc-500 block text-[10px] uppercase">To Target Node</span>
                <span className="font-semibold text-zinc-300 font-mono break-all">{steps[activeStep].target}</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-zinc-500 italic text-center py-2 flex items-center justify-center gap-2">
            <HelpCircle size={14} />
            <span>Click any connecting transition line to inspect transaction details.</span>
          </div>
        )}
      </div>
    </div>
  );
};
