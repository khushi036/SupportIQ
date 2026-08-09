import React, { useState } from 'react';
import { BookOpen, FileText, ShieldCheck } from 'lucide-react';

const POLICIES = [
  {
    id: 'shipping',
    title: 'Shipping & Delivery Policy (v2.4)',
    filename: 'shipping_delivery.md',
    content: `## Delivery Timelines
- Standard Shipping: 3 to 5 business days within India.
- Express Delivery: 1 to 2 business days for select metro cities (Delhi NCR, Mumbai, Bengaluru).
- Same-Day Delivery: Orders placed before 11:00 AM IST are eligible for same-day delivery by 8:00 PM IST.

## Order Tracking
Customers receive a tracking number via SMS and Email once the shipment leaves our warehouse. You can check your real-time order status by providing your 5-digit Order ID to our support agent.`
  },
  {
    id: 'returns',
    title: 'Returns & Refunds Policy (v3.1)',
    filename: 'returns_refunds.md',
    content: `## Return Window
Items can be returned within 14 days of delivery. To be eligible for a full refund, items must be unused, in their original packaging, and with all tags intact.

## Damaged or Defective Goods
If you receive a damaged, broken, or defective product:
1. Report the issue within 48 hours of delivery.
2. Provide photos of the damaged item and packaging.
3. Because damaged goods refunds require human verification, our system will automatically open a High-Priority Support Ticket for supervisor review.
4. Refunds for damaged items over $100 require manual supervisor approval under company compliance rules.`
  },
  {
    id: 'cancellations',
    title: 'Order Cancellation Policy (v1.8)',
    filename: 'cancellations.md',
    content: `## Cancellation Rules
- Orders in PROCESSING status can be cancelled immediately for a 100% refund.
- Orders in SHIPPED or OUT_FOR_DELIVERY status cannot be cancelled automatically. Customers may refuse delivery at the doorstep or initiate a return after receiving the product.`
  },
  {
    id: 'warranty',
    title: 'Product Warranty & Guarantee Policy (v2.0)',
    filename: 'warranty_guarantee.md',
    content: `## Standard Warranty
All electronic accessories and gadgets sold on SupportIQ carry a standard 1-Year Manufacturer Warranty covering mechanical and electrical defects.

## Warranty Exclusions
The warranty does not cover physical damage caused by drops or liquid spills.`
  }
];

export const PolicyViewer: React.FC = () => {
  const [selectedPolicy, setSelectedPolicy] = useState(POLICIES[0]);

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6 h-[calc(100vh-5rem)] overflow-y-auto">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-100 flex items-center space-x-3">
          <BookOpen className="h-7 w-7 text-indigo-400" />
          <span>Knowledge Base RAG Policy Corpus</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Grounding documents referenced by SupportIQ agent to generate 100% factual, cited responses.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        
        {/* Sidebar Selection */}
        <div className="space-y-2">
          {POLICIES.map((p) => (
            <button
              key={p.id}
              onClick={() => setSelectedPolicy(p)}
              className={`w-full text-left p-3.5 rounded-xl text-xs font-bold transition-all flex items-center space-x-2.5 ${
                selectedPolicy.id === p.id
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'bg-slate-900/80 text-slate-400 hover:bg-slate-800 hover:text-slate-200 border border-slate-800'
              }`}
            >
              <FileText className="h-4 w-4" />
              <span>{p.title}</span>
            </button>
          ))}
        </div>

        {/* Document Display Panel */}
        <div className="md:col-span-3 glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <h2 className="text-lg font-bold text-slate-200">{selectedPolicy.title}</h2>
              <span className="text-xs font-mono text-indigo-400">Path: backend/knowledge/{selectedPolicy.filename}</span>
            </div>
            <span className="px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold rounded-lg flex items-center space-x-1">
              <ShieldCheck className="h-3.5 w-3.5" />
              <span>RAG Vector Indexed</span>
            </span>
          </div>

          <div className="prose prose-invert max-w-none text-slate-300 text-sm whitespace-pre-line leading-relaxed font-sans bg-slate-950 p-6 rounded-xl border border-slate-800/80">
            {selectedPolicy.content}
          </div>
        </div>

      </div>

    </div>
  );
};
