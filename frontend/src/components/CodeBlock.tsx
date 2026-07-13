import React, { useState } from 'react';
import { Copy, Check, Terminal } from 'lucide-react';

interface CodeBlockProps {
  code: string;
  language?: string;
  fileName?: string;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language = 'python',
  fileName,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const lines = code.trim().split('\n');

  return (
    <div className="border border-zinc-800 rounded-xl overflow-hidden bg-[#09090b] font-mono text-xs">
      {/* File Header Tab */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-zinc-950/80 border-b border-zinc-850">
        <div className="flex items-center gap-2 text-zinc-400">
          <Terminal size={14} className="text-zinc-500" />
          <span className="text-[11px] truncate select-none">{fileName || `preview.${language}`}</span>
        </div>
        <button
          onClick={handleCopy}
          className="text-zinc-500 hover:text-zinc-350 p-1 hover:bg-zinc-900 rounded-md transition-colors"
          title="Copy Code"
        >
          {copied ? <Check size={14} className="text-emerald-500" /> : <Copy size={14} />}
        </button>
      </div>

      {/* Code Text Grid */}
      <div className="overflow-x-auto p-4 flex gap-4 leading-relaxed max-h-[350px]">
        {/* Line Numbers */}
        <div className="text-zinc-650 text-right select-none pr-2 border-r border-zinc-900 min-w-[20px] text-zinc-600">
          {lines.map((_, i) => (
            <div key={`ln-${i}`}>{i + 1}</div>
          ))}
        </div>
        {/* Source Content */}
        <pre className="flex-1 text-zinc-350 overflow-x-auto text-left select-text">
          <code className={`language-${language}`}>
            {lines.map((line, idx) => {
              // Basic color highlights for visual polish without heavy library overhead
              const isComment = line.trim().startsWith('#') || line.trim().startsWith('//');
              const isImport = line.trim().startsWith('import ') || line.trim().startsWith('from ');
              const isDef = line.trim().startsWith('def ') || line.trim().startsWith('class ') || line.trim().startsWith('const ');
              
              let styleClass = "text-zinc-300";
              if (isComment) styleClass = "text-zinc-600 italic";
              else if (isImport) styleClass = "text-blue-400 font-semibold";
              else if (isDef) styleClass = "text-emerald-400";

              return (
                <div key={`line-${idx}`} className={styleClass}>
                  {line || ' '}
                </div>
              );
            })}
          </code>
        </pre>
      </div>
    </div>
  );
};
