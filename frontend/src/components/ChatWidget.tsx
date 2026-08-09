import React, { useState } from 'react';
import { Send, Bot, User, ShieldAlert, Sparkles, CheckCircle2, HelpCircle, FileText, Cpu, ArrowRight } from 'lucide-react';
import { ChatMessage } from '../types';

interface ChatWidgetProps {
  messages: ChatMessage[];
  onSendMessage: (text: string) => void;
  isLoading: boolean;
  onSelectTrace: (msg: ChatMessage) => void;
}

export const ChatWidget: React.FC<ChatWidgetProps> = ({
  messages,
  onSendMessage,
  isLoading,
  onSelectTrace,
}) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input);
    setInput('');
  };

  const handleQuickDemo = (text: string) => {
    onSendMessage(text);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-5rem)] max-w-5xl mx-auto glass-panel rounded-2xl border border-slate-800 shadow-2xl overflow-hidden">
      
      {/* Chat Top Banner */}
      <div className="px-6 py-3.5 bg-slate-900/90 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="h-3 w-3 rounded-full bg-emerald-400 animate-pulse"></div>
          <div>
            <h2 className="text-sm font-bold text-slate-200">Customer Support Agent Workspace</h2>
            <p className="text-xs text-slate-400">Live Customer Session • Active Order #48291</p>
          </div>
        </div>

        {/* Quick Demo Scenario Controls for Hackathon Pitch */}
        <div className="hidden sm:flex items-center space-x-2">
          <span className="text-[11px] text-slate-400 font-semibold uppercase">Demo Presets:</span>
          <button
            onClick={() => handleQuickDemo("Where is my order #48291?")}
            className="px-2.5 py-1 text-xs bg-indigo-950/80 hover:bg-indigo-900 text-indigo-300 rounded-lg border border-indigo-700/40 transition-all font-medium"
          >
            1. Order #48291
          </button>
          <button
            onClick={() => handleQuickDemo("I want a refund. The product I received is damaged.")}
            className="px-2.5 py-1 text-xs bg-rose-950/80 hover:bg-rose-900 text-rose-300 rounded-lg border border-rose-700/40 transition-all font-medium"
          >
            2. Damaged Refund
          </button>
          <button
            onClick={() => handleQuickDemo("I don't know my order number.")}
            className="px-2.5 py-1 text-xs bg-amber-950/80 hover:bg-amber-900 text-amber-300 rounded-lg border border-amber-700/40 transition-all font-medium"
          >
            3. Clarification
          </button>
        </div>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start space-x-3 ${
              msg.sender === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {msg.sender === 'agent' && (
              <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 p-0.5 shadow-md flex-shrink-0">
                <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                  <Bot className="h-5 w-5 text-indigo-400" />
                </div>
              </div>
            )}

            <div
              className={`max-w-2xl rounded-2xl p-4 shadow-lg transition-all ${
                msg.sender === 'user'
                  ? 'bg-indigo-600 text-white rounded-tr-none'
                  : 'bg-slate-900/90 border border-slate-800 text-slate-200 rounded-tl-none'
              }`}
            >
              {/* Agent Message Header with Badges */}
              {msg.sender === 'agent' && (
                <div className="flex flex-wrap items-center gap-2 mb-2.5 pb-2 border-b border-slate-800/80">
                  {/* Decision Badge */}
                  {msg.decision_action === 'AUTO_RESOLVE' && (
                    <span className="flex items-center space-x-1 text-[11px] font-bold px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      <CheckCircle2 className="h-3 w-3" />
                      <span>AUTO-RESOLVED</span>
                    </span>
                  )}
                  {msg.decision_action === 'ASK_CLARIFICATION' && (
                    <span className="flex items-center space-x-1 text-[11px] font-bold px-2 py-0.5 rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      <HelpCircle className="h-3 w-3" />
                      <span>CLARIFICATION NEEDED</span>
                    </span>
                  )}
                  {msg.decision_action === 'ESCALATE_TO_HUMAN' && (
                    <span className="flex items-center space-x-1 text-[11px] font-bold px-2 py-0.5 rounded-md bg-rose-500/10 text-rose-400 border border-rose-500/20 badge-glow-red">
                      <ShieldAlert className="h-3 w-3" />
                      <span>HUMAN ESCALATION TRIGGERED</span>
                    </span>
                  )}

                  {/* Confidence Badge */}
                  {msg.confidence_score && (
                    <span className="text-[11px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded-md">
                      Confidence: {(msg.confidence_score * 100).toFixed(0)}%
                    </span>
                  )}

                  {/* Swytchcode Trace Trigger */}
                  {msg.swytchcode_trace && (
                    <button
                      onClick={() => onSelectTrace(msg)}
                      className="ml-auto text-[11px] font-semibold text-indigo-400 hover:text-indigo-300 bg-indigo-950/60 hover:bg-indigo-900/60 px-2.5 py-0.5 rounded-md border border-indigo-500/30 flex items-center space-x-1 transition-all"
                    >
                      <Cpu className="h-3 w-3" />
                      <span>View Swytchcode Trace</span>
                      <ArrowRight className="h-3 w-3" />
                    </button>
                  )}
                </div>
              )}

              {/* Message Text */}
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>

              {/* Grounded Source Citations */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-3.5 pt-3 border-t border-slate-800/80">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1.5 flex items-center space-x-1">
                    <FileText className="h-3 w-3 text-indigo-400" />
                    <span>Grounded Knowledge Base Sources:</span>
                  </span>
                  <div className="space-y-1.5">
                    {msg.sources.map((src, idx) => (
                      <div key={idx} className="text-xs bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                        <div className="flex items-center justify-between text-indigo-300 font-semibold mb-0.5">
                          <span>{src.title}</span>
                          <span className="text-[10px] text-slate-400">Match: {(src.relevance_score * 100).toFixed(0)}%</span>
                        </div>
                        <p className="text-[11px] text-slate-400 italic">"{src.excerpt}"</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <span className="text-[10px] text-slate-400 mt-2 block text-right font-mono">
                {msg.timestamp}
              </span>
            </div>

            {msg.sender === 'user' && (
              <div className="h-9 w-9 rounded-xl bg-slate-800 p-0.5 shadow-md flex-shrink-0 flex items-center justify-center">
                <User className="h-5 w-5 text-slate-300" />
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center space-x-3 text-slate-400 text-xs font-mono">
            <div className="h-8 w-8 rounded-xl bg-indigo-950 border border-indigo-500/30 flex items-center justify-center">
              <Sparkles className="h-4 w-4 text-indigo-400 animate-spin" />
            </div>
            <span>Swytchcode Policy Kernel validating tool permissions & RAG grounding...</span>
          </div>
        )}
      </div>

      {/* Input Box */}
      <form onSubmit={handleSubmit} className="p-4 bg-slate-900/90 border-t border-slate-800">
        <div className="flex items-center space-x-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask SupportIQ agent (e.g. 'Where is my order #48291?' or 'I want a refund for damaged goods')"
            className="flex-1 bg-slate-950 text-slate-100 placeholder-slate-500 text-sm px-4 py-3 rounded-xl border border-slate-800 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-5 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-lg shadow-indigo-600/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center space-x-2"
          >
            <span>Send</span>
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>

    </div>
  );
};
