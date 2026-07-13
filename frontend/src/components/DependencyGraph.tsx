import React, { useState, useMemo } from 'react';
import { Layers } from 'lucide-react';
import type { AnalysisResult } from '../types';

interface DependencyGraphProps {
  result: AnalysisResult;
}

interface Node {
  id: string;
  label: string;
  type: 'core' | 'internal' | 'external';
  x: number;
  y: number;
}

interface Link {
  source: string;
  target: string;
  importName?: string;
}

export const DependencyGraph: React.FC<DependencyGraphProps> = ({ result }) => {
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);
  const [filterType, setFilterType] = useState<'all' | 'internal' | 'external'>('all');

  const { repository_summary, important_file_details, internal_dependencies } = result;

  const repoName = repository_summary.repository_identity.name;
  const internals = important_file_details || [];
  const externals = repository_summary.dependencies.directly_used || [];
  const linksRaw = internal_dependencies || [];

  // SVG Size Definitions
  const width = 600;
  const height = 400;
  const cx = width / 2;
  const cy = height / 2;

  // Compute Node Positions Radially
  const graph = useMemo(() => {
    const nodes: Node[] = [];
    const links: Link[] = [];

    // Core Root Node
    nodes.push({
      id: "root",
      label: repoName,
      type: 'core',
      x: cx,
      y: cy,
    });

    // Positions for Internal Nodes
    const internalNodesCount = internals.length;
    const rInternal = 100; // Radius for internal layer
    internals.forEach((file, index) => {
      const angle = (index * 2 * Math.PI) / (internalNodesCount || 1) - Math.PI / 2;
      const x = cx + rInternal * Math.cos(angle);
      const y = cy + rInternal * Math.sin(angle);
      
      const fileBasename = file.path.split('/').pop() || file.path;

      nodes.push({
        id: file.path,
        label: fileBasename,
        type: 'internal',
        x,
        y,
      });

      // Connect internal files to core root
      links.push({
        source: file.path,
        target: "root"
      });
    });

    // Positions for External Nodes
    const externalNodesCount = externals.length;
    const rExternal = 190; // Radius for external layer
    externals.forEach((ext, index) => {
      // Offset angles slightly so they align beautifully
      const angle = (index * 2 * Math.PI) / (externalNodesCount || 1) + Math.PI / 6;
      const x = cx + rExternal * Math.cos(angle);
      const y = cy + rExternal * Math.sin(angle);

      nodes.push({
        id: `ext-${ext}`,
        label: ext,
        type: 'external',
        x,
        y,
      });
    });

    // Map internal dependencies link structures
    linksRaw.forEach(link => {
      links.push({
        source: link.source,
        target: link.target,
        importName: link.import
      });
    });

    // Map external dependencies links from internal files that import them
    internals.forEach(file => {
      file.imports.forEach(imp => {
        // Simple heuristic to check if import contains an external library name
        externals.forEach(ext => {
          const cleanExt = ext.replace('-', '_');
          if (imp.toLowerCase().startsWith(cleanExt) || imp.toLowerCase().includes(`.${cleanExt}`)) {
            links.push({
              source: file.path,
              target: `ext-${ext}`,
              importName: imp
            });
          }
        });
      });
    });

    return { nodes, links };
  }, [repoName, internals, externals, linksRaw, cx, cy]);

  // Filters nodes and links based on selected tab filter
  const filteredGraph = useMemo(() => {
    let nodes = graph.nodes;
    let links = graph.links;

    if (filterType === 'internal') {
      nodes = nodes.filter(n => n.type !== 'external');
      links = links.filter(l => {
        const s = graph.nodes.find(n => n.id === l.source);
        const t = graph.nodes.find(n => n.id === l.target);
        return s?.type !== 'external' && t?.type !== 'external';
      });
    } else if (filterType === 'external') {
      nodes = nodes.filter(n => n.type !== 'internal');
      links = links.filter(l => {
        const s = graph.nodes.find(n => n.id === l.source);
        const t = graph.nodes.find(n => n.id === l.target);
        return s?.type === 'external' || t?.type === 'external' || l.target === 'root';
      });
    }

    return { nodes, links };
  }, [graph, filterType]);

  const getNodeColor = (type: Node['type'], isHovered: boolean) => {
    if (type === 'core') return isHovered ? '#3b82f6' : '#2563eb'; // Deep Blue
    if (type === 'internal') return isHovered ? '#10b981' : '#059669'; // Emerald
    return isHovered ? '#a855f7' : '#8b5cf6'; // Purple
  };

  const getFilteredLinks = () => {
    if (hoveredNode) {
      return filteredGraph.links.filter(
        link => link.source === hoveredNode || link.target === hoveredNode
      );
    }
    return filteredGraph.links;
  };

  return (
    <div className="bg-[#0f0f12] border border-zinc-800 rounded-xl p-6 flex flex-col md:flex-row gap-6">
      <div className="flex-1">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-semibold text-lg text-zinc-100 flex items-center gap-2">
            <Layers size={18} className="text-blue-500" />
            Dependency Architecture Map
          </h3>
          <div className="flex bg-zinc-900 border border-zinc-800 rounded-lg p-0.5 text-xs">
            {(['all', 'internal', 'external'] as const).map(type => (
              <button
                key={type}
                className={`px-3 py-1.5 rounded-md capitalize font-medium transition-all ${
                  filterType === type
                    ? 'bg-zinc-800 text-zinc-100'
                    : 'text-zinc-400 hover:text-zinc-200'
                }`}
                onClick={() => setFilterType(type)}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        <div className="relative border border-zinc-800/80 bg-[#09090b]/80 rounded-lg overflow-hidden flex items-center justify-center min-h-[400px]">
          <svg
            viewBox={`0 0 ${width} ${height}`}
            className="w-full h-full max-h-[400px] select-none"
          >
            {/* Draw Arrows Definition */}
            <defs>
              <marker
                id="arrow"
                viewBox="0 0 10 10"
                refX="20"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#3f3f46" />
              </marker>
              <marker
                id="arrow-hover"
                viewBox="0 0 10 10"
                refX="20"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb" />
              </marker>
            </defs>

            {/* Render Link Lines */}
            {getFilteredLinks().map((link, i) => {
              const sourceNode = filteredGraph.nodes.find(n => n.id === link.source);
              const targetNode = filteredGraph.nodes.find(n => n.id === link.target);
              if (!sourceNode || !targetNode) return null;

              const isHighlighted = hoveredNode === link.source || hoveredNode === link.target;

              return (
                <line
                  key={`link-${i}`}
                  x1={sourceNode.x}
                  y1={sourceNode.y}
                  x2={targetNode.x}
                  y2={targetNode.y}
                  stroke={isHighlighted ? '#3b82f6' : '#27272a'}
                  strokeWidth={isHighlighted ? 2.5 : 1}
                  strokeDasharray={sourceNode.type === 'external' || targetNode.type === 'external' ? '4,4' : undefined}
                  markerEnd={isHighlighted ? 'url(#arrow-hover)' : 'url(#arrow)'}
                  className="transition-all duration-300"
                />
              );
            })}

            {/* Render Nodes */}
            {filteredGraph.nodes.map(node => {
              const isHovered = hoveredNode === node.id;
              const isDimmed = hoveredNode !== null && !isHovered && 
                !filteredGraph.links.some(l => 
                  (l.source === node.id && l.target === hoveredNode) || 
                  (l.target === node.id && l.source === hoveredNode)
                );

              return (
                <g
                  key={node.id}
                  className="cursor-pointer transition-all duration-300"
                  onMouseEnter={() => setHoveredNode(node.id)}
                  onMouseLeave={() => setHoveredNode(null)}
                  style={{ opacity: isDimmed ? 0.35 : 1 }}
                >
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={node.type === 'core' ? 22 : node.type === 'internal' ? 14 : 10}
                    fill={getNodeColor(node.type, isHovered)}
                    stroke="#09090b"
                    strokeWidth={2}
                    className="transition-all duration-300"
                  />
                  <text
                    x={node.x}
                    y={node.y + (node.type === 'core' ? 36 : node.type === 'internal' ? 28 : 22)}
                    textAnchor="middle"
                    fill={isHovered ? '#ffffff' : '#a1a1aa'}
                    className={`font-mono ${node.type === 'core' ? 'text-xs font-bold' : 'text-[10px]'} fill-current transition-colors`}
                  >
                    {node.label}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>
      </div>

      {/* Info Sidebar Details */}
      <div className="w-full md:w-56 flex flex-col justify-between border-t md:border-t-0 md:border-l border-zinc-800 pt-6 md:pt-0 md:pl-6">
        <div>
          <h4 className="text-sm font-semibold text-zinc-200 mb-3 uppercase tracking-wider">Legend</h4>
          <div className="space-y-3">
            <div className="flex items-center gap-2.5 text-xs text-zinc-300">
              <span className="w-3.5 h-3.5 rounded-full bg-blue-600 border border-black shrink-0" />
              <div className="flex flex-col">
                <span className="font-semibold text-zinc-200">Repository Root</span>
                <span className="text-zinc-500">Central module core</span>
              </div>
            </div>
            <div className="flex items-center gap-2.5 text-xs text-zinc-300">
              <span className="w-3.5 h-3.5 rounded-full bg-emerald-600 border border-black shrink-0" />
              <div className="flex flex-col">
                <span className="font-semibold text-emerald-400">Internal Files</span>
                <span className="text-zinc-500">Module components</span>
              </div>
            </div>
            <div className="flex items-center gap-2.5 text-xs text-zinc-300">
              <span className="w-3.5 h-3.5 rounded-full bg-purple-600 border border-black shrink-0" />
              <div className="flex flex-col">
                <span className="font-semibold text-purple-400">External Packages</span>
                <span className="text-zinc-500">Imported package links</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-zinc-900/60 rounded-xl p-3 border border-zinc-800/80 mt-6 text-xs text-zinc-400">
          {hoveredNode ? (
            <div>
              <div className="font-bold text-zinc-200 truncate mb-1">
                {hoveredNode === 'root' ? repoName : hoveredNode.replace('ext-', '')}
              </div>
              <div className="capitalize text-zinc-500 font-medium mb-2 text-[10px]">
                Type: {hoveredNode === 'root' ? 'Repository Core' : hoveredNode.startsWith('ext-') ? 'External Library' : 'Internal Source Code'}
              </div>
              <div className="text-zinc-400 border-t border-zinc-800/80 pt-1.5">
                {hoveredNode === 'root' ? (
                  <span>Main application boundary containing analyzed files.</span>
                ) : hoveredNode.startsWith('ext-') ? (
                  <span>Third-party dependency declared in package configuration scripts.</span>
                ) : (
                  <span>
                    Imports: {internals.find(f => f.path === hoveredNode)?.imports.length || 0} packages.
                  </span>
                )}
              </div>
            </div>
          ) : (
            <div className="text-zinc-500 italic text-center py-4">
              Hover over nodes to inspect details and dependency linkages.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
