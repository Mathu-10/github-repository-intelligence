import React, { useState } from 'react';
import { Settings as SettingsIcon, Bell, Shield, Key, AlertTriangle, Check } from 'lucide-react';
import type { UserProfile } from '../types';

interface SettingsProps {
  profile: UserProfile;
  onUpdateProfile: (name: string, email: string) => void;
  onDeleteAccount: () => void;
}

export const Settings: React.FC<SettingsProps> = ({
  profile,
  onUpdateProfile,
  onDeleteAccount,
}) => {
  const [name, setName] = useState(profile.name);
  const [email, setEmail] = useState(profile.email);
  const [notifyAnalysis, setNotifyAnalysis] = useState(true);
  const [notifyDataset, setNotifyDataset] = useState(false);
  const [apiKey, setApiKey] = useState('sk-proj-••••••••••••••••••••••••');
  const [successMsg, setSuccessMsg] = useState('');

  const handleSaveAccount = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdateProfile(name, email);
    triggerSuccess('Account properties updated successfully.');
  };

  const handleSaveSecurity = (e: React.FormEvent) => {
    e.preventDefault();
    triggerSuccess('Security API keys synchronized.');
  };

  const triggerSuccess = (msg: string) => {
    setSuccessMsg(msg);
    setTimeout(() => setSuccessMsg(''), 3000);
  };

  const handleDelete = () => {
    if (confirm("WARNING: Are you absolutely sure you want to delete your account? This action is irreversible, and all scan logs will be removed.")) {
      onDeleteAccount();
    }
  };

  return (
    <div className="flex-1 max-w-4xl mx-auto w-full p-4 text-left space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <SettingsIcon className="text-blue-500" size={20} />
          Application Settings
        </h2>
        <p className="text-xs text-zinc-500 mt-1 select-none">
          Configure security modules, notification webhooks, account properties, and fine-tuning details.
        </p>
      </div>

      {successMsg && (
        <div className="p-3 bg-emerald-950/40 border border-emerald-900/50 text-emerald-400 rounded-lg text-xs flex items-center gap-2 font-mono">
          <Check size={14} />
          {successMsg}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Navigation Categories Sidebar */}
        <div className="md:col-span-1 select-none">
          <div className="bg-[#0f0f12] border border-zinc-800 rounded-xl p-2 flex flex-col gap-1 text-xs font-mono font-medium">
            <a href="#account" className="flex items-center gap-2.5 px-3 py-2 text-zinc-300 hover:bg-zinc-900 rounded-lg transition-all">
              <Shield size={14} className="text-zinc-500" />
              Account Profiles
            </a>
            <a href="#notifications" className="flex items-center gap-2.5 px-3 py-2 text-zinc-300 hover:bg-zinc-900 rounded-lg transition-all">
              <Bell size={14} className="text-zinc-500" />
              Notification Routing
            </a>
            <a href="#security" className="flex items-center gap-2.5 px-3 py-2 text-zinc-300 hover:bg-zinc-900 rounded-lg transition-all">
              <Key size={14} className="text-zinc-500" />
              API Provider Settings
            </a>
          </div>
        </div>

        {/* Configurations Fields Canvas */}
        <div className="md:col-span-2 space-y-6">
          
          {/* SEC: ACCOUNT PROFILE */}
          <section id="account" className="bg-[#0f0f12] border border-zinc-800 rounded-xl p-6 space-y-4">
            <h3 className="text-sm font-semibold text-zinc-200 border-b border-zinc-900 pb-3 flex items-center gap-2 select-none">
              Account Information
            </h3>
            <form onSubmit={handleSaveAccount} className="space-y-4 text-xs font-mono">
              <div className="flex flex-col gap-1.5">
                <label className="text-zinc-400 font-semibold" htmlFor="settingName">Full Name</label>
                <input
                  id="settingName"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-[#09090b] border border-zinc-800 focus:border-blue-500 outline-none rounded-lg text-zinc-300 transition-all"
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-zinc-400 font-semibold" htmlFor="settingEmail">Email Address</label>
                <input
                  id="settingEmail"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-[#09090b] border border-zinc-800 focus:border-blue-500 outline-none rounded-lg text-zinc-300 transition-all"
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg shadow-md transition-all focus:outline-none"
              >
                Save Profile Updates
              </button>
            </form>
          </section>

          {/* SEC: NOTIFICATIONS */}
          <section id="notifications" className="bg-[#0f0f12] border border-zinc-800 rounded-xl p-6 space-y-4 select-none">
            <h3 className="text-sm font-semibold text-zinc-200 border-b border-zinc-900 pb-3 flex items-center gap-2">
              Notifications Preferences
            </h3>
            <div className="space-y-3.5 text-xs text-zinc-300 font-mono">
              <label className="flex items-start gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={notifyAnalysis}
                  onChange={(e) => setNotifyAnalysis(e.target.checked)}
                  className="rounded bg-[#09090b] border-zinc-800 text-blue-500 focus:ring-0 focus:ring-offset-0 w-3.5 h-3.5 mt-0.5"
                />
                <div className="flex flex-col">
                  <span className="font-semibold text-zinc-300">Email Analysis Reports</span>
                  <span className="text-[10px] text-zinc-550 mt-0.5">Receive email markdown file attachments when scans complete.</span>
                </div>
              </label>

              <label className="flex items-start gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={notifyDataset}
                  onChange={(e) => setNotifyDataset(e.target.checked)}
                  className="rounded bg-[#09090b] border-zinc-800 text-blue-500 focus:ring-0 focus:ring-offset-0 w-3.5 h-3.5 mt-0.5"
                />
                <div className="flex flex-col">
                  <span className="font-semibold text-zinc-300">Dataset Training Webhooks</span>
                  <span className="text-[10px] text-zinc-550 mt-0.5">Dispatch payload records notifications to third-party logs.</span>
                </div>
              </label>
            </div>
          </section>

          {/* SEC: API SECURITY */}
          <section id="security" className="bg-[#0f0f12] border border-zinc-800 rounded-xl p-6 space-y-4">
            <h3 className="text-sm font-semibold text-zinc-200 border-b border-zinc-900 pb-3 flex items-center gap-2 select-none">
              API Configuration Keys
            </h3>
            <form onSubmit={handleSaveSecurity} className="space-y-4 text-xs font-mono">
              <div className="flex flex-col gap-1.5">
                <label className="text-zinc-400 font-semibold" htmlFor="apiKeyInput">LLM Provider API Key</label>
                <input
                  id="apiKeyInput"
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-[#09090b] border border-zinc-800 focus:border-blue-500 outline-none rounded-lg text-zinc-300 transition-all font-mono"
                />
                <span className="text-[9px] text-zinc-500">API keys are stored strictly in client memory states.</span>
              </div>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg shadow-md transition-all focus:outline-none"
              >
                Save Keys
              </button>
            </form>
          </section>

          {/* SEC: DANGER ZONE (DELETE ACCOUNT) */}
          <section className="bg-red-950/10 border border-red-900/30 rounded-xl p-6 space-y-4 select-none">
            <h3 className="text-sm font-semibold text-red-400 border-b border-red-900/20 pb-3 flex items-center gap-2">
              <AlertTriangle size={16} />
              Danger Zone
            </h3>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="flex-1 text-xs">
                <span className="font-bold text-zinc-300 block font-mono">Delete Account Database</span>
                <span className="text-zinc-500 mt-1 block">Permanently erase profile settings and LocalStorage scan history logs.</span>
              </div>
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-900/20 hover:bg-red-900/30 border border-red-900/40 text-red-400 text-xs font-semibold font-mono rounded-lg transition-colors shrink-0"
              >
                Delete Account
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};
