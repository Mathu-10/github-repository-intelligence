import React from 'react';
import { Award, GitBranch, Cpu, Mail, Calendar, FileDown } from 'lucide-react';
import type { UserProfile, AnalysisHistoryItem } from '../types';

interface ProfileProps {
  profile: UserProfile;
  historyItems: AnalysisHistoryItem[];
}

export const Profile: React.FC<ProfileProps> = ({ profile, historyItems }) => {
  const languageCounts = React.useMemo(() => {
    const counts: Record<string, number> = {};
    historyItems.forEach(item => {
      counts[item.language] = (counts[item.language] || 0) + 1;
    });
    return counts;
  }, [historyItems]);

  const sortedLanguages = Object.entries(languageCounts)
    .sort((a, b) => b[1] - a[1])
    .map(entry => entry[0]);

  const handleExportHistory = () => {
    const csvContent = "data:text/csv;charset=utf-8," 
      + ["Repository,Date,Language,Architecture,Score,Status"].join(",") + "\n"
      + historyItems.map(item => 
          `"${item.owner}/${item.name}","${item.date}","${item.language}","${item.architecture}",${item.score},"${item.status}"`
        ).join("\n");
        
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "repository_intelligence_history.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex-1 max-w-4xl mx-auto w-full p-4 text-left space-y-6">
      {/* Profile Overview Card */}
      <div className="bg-[#0f0f12] border border-zinc-800 rounded-xl p-6 relative overflow-hidden shadow-xl">
        <div className="absolute top-0 right-0 w-48 h-48 bg-blue-500/5 rounded-full blur-3xl -z-10" />

        <div className="flex flex-col sm:flex-row items-center gap-6 select-none">
          {/* Avatar Badge */}
          <div className="w-16 h-16 rounded-xl bg-blue-600/10 border border-blue-500/20 text-blue-500 flex items-center justify-center font-bold text-2xl shadow-[0_0_15px_-3px_rgba(37,99,235,0.2)] shrink-0">
            {profile.name.split(' ').map(p => p[0]).join('')}
          </div>

          <div className="flex-1 text-center sm:text-left space-y-2">
            <h2 className="text-xl font-bold text-white">{profile.name}</h2>
            <div className="flex flex-wrap items-center justify-center sm:justify-start gap-4 text-xs text-zinc-450 font-mono">
              <span className="flex items-center gap-1.5"><Mail size={12} /> {profile.email}</span>
              <span className="flex items-center gap-1.5"><Calendar size={12} /> Joined {profile.joinedDate}</span>
            </div>
          </div>

          <button
            onClick={handleExportHistory}
            className="flex items-center gap-1.5 px-4 py-2 bg-zinc-900 border border-zinc-850 hover:bg-zinc-850 hover:border-zinc-750 text-xs font-mono font-medium rounded-lg text-zinc-300 transition-all text-center shrink-0"
          >
            <FileDown size={14} />
            Export History
          </button>
        </div>
      </div>

      {/* Analytics Dashboard Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-[#0f0f12] border border-zinc-850 p-5 rounded-xl text-left select-none">
          <div className="p-2 bg-blue-500/10 rounded-lg text-blue-500 w-fit mb-3"><Award size={16} /></div>
          <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest font-bold">Total Scans Run</span>
          <span className="text-3xl font-extrabold text-white block mt-1">{profile.analysesCompleted}</span>
          <span className="text-[9px] font-mono text-zinc-550 block mt-1.5">Accumulated project audits</span>
        </div>

        <div className="bg-[#0f0f12] border border-zinc-850 p-5 rounded-xl text-left select-none">
          <div className="p-2 bg-blue-500/10 rounded-lg text-blue-500 w-fit mb-3"><GitBranch size={16} /></div>
          <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest font-bold">Repositories Tracked</span>
          <span className="text-3xl font-extrabold text-white block mt-1">{profile.repositoriesAnalyzedCount}</span>
          <span className="text-[9px] font-mono text-zinc-550 block mt-1.5">Unique public packages analyzed</span>
        </div>

        <div className="bg-[#0f0f12] border border-zinc-850 p-5 rounded-xl text-left select-none">
          <div className="p-2 bg-blue-500/10 rounded-lg text-blue-500 w-fit mb-3"><Cpu size={16} /></div>
          <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest font-bold">Favorite Languages</span>
          <div className="flex flex-wrap gap-1.5 mt-2">
            {(sortedLanguages.length > 0 ? sortedLanguages.slice(0, 3) : profile.favoriteLanguages).map(lang => (
              <span key={lang} className="px-2 py-0.5 rounded bg-zinc-950 border border-zinc-850 text-xs font-semibold text-zinc-450 font-mono">
                {lang}
              </span>
            ))}
          </div>
          <span className="text-[9px] font-mono text-zinc-550 block mt-2">Inferred from parser runs</span>
        </div>
      </div>

      {/* Dataset Summary panel */}
      <div className="border border-zinc-800 bg-[#0f0f12] rounded-xl p-5 select-none text-left">
        <h4 className="text-xs font-mono font-bold text-zinc-400 uppercase tracking-wider mb-2">Fine-Tuning Dataset Contributions</h4>
        <p className="text-xs text-zinc-500 leading-relaxed">
          Your profile is currently synchronized with the pipeline's fine-tuning dataset writer. You have contributed <span className="text-blue-400 font-bold font-mono">34</span> highly verified repository summary examples towards model dataset refinement.
        </p>
      </div>
    </div>
  );
};
