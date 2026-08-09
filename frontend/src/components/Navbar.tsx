import React from 'react';
import { ShieldCheck, MessageSquare, Activity, LayoutDashboard, BookOpen, Sparkles } from 'lucide-react';

interface NavbarProps {
  activeTab: 'chat' | 'dashboard' | 'knowledge';
  setActiveTab: (tab: 'chat' | 'dashboard' | 'knowledge') => void;
  showInspector: boolean;
  setShowInspector: (show: boolean) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  showInspector,
  setShowInspector,
}) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800 bg-slate-950/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand & Track Badge */}
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 p-0.5 shadow-lg shadow-indigo-500/30 flex items-center justify-center">
            <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <ShieldCheck className="h-6 w-6 text-indigo-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400">
                Support<span className="text-indigo-400">IQ</span>
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Track 1 • AI Agent
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Powered by <span className="text-indigo-300 font-semibold">Swytchcode Governed Execution Layer</span>
            </p>
          </div>
        </div>

        {/* Center Tab Navigation */}
        <nav className="flex items-center space-x-1 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'chat'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <MessageSquare className="h-4 w-4" />
            <span>Agent Workspace</span>
          </button>

          <button
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'dashboard'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <LayoutDashboard className="h-4 w-4" />
            <span>Analytics Dashboard</span>
          </button>

          <button
            onClick={() => setActiveTab('knowledge')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'knowledge'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <BookOpen className="h-4 w-4" />
            <span className="hidden md:inline">Knowledge RAG</span>
          </button>
        </nav>

        {/* Right Governance Toggle & Live Indicator */}
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setShowInspector(!showInspector)}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-bold transition-all border ${
              showInspector
                ? 'bg-purple-950/60 text-purple-300 border-purple-500/40 badge-glow-amber'
                : 'bg-slate-900 text-slate-400 border-slate-800 hover:border-slate-700'
            }`}
          >
            <Activity className="h-4 w-4 text-purple-400 animate-pulse" />
            <span className="hidden sm:inline">Action Inspector</span>
          </button>

          <div className="flex items-center space-x-2 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span className="hidden lg:inline">Swytchcode Governed</span>
          </div>
        </div>

      </div>
    </header>
  );
};
