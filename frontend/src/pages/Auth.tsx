import React, { useState } from 'react';
import { Shield, Mail, Lock, User, ArrowRight } from 'lucide-react';
import { GithubIcon } from '../components/GithubIcon';
import { useAuth } from '../context/AuthContext';

interface AuthProps {
  onLogin: (userName: string, userEmail: string) => void;
}

export const Auth: React.FC<AuthProps> = ({ onLogin }) => {
  const { login, register } = useAuth();
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      if (isRegister) {
        if (!fullName || !email || !password || !confirmPassword) {
          setError('Please fill in all registration fields');
          return;
        }
        if (password !== confirmPassword) {
          setError('Passwords do not match');
          return;
        }
        await register(fullName, email, password);
        onLogin(fullName, email);
      } else {
        if (!email || !password) {
          setError('Please enter your email and password');
          return;
        }
        await login(email, password);
        const nameFromEmail = email.split('@')[0];
        const capitalized = nameFromEmail.charAt(0).toUpperCase() + nameFromEmail.slice(1);
        onLogin(capitalized, email);
      }
    } catch (err: any) {
      console.error("Auth error:", err);
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : 'Authentication failed. Please verify connection credentials.');
    }
  };

  const handleGitHubAuth = async () => {
    try {
      // Simulate successful GitHub OAuth route callback sequence
      await login("github-dev@git-intel.io", "github_oauth_mock_password");
      onLogin("GitHub Developer", "github-dev@git-intel.io");
    } catch (err: any) {
      setError('GitHub authentication simulation failed.');
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center p-4 bg-[#09090b] min-h-[calc(100vh-140px)]">
      <div className="w-full max-w-md bg-[#0f0f12] border border-zinc-800 rounded-xl p-8 shadow-2xl relative overflow-hidden">
        {/* Decorative corner light */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl -z-10" />

        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 bg-blue-600/10 border border-blue-500/30 rounded-xl flex items-center justify-center text-blue-500 mb-3 shadow-[0_0_15px_-3px_rgba(37,99,235,0.25)]">
            <Shield size={24} />
          </div>
          <h2 className="text-xl font-bold text-zinc-100 select-none">
            {isRegister ? 'Create Your Account' : 'Welcome to Repository Intelligence'}
          </h2>
          <p className="text-xs text-zinc-500 mt-1 select-none text-center">
            {isRegister
              ? 'Join software teams analyzing repository structures and codebase flows.'
              : 'Log in to continue to your developer console dashboard.'}
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-950/40 border border-red-900/50 rounded-lg text-xs text-red-400 text-left">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-left">
          {isRegister && (
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-mono text-zinc-400 font-semibold" htmlFor="fullName">Full Name</label>
              <div className="relative">
                <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-500"><User size={16} /></span>
                <input
                  id="fullName"
                  type="text"
                  placeholder="Sarah Jenkins"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-[#09090b] border border-zinc-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none rounded-lg text-sm text-zinc-300 font-mono transition-all"
                />
              </div>
            </div>
          )}

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-mono text-zinc-400 font-semibold" htmlFor="email">Email Address</label>
            <div className="relative">
              <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-500"><Mail size={16} /></span>
              <input
                id="email"
                type="email"
                placeholder="s.jenkins@developer.io"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-[#09090b] border border-zinc-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none rounded-lg text-sm text-zinc-300 font-mono transition-all"
              />
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <div className="flex justify-between items-center">
              <label className="text-xs font-mono text-zinc-400 font-semibold" htmlFor="password">Password</label>
              {!isRegister && (
                <button
                  type="button"
                  className="text-[10px] text-zinc-500 hover:text-blue-400 font-mono"
                  onClick={() => alert("Simulating forgot password sequence. A password reset link has been dispatched to your email mock.")}
                >
                  Forgot password?
                </button>
              )}
            </div>
            <div className="relative">
              <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-500"><Lock size={16} /></span>
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-[#09090b] border border-zinc-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none rounded-lg text-sm text-zinc-300 font-mono transition-all"
              />
            </div>
          </div>

          {isRegister && (
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-mono text-zinc-400 font-semibold" htmlFor="confirmPassword">Confirm Password</label>
              <div className="relative">
                <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-500"><Lock size={16} /></span>
                <input
                  id="confirmPassword"
                  type="password"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-[#09090b] border border-zinc-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none rounded-lg text-sm text-zinc-300 font-mono transition-all"
                />
              </div>
            </div>
          )}

          {!isRegister && (
            <div className="flex items-center justify-between py-1">
              <label className="flex items-center gap-2 text-xs text-zinc-400 font-mono select-none cursor-pointer">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded bg-[#09090b] border-zinc-800 text-blue-500 focus:ring-0 focus:ring-offset-0 focus:outline-none w-3.5 h-3.5"
                />
                Remember me
              </label>
            </div>
          )}

          <button
            type="submit"
            className="w-full flex items-center justify-center gap-2 py-3 bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold rounded-lg shadow-md hover:shadow-lg transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/50"
          >
            {isRegister ? 'Create Account' : 'Log In'}
            <ArrowRight size={16} />
          </button>

          <div className="relative my-6 select-none">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-zinc-800" /></div>
            <div className="relative flex justify-center text-xs uppercase"><span className="bg-[#0f0f12] px-2 text-zinc-500 font-mono">Or connect with</span></div>
          </div>

          <button
            type="button"
            onClick={handleGitHubAuth}
            className="w-full flex items-center justify-center gap-2 py-2.5 bg-[#09090b] hover:bg-zinc-900 border border-zinc-800 hover:border-zinc-700 text-zinc-200 text-sm font-medium rounded-lg transition-all focus:outline-none"
          >
            <GithubIcon size={16} />
            Continue with GitHub
          </button>
        </form>

        <div className="mt-6 text-center select-none">
          <button
            type="button"
            className="text-xs text-zinc-400 hover:text-blue-400 transition-colors font-mono"
            onClick={() => {
              setIsRegister(!isRegister);
              setError('');
            }}
          >
            {isRegister ? 'Already have an account? Log in' : "Don't have an account? Register"}
          </button>
        </div>
      </div>
    </div>
  );
};
