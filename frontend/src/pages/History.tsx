


import React, { useState } from 'react';
import { History as HistoryIcon, Search, Eye, Trash2, Calendar, Award } from 'lucide-react';
import type { AnalysisHistoryItem } from '../types';

interface HistoryProps {
  historyItems: AnalysisHistoryItem[];
  onSelectHistory: (item: AnalysisHistoryItem) => void;
  onDeleteHistory: (id: string) => void;
}

export const History: React.FC<HistoryProps> = ({
  historyItems,
  onSelectHistory,
  onDeleteHistory,
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredItems = historyItems.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.owner.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.language.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex-1 max-w-6xl mx-auto w-full p-4 text-left">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <HistoryIcon className="text-blue-500" size={20} />
            Analysis History
          </h2>
          <p className="text-xs text-zinc-500 mt-1 select-none">
            A comprehensive record of all previous repository structure analyses and fine-tuning datasets.
          </p>
        </div>

        {/* Search filter input */}
        <div className="relative w-full md:w-64">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-550"><Search size={14} /></span>
          <input
            type="text"
            placeholder="Filter by name or language..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-[#0f0f12] border border-zinc-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none rounded-lg text-xs font-mono text-zinc-300 transition-all placeholder:text-zinc-600"
          />
        </div>
      </div>

      {filteredItems.length === 0 ? (
        /* Empty State */
        <div className="border border-zinc-850 bg-[#0f0f12]/40 rounded-xl p-12 text-center select-none">
          <div className="w-12 h-12 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-center mx-auto mb-4 text-zinc-500">
            <HistoryIcon size={20} />
          </div>
          <h3 className="font-semibold text-zinc-300 text-sm">No analysis history found</h3>
          <p className="text-xs text-zinc-500 mt-1 max-w-sm mx-auto">
            Run a diagnostic analysis on a GitHub repository URL from the central console to build audit histories.
          </p>
        </div>
      ) : (
        /* History Logs List Table */
        <div className="border border-zinc-800 rounded-xl overflow-hidden bg-[#0f0f12] shadow-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-xs font-mono text-left">
              <thead className="bg-[#09090b] border-b border-zinc-800 text-zinc-500 select-none">
                <tr>
                  <th className="p-4">Repository</th>
                  <th className="p-4">Date</th>
                  <th className="p-4">Primary Language</th>
                  <th className="p-4">Architecture Type</th>
                  <th className="p-4 text-right">Score</th>
                  <th className="p-4 text-center">Status</th>
                  <th className="p-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-900/60 text-zinc-300">
                {filteredItems.map((item) => (
                  <tr key={item.id} className="hover:bg-zinc-900/30 transition-colors">
                    <td className="p-4">
                      <div className="flex flex-col">
                        <span className="font-bold text-zinc-200">{item.owner}/{item.name}</span>
                        <span className="text-[10px] text-zinc-500 truncate max-w-xs mt-0.5">{item.repositoryUrl}</span>
                      </div>
                    </td>
                    <td className="p-4 text-zinc-400">
                      <div className="flex items-center gap-1.5">
                        <Calendar size={12} className="text-zinc-650" />
                        {new Date(item.date).toLocaleDateString()}
                      </div>
                    </td>
                    <td className="p-4">
                      <span className="px-2 py-0.5 rounded bg-zinc-950 border border-zinc-850 text-zinc-400">
                        {item.language}
                      </span>
                    </td>
                    <td className="p-4 text-zinc-400 max-w-[150px] truncate" title={item.architecture}>
                      {item.architecture}
                    </td>
                    <td className="p-4 text-right font-bold text-blue-400">
                      <div className="flex items-center justify-end gap-1">
                        <Award size={12} className="text-zinc-600" />
                        {item.score}%
                      </div>
                    </td>
                    <td className="p-4 text-center">
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-950/40 border border-emerald-900/50 text-emerald-400">
                        <span className="w-1 h-1 rounded-full bg-emerald-400" />
                        {item.status}
                      </span>
                    </td>
                    <td className="p-4 text-center">
                      <div className="flex items-center justify-center gap-2">
                        <button
                          onClick={() => onSelectHistory(item)}
                          className="p-1.5 bg-zinc-900 hover:bg-zinc-850 border border-zinc-800 text-zinc-400 hover:text-white rounded-md transition-colors"
                          title="Open Report"
                        >
                          <Eye size={12} />
                        </button>
                        <button
                          onClick={() => onDeleteHistory(item.id)}
                          className="p-1.5 bg-zinc-900 hover:bg-red-950/20 border border-zinc-800 hover:border-red-900/30 text-zinc-500 hover:text-red-400 rounded-md transition-colors"
                          title="Delete Record"
                        >
                          <Trash2 size={12} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
