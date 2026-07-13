import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface AccordionProps {
  title: string;
  icon?: React.ReactNode;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

export const Accordion: React.FC<AccordionProps> = ({
  title,
  icon,
  children,
  defaultOpen = false,
}) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border border-zinc-800 rounded-xl overflow-hidden bg-[#0f0f12]">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 font-semibold text-sm text-zinc-200 hover:bg-zinc-800/20 transition-all select-none"
      >
        <div className="flex items-center gap-3.5">
          {icon && <span className="text-zinc-500">{icon}</span>}
          <span className="text-left font-mono tracking-wide">{title}</span>
        </div>
        <span className="text-zinc-500">
          {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </span>
      </button>
      
      {isOpen && (
        <div className="border-t border-zinc-800/60 p-4 bg-[#09090b]/40 text-sm text-zinc-300">
          {children}
        </div>
      )}
    </div>
  );
};
