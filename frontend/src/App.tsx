import { useState, useEffect } from 'react';
import { 
  History as HistoryIcon, User, Settings as SettingsIcon, 
  LogOut, LayoutDashboard, Search, BookOpen, AlertCircle
} from 'lucide-react';
import type { AnalysisResult, AnalysisHistoryItem } from './types';
import { GithubIcon } from './components/GithubIcon';
import { Auth } from './pages/Auth';
import { Dashboard } from './pages/Dashboard';
import { Report } from './pages/Report';
import { History } from './pages/History';
import { Profile } from './pages/Profile';
import { Settings } from './pages/Settings';
import { useAuth } from './context/AuthContext';
import { repositoriesAPI } from './services/api';
import { parseGitHubUrl } from './utils/api';
import { MOCK_HISTORY } from './utils/mockData';

function App() {
  const { user, isAuthenticated, logout, updateProfileState } = useAuth();
  const [currentView, setCurrentView] = useState<'dashboard' | 'history' | 'profile' | 'settings' | 'report'>('dashboard');
  const [historyItems, setHistoryItems] = useState<AnalysisHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStepIndex, setLoadingStepIndex] = useState(0);
  const [activeReport, setActiveReport] = useState<AnalysisResult | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState<string | null>(null);

  // Synchronize history items from backend if authenticated
  useEffect(() => {
    if (isAuthenticated) {
      repositoriesAPI.getHistory()
        .then(data => setHistoryItems(data))
        .catch(err => {
          console.warn("Failed to load history from backend, falling back to mock logs cache:", err);
          const saved = localStorage.getItem('git_intel_history');
          if (saved) setHistoryItems(JSON.parse(saved));
          else setHistoryItems(MOCK_HISTORY);
        });
    } else {
      setHistoryItems([]);
    }
  }, [isAuthenticated]);

  // Sync scan history to localStorage as secondary backup cache
  useEffect(() => {
    if (historyItems.length > 0) {
      localStorage.setItem('git_intel_history', JSON.stringify(historyItems));
    }
  }, [historyItems]);

  const handleStartAnalysis = async (url: string) => {
    setError(null);
    setIsLoading(true);
    setLoadingStepIndex(0);

    // Simulate timeline steps with timer intervals
    const interval = setInterval(() => {
      setLoadingStepIndex(prev => {
        if (prev >= 5) {
          clearInterval(interval);
          return 5;
        }
        return prev + 1;
      });
    }, 1100);

    try {
      // Execute the static code analysis request using Axios
      const reportData = await repositoriesAPI.analyze(url, false);
      
      // Ensure visual timeline reaches completion before rendering report
      await new Promise(resolve => setTimeout(resolve, 6000));
      clearInterval(interval);

      setActiveReport(reportData);
      
      // Synchronize history items from backend
      try {
        const historyData = await repositoriesAPI.getHistory();
        setHistoryItems(historyData);
      } catch {
        const parsed = parseGitHubUrl(url);
        const newHistoryItem: AnalysisHistoryItem = {
          id: reportData.analysis_id || `hist-${Date.now()}`,
          repositoryUrl: url,
          name: parsed?.name || reportData.repository,
          owner: parsed?.owner || 'github',
          date: new Date().toISOString().split('T')[0],
          language: reportData.repository_summary.repository_identity.primary_language,
          architecture: reportData.repository_summary.architecture.primary,
          score: reportData.training_quality?.score || 88,
          status: 'completed',
          result: reportData
        };
        setHistoryItems(prev => [newHistoryItem, ...prev]);
      }

      setIsLoading(false);
      setCurrentView('report');
    } catch (err: any) {
      clearInterval(interval);
      console.error("Analysis failed:", err);
      
      let errorMsg = 'An unexpected analysis pipeline error occurred.';
      if (err.code === 'ERR_NETWORK') {
        errorMsg = 'Backend Offline. Please confirm that the FastAPI backend server is running on port 8000.';
      } else if (err.response) {
        const status = err.response.status;
        const detail = err.response.data?.detail;
        
        if (status === 404) {
          errorMsg = 'Repository Not Found or is Private. Please verify the URL.';
        } else if (status === 403 || status === 429) {
          errorMsg = 'GitHub API Rate Limit Exceeded. Please configure a valid GITHUB_TOKEN inside backend .env configurations.';
        } else if (detail) {
          errorMsg = detail;
        } else if (status === 500) {
          errorMsg = 'AST Parsing or AI Generation Failed. The model failed to explain this codebase structure.';
        }
      }
      
      setError(errorMsg);
      setIsLoading(false);
    }
  };

  const handleSelectHistory = (item: AnalysisHistoryItem) => {
    if (item.result) {
      setActiveReport(item.result);
      setCurrentView('report');
    } else {
      // Re-run scan if raw report metadata was missing
      handleStartAnalysis(item.repositoryUrl);
    }
  };

  const handleDeleteHistory = async (id: string) => {
    try {
      await repositoriesAPI.deleteHistory(id);
    } catch (err) {
      console.warn("Failed to delete history log from backend:", err);
    }
    setHistoryItems(prev => prev.filter(item => item.id !== id));
  };

  const handleHeaderSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setCurrentView('dashboard');
    handleStartAnalysis(searchQuery.trim());
    setSearchQuery('');
  };

  // Render view controller templates
  const renderContent = () => {
    if (!isAuthenticated) {
      // Pass a dummy function as onLogin because the Auth component handles backend login context calls internally
      return <Auth onLogin={() => setCurrentView('dashboard')} />;
    }

    switch (currentView) {
      case 'dashboard':
        return (
          <Dashboard
            onStartAnalysis={handleStartAnalysis}
            isLoading={isLoading}
            loadingStepIndex={loadingStepIndex}
            error={error}
            clearError={() => setError(null)}
          />
        );
      case 'report':
        return activeReport ? (
          <Report 
            result={activeReport} 
            onBackToDashboard={() => setCurrentView('dashboard')} 
          />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center p-8 select-none">
            <AlertCircle size={32} className="text-zinc-650 mb-3" />
            <span className="text-sm font-mono text-zinc-500">No active analysis report loaded.</span>
          </div>
        );
      case 'history':
        return (
          <History
            historyItems={historyItems}
            onSelectHistory={handleSelectHistory}
            onDeleteHistory={handleDeleteHistory}
          />
        );
      case 'profile':
        return user ? (
          <Profile profile={user} historyItems={historyItems} />
        ) : null;
      case 'settings':
        return user ? (
          <Settings
            profile={user}
            onUpdateProfile={updateProfileState}
            onDeleteAccount={logout}
          />
        ) : null;
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-[#09090b]">
      {/* Sticky Navigation Header */}
      <header className="sticky top-0 z-50 w-full border-b border-zinc-800 bg-[#09090b]/80 backdrop-blur-md px-4 lg:px-8 py-3 flex items-center justify-between">
        
        {/* Left branding */}
        <div className="flex items-center gap-6">
          <div 
            onClick={() => setCurrentView('dashboard')}
            className="flex items-center gap-2.5 cursor-pointer select-none"
          >
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20 font-mono font-bold text-sm">
              RI
            </div>
            <span className="font-bold text-sm text-zinc-100 hidden sm:inline">Repository Intelligence</span>
          </div>

          {/* Quick Header search */}
          {isAuthenticated && currentView !== 'dashboard' && (
            <form onSubmit={handleHeaderSearch} className="relative hidden md:block">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-650" size={12} />
              <input
                type="url"
                required
                placeholder="Search Repository URL..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-48 xl:w-64 pl-8 pr-3 py-1.5 bg-zinc-900 border border-zinc-800 hover:border-zinc-750 focus:border-blue-500 outline-none rounded-lg text-[10px] font-mono text-zinc-300 transition-all"
              />
            </form>
          )}
        </div>

        {/* Right menu actions */}
        {isAuthenticated && (
          <nav className="flex items-center gap-1 select-none font-mono text-[11px] font-medium text-zinc-400">
            <button
              onClick={() => setCurrentView('dashboard')}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-lg transition-colors ${
                currentView === 'dashboard' ? 'text-zinc-100 bg-zinc-900' : 'hover:text-zinc-200'
              }`}
            >
              <LayoutDashboard size={14} />
              <span className="hidden sm:inline">Dashboard</span>
            </button>
            <button
              onClick={() => setCurrentView('history')}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-lg transition-colors ${
                currentView === 'history' ? 'text-zinc-100 bg-zinc-900' : 'hover:text-zinc-200'
              }`}
            >
              <HistoryIcon size={14} />
              <span className="hidden sm:inline">History</span>
            </button>
            <button
              onClick={() => setCurrentView('profile')}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-lg transition-colors ${
                currentView === 'profile' ? 'text-zinc-100 bg-zinc-900' : 'hover:text-zinc-200'
              }`}
            >
              <User size={14} />
              <span className="hidden sm:inline">Profile</span>
            </button>
            <button
              onClick={() => setCurrentView('settings')}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-lg transition-colors ${
                currentView === 'settings' ? 'text-zinc-100 bg-zinc-900' : 'hover:text-zinc-200'
              }`}
            >
              <SettingsIcon size={14} />
              <span className="hidden sm:inline">Settings</span>
            </button>
            <div className="w-[1px] h-4 bg-zinc-800 mx-2" />
            <button
              onClick={logout}
              className="flex items-center gap-1.5 px-3 py-2 text-red-400 hover:text-red-300 rounded-lg transition-colors"
              title="Logout Account"
            >
              <LogOut size={14} />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </nav>
        )}
      </header>

      {/* Main Panel */}
      <main className="flex-1 flex flex-col min-h-[calc(100vh-120px)] bg-[#09090b] relative">
        {renderContent()}
      </main>

      {/* universal SaaS Footer */}
      <footer className="w-full border-t border-zinc-850 bg-[#09090b] py-6 px-4 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4 font-mono text-[10px] text-zinc-550 select-none">
        <div className="flex items-center gap-1">
          <span>Engine v0.1.0</span>
          <span>•</span>
          <span>© 2026 Repository Intelligence SaaS.</span>
        </div>
        <div className="flex items-center gap-4 text-zinc-500">
          <a href="https://github.com" target="_blank" className="flex items-center gap-1 hover:text-zinc-350 transition-colors">
            <GithubIcon size={12} />
            GitHub
          </a>
          <a href="#docs" className="flex items-center gap-1 hover:text-zinc-350 transition-colors">
            <BookOpen size={12} />
            Documentation
          </a>
          <a href="#privacy" className="hover:text-zinc-350 transition-colors">Privacy</a>
          <a href="#terms" className="hover:text-zinc-350 transition-colors">Terms</a>
        </div>
      </footer>
    </div>
  );
}

export default App;
