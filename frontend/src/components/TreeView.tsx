import React, { useState } from 'react';
import { Folder, FolderOpen, FileText, ChevronDown, ChevronRight, Settings, Terminal, Info, Database } from 'lucide-react';

interface TreeNode {
  path: string;
  isDir: boolean;
  children?: TreeNode[];
}

interface TreeViewProps {
  nodes: TreeNode[];
}

export const TreeView: React.FC<TreeViewProps> = ({ nodes }) => {
  return (
    <div className="font-mono text-sm text-zinc-300 select-none overflow-y-auto max-h-[450px] p-2 bg-[#09090b]/40 rounded-lg border border-zinc-800">
      {nodes.length === 0 ? (
        <div className="text-zinc-500 italic p-4 text-center">No structural files found.</div>
      ) : (
        nodes.map((node) => <TreeNodeComponent key={node.path} node={node} depth={0} />)
      )}
    </div>
  );
};

interface TreeNodeComponentProps {
  node: TreeNode;
  depth: number;
}

const TreeNodeComponent: React.FC<TreeNodeComponentProps> = ({ node, depth }) => {
  const [isOpen, setIsOpen] = useState(depth === 0); // Keep root nodes open by default
  const parts = node.path.split('/');
  const name = parts[parts.length - 1];

  const handleToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (node.isDir) {
      setIsOpen(!isOpen);
    }
  };

  // Select appropriate icon for different file types
  const getFileIcon = (fileName: string) => {
    const lower = fileName.toLowerCase();
    if (lower === 'package.json' || lower === 'pyproject.toml' || lower === 'tsconfig.json') {
      return <Settings size={16} className="text-blue-400 mr-2 shrink-0" />;
    }
    if (lower.endsWith('.py') || lower.endsWith('.sh') || lower.endsWith('.bat')) {
      return <Terminal size={16} className="text-emerald-400 mr-2 shrink-0" />;
    }
    if (lower.endsWith('.md') || lower.endsWith('.txt')) {
      return <Info size={16} className="text-amber-400 mr-2 shrink-0" />;
    }
    if (lower.includes('db') || lower.endsWith('.sql') || lower.endsWith('.sqlite')) {
      return <Database size={16} className="text-purple-400 mr-2 shrink-0" />;
    }
    return <FileText size={16} className="text-zinc-400 mr-2 shrink-0" />;
  };

  return (
    <div className="flex flex-col">
      <div
        className={`flex items-center py-1.5 px-2 rounded-md cursor-pointer hover:bg-zinc-800/50 transition-colors ${
          node.isDir ? 'text-zinc-200' : 'text-zinc-400'
        }`}
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
        onClick={handleToggle}
      >
        {node.isDir ? (
          <>
            <span className="text-zinc-500 mr-1.5 hover:text-zinc-300 shrink-0">
              {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            </span>
            <span className="mr-2 shrink-0">
              {isOpen ? (
                <FolderOpen size={16} className="text-blue-500" />
              ) : (
                <Folder size={16} className="text-blue-500" />
              )}
            </span>
          </>
        ) : (
          <span className="ml-5 shrink-0">{getFileIcon(name)}</span>
        )}
        <span className="truncate">{name}</span>
      </div>

      {node.isDir && isOpen && node.children && (
        <div className="flex flex-col">
          {node.children.map((child) => (
            <TreeNodeComponent key={child.path} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
};
