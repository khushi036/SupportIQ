import React from 'react';
import { X, ShieldCheck, CheckCircle2, AlertTriangle, Clock, Lock, Cpu, Code2 } from 'lucide-react';
import { ChatMessage } from '../types';

interface ActionInspectorProps {
  selectedMessage: ChatMessage | null;
  onClose: () => void;
}

export const ActionInspector: React.FC<ActionInspectorProps> = ({
  selectedMessage,
  onClose,
}) => {
  if (!selectedMessage || !selectedMessage.swytchcode_trace) {
    return (
      <div className="w-80 sm:w-96 glass-panel border-l border-slate-800 p-6 flex flex-col items-center justify-center text-center text-slate-500">
        <Cpu className="h-12 w-12 text-slate-700 mb-3 animate-pulse" />
        <h3 className="text-sm font-bold text-slate-300">Swytchcode Action Inspector</h3>
        <p className="text-xs text-slate-500 mt-1 max-w-xs">
          Select any agent response with an active tool execution trace to inspect Swytchcode policy checks, schema validation, and raw JSON payloads.
        </p>
      </div>
    );
  }

  const trace = selectedMessage.swytchcode_trace;
  const gov = trace.swytchcode_governance;

  return (
    <aside className="w-80 sm:w-96 glass-panel-glow border-l border-slate-800 flex flex-col h-[calc(100vh-5rem)] overflow-y-auto">
      
      {/* Header */}
      <div className="p-4 bg-slate-900/90 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="h-5 w-5 text-indigo-400" />
          <div>
            <h3 className="text-sm font-bold text-slate-200">Swytchcode Governance Inspector</h3>
            <p className="text-[10px] text-indigo-300 font-mono">Kernel: {gov.execution_kernel}</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      <div className="p-5 space-y-6">
        
        {/* Status Summary Card */}
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Policy Compliance</span>
            <span
              className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
                trace.success
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 badge-glow-green'
                  : 'bg-rose-500/10 text-rose-400 border-rose-500/30 badge-glow-red'
              }`}
            >
              {gov.policy_status}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800 text-xs">
            <div>
              <span className="text-[10px] text-slate-500 block">Executed Tool</span>
              <span className="font-mono text-indigo-300 font-bold">{gov.tool}</span>
            </div>
            <div>
              <span className="text-[10px] text-slate-500 block">Risk Rating</span>
              <span
                className={`font-bold ${
                  gov.risk_level === 'HIGH'
                    ? 'text-rose-400'
                    : gov.risk_level === 'MEDIUM'
                    ? 'text-amber-400'
                    : 'text-emerald-400'
                }`}
              >
                {gov.risk_level} RISK
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-500 block">Execution Latency</span>
              <span className="font-mono text-slate-300 flex items-center space-x-1">
                <Clock className="h-3 w-3 text-slate-500" />
                <span>{gov.latency_ms} ms</span>
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-500 block">Timestamp</span>
              <span className="font-mono text-slate-400 text-[10px]">{gov.timestamp}</span>
            </div>
          </div>
        </div>

        {/* Validated Input Parameters */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
              <Lock className="h-3.5 w-3.5 text-indigo-400" />
              <span>Validated Schema Parameters</span>
            </span>
            <span className="text-[10px] text-emerald-400 font-mono">Regex Match Verified</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 overflow-x-auto">
            <pre>{JSON.stringify(trace.params_validated, null, 2)}</pre>
          </div>
        </div>

        {/* Swytchcode Tooling Policy Rule Reference */}
        <div className="p-3.5 rounded-xl bg-indigo-950/30 border border-indigo-500/20 text-xs">
          <div className="flex items-center space-x-2 text-indigo-300 font-semibold mb-1">
            <ShieldCheck className="h-4 w-4 text-indigo-400" />
            <span>Swytchcode Rule Verification (`tooling.json`)</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Every tool invocation is evaluated against pre-configured rate limits, permission manifests, and schema patterns before dispatching to backend APIs.
          </p>
        </div>

        {/* Raw JSON Trace Payload */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
              <Code2 className="h-3.5 w-3.5 text-purple-400" />
              <span>Raw API Response Payload</span>
            </span>
          </div>
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 font-mono text-[11px] text-purple-300 max-h-60 overflow-y-auto">
            <pre>{JSON.stringify(trace.data || trace.error, null, 2)}</pre>
          </div>
        </div>

      </div>
    </aside>
  );
};
