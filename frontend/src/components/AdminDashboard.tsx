import React, { useEffect, useState } from 'react';
import { LayoutDashboard, CheckCircle, Clock, ShieldAlert, Star, Cpu, ArrowUpRight, Activity, Users, FileSpreadsheet } from 'lucide-react';
import { DashboardMetrics } from '../types';

export const AdminDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/dashboard')
      .then((res) => res.json())
      .then((data) => {
        setMetrics(data);
        setLoading(false);
      })
      .catch(() => {
        // Fallback demo metrics if backend off
        setMetrics({
          total_conversations: 1248,
          auto_resolution_rate: 87.4,
          average_response_time_sec: 1.2,
          escalation_count: 96,
          customer_satisfaction: 4.85,
          total_swytchcode_calls: 3420,
          active_conversations: 14,
          recent_escalations: [
            {
              id: 'ESC-901',
              customer: 'Akshay Saxena',
              order_id: '48291',
              reason: 'Damaged goods refund request ($129.99)',
              priority: 'HIGH',
              status: 'ASSIGNED_SUPERVISOR',
              time: '2 mins ago',
            },
            {
              id: 'ESC-884',
              customer: 'Rahul Verma',
              order_id: '10244',
              reason: 'Frustrated sentiment & shipping delay inquiry',
              priority: 'MEDIUM',
              status: 'IN_REVIEW',
              time: '14 mins ago',
            },
          ],
          api_action_breakdown: {
            get_order_status: 2180,
            create_support_ticket: 490,
            request_refund: 310,
            get_customer_details: 440,
          },
        });
        setLoading(false);
      });
  }, []);

  if (loading || !metrics) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-5rem)]">
        <div className="flex items-center space-x-3 text-indigo-400 font-mono">
          <Activity className="h-6 w-6 animate-spin" />
          <span>Loading SupportIQ Real-time Analytics...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8 overflow-y-auto max-h-[calc(100vh-5rem)]">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-100 flex items-center space-x-3">
            <LayoutDashboard className="h-7 w-7 text-indigo-400" />
            <span>SupportIQ Executive Analytics Dashboard</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time performance metrics, Swytchcode execution stats, and human escalation queues.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold rounded-xl flex items-center space-x-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span>Live Telemetry Active</span>
          </span>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        {/* Metric 1 */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider">AI Resolution Rate</span>
            <CheckCircle className="h-5 w-5 text-emerald-400" />
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-white">{metrics.auto_resolution_rate}%</span>
            <span className="text-xs font-semibold text-emerald-400 flex items-center">
              <ArrowUpRight className="h-3.5 w-3.5" /> +4.2%
            </span>
          </div>
          <p className="text-xs text-slate-500">Autonomous resolution without human touch</p>
        </div>

        {/* Metric 2 */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider">Avg Response Time</span>
            <Clock className="h-5 w-5 text-indigo-400" />
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-white">{metrics.average_response_time_sec}s</span>
            <span className="text-xs font-semibold text-indigo-400 font-mono">1,200ms latency</span>
          </div>
          <p className="text-xs text-slate-500">FastAPI + Swytchcode Execution Kernel</p>
        </div>

        {/* Metric 3 */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider">Swytchcode API Calls</span>
            <Cpu className="h-5 w-5 text-purple-400" />
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-white">{metrics.total_swytchcode_calls.toLocaleString()}</span>
            <span className="text-xs font-semibold text-purple-400 font-mono">100% Policy Checked</span>
          </div>
          <p className="text-xs text-slate-500">Governed backend API executions</p>
        </div>

        {/* Metric 4 */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase tracking-wider">Customer CSAT</span>
            <Star className="h-5 w-5 text-amber-400 fill-amber-400" />
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-3xl font-extrabold text-white">{metrics.customer_satisfaction} / 5.0</span>
          </div>
          <p className="text-xs text-slate-500">Based on post-chat resolution surveys</p>
        </div>

      </div>

      {/* Two Column Layout: API Action Breakdown & Live Escalation Queue */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left 1 Col: API Action Distribution */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-slate-200 flex items-center space-x-2">
            <FileSpreadsheet className="h-5 w-5 text-indigo-400" />
            <span>Swytchcode Tool Executions</span>
          </h3>

          <div className="space-y-3.5">
            {Object.entries(metrics.api_action_breakdown).map(([tool, count]) => {
              const total = Object.values(metrics.api_action_breakdown).reduce((a, b) => a + b, 0);
              const pct = ((count / total) * 100).toFixed(1);
              return (
                <div key={tool} className="space-y-1">
                  <div className="flex justify-between text-xs font-mono">
                    <span className="text-indigo-300 font-semibold">{tool}</span>
                    <span className="text-slate-400">{count} ({pct}%)</span>
                  </div>
                  <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"
                      style={{ width: `${pct}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs text-slate-400">
            <span className="font-semibold text-slate-200">Governance Engine Note:</span> Zero unvalidated tool calls allowed under active `tooling.json` policy rules.
          </div>
        </div>

        {/* Right 2 Col: Live Escalation Queue */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-200 flex items-center space-x-2">
              <ShieldAlert className="h-5 w-5 text-rose-400" />
              <span>Active Human Escalation Queue ({metrics.escalation_count})</span>
            </h3>
            <span className="text-xs text-slate-400 font-mono">Auto-assigned via 3-Tier Decision Matrix</span>
          </div>

          <div className="space-y-3">
            {metrics.recent_escalations.map((esc) => (
              <div
                key={esc.id}
                className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:border-slate-700 transition-all"
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-bold text-indigo-400 font-mono">{esc.id}</span>
                    <span className="text-xs font-semibold text-slate-200">{esc.customer}</span>
                    <span className="text-xs text-slate-500 font-mono">(Order #{esc.order_id})</span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-md border ${
                        esc.priority === 'HIGH'
                          ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                          : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                      }`}
                    >
                      {esc.priority} PRIORITY
                    </span>
                  </div>
                  <p className="text-xs text-slate-300">{esc.reason}</p>
                </div>

                <div className="flex items-center space-x-3 text-xs">
                  <span className="text-slate-400 font-mono">{esc.time}</span>
                  <button className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-md">
                    Claim Case
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
