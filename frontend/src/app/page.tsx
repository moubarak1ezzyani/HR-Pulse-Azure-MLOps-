"use client";

import { useState } from "react";

export default function Home() {
  // --- LOGIC REMAINS 100% IDENTICAL ---
  const [description, setDescription] = useState("");
  const [sizeAvg, setSizeAvg] = useState("");
  const [revenueAvg, setRevenueAvg] = useState("");
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cleaned_description: description,
          Size_Avg: parseFloat(sizeAvg),
          Revenue_Avg_Millions: parseFloat(revenueAvg),
        }),
      });
      if (!response.ok) throw new Error("Error communicating with the ML model.");
      const data = await response.json();
      setPrediction(data.prediction);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    // Background with animated gradient and futuristic grain
    <main className="min-h-screen bg-[#0f172a] bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-blue-900 via-slate-900 to-black flex items-center justify-center p-4 font-sans">
      
      {/* Glassmorphism Main Card */}
      <div className="relative max-w-2xl w-full">
        <div className="absolute -top-20 -left-20 w-64 h-64 bg-blue-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute -bottom-20 -right-20 w-64 h-64 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>

        <div className="relative backdrop-blur-xl bg-white/10 p-8 md:p-12 rounded-[2rem] border border-white/20 shadow-2xl overflow-hidden">
          
          {/* Innovative Header */}
          <header className="text-center mb-10">
            <div className="inline-block px-4 py-1.5 mb-4 rounded-full border border-blue-400/30 bg-blue-400/10 text-blue-300 text-xs font-semibold uppercase tracking-widest">
              ML Engine v2.0
            </div>
            <h1 className="text-4xl md:text-5xl font-black text-white mb-4 tracking-tight">
              HR Pulse <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">AI</span>
            </h1>
            <p className="text-slate-400 text-base max-w-sm mx-auto">
              Optimize your recruitment strategy with the predictive power of Machine Learning.
            </p>
          </header>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Input Description : Neon Focus Style */}
            <div className="group">
              <label className="block text-xs font-bold text-slate-400 uppercase mb-2 ml-1 tracking-wider">
                Expertise & Role
              </label>
              <textarea
                required
                className="w-full bg-slate-800/50 border border-slate-700 rounded-2xl p-4 text-white placeholder-slate-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none resize-none group-hover:border-slate-500"
                rows={3}
                placeholder="What are the key skills required? (e.g., Python, SQL, Machine Learning)"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            {/* Inputs Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="group">
                <label className="block text-xs font-bold text-slate-400 uppercase mb-2 ml-1 tracking-wider">
                  Company Size
                </label>
                <input
                  type="number"
                  required
                  className="w-full bg-slate-800/50 border border-slate-700 rounded-2xl p-4 text-white placeholder-slate-500 focus:ring-2 focus:ring-blue-500 transition-all outline-none group-hover:border-slate-500"
                  placeholder="e.g., 7500 employees"
                  value={sizeAvg}
                  onChange={(e) => setSizeAvg(e.target.value)}
                />
              </div>
              <div className="group">
                <label className="block text-xs font-bold text-slate-400 uppercase mb-2 ml-1 tracking-wider">
                  Annual Revenue ($M)
                </label>
                <input
                  type="number"
                  required
                  className="w-full bg-slate-800/50 border border-slate-700 rounded-2xl p-4 text-white placeholder-slate-500 focus:ring-2 focus:ring-blue-500 transition-all outline-none group-hover:border-slate-500"
                  placeholder="e.g., 1200"
                  value={revenueAvg}
                  onChange={(e) => setRevenueAvg(e.target.value)}
                />
              </div>
            </div>

            {/* Pulsing Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="relative w-full group overflow-hidden rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 p-px font-bold text-white transition-all hover:shadow-[0_0_20px_rgba(37,99,235,0.4)] disabled:opacity-50"
            >
              <div className="relative flex items-center justify-center gap-2 rounded-2xl bg-slate-900 px-8 py-4 transition-all group-hover:bg-transparent">
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span className="tracking-wide">Calculating probabilities...</span>
                  </>
                ) : (
                  <span className="tracking-wide">Generate Prediction</span>
                )}
              </div>
            </button>
          </form>

          {/* Error Alerts */}
          {error && (
            <div className="mt-8 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-400 text-sm text-center animate-pulse">
              {error}
            </div>
          )}

          {/* High-Tech Result 🎉 */}
          {prediction !== null && (
            <div className="mt-10 relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-green-400 to-emerald-500 rounded-3xl blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
              <div className="relative bg-slate-900/80 border border-green-500/30 p-8 rounded-3xl text-center">
                <p className="text-green-400/70 text-[0.65rem] uppercase font-black tracking-[0.3em] mb-3">
                  AI Estimation: Validated
                </p>
                <div className="flex items-center justify-center gap-3">
                   <span className="text-5xl md:text-6xl font-black text-white tracking-tighter">
                    {prediction.toLocaleString('en-US')}
                  </span>
                  <span className="text-2xl font-light text-green-400 self-end mb-2">
                    K $ / year
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Discreet Footer */}
        <p className="text-center mt-8 text-slate-500 text-[10px] uppercase tracking-[0.2em]">
          Powered by MAE
        </p>
      </div>
    </main>
  );
}