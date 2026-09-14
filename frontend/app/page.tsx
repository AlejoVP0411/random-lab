"use client";

import { useEffect, useMemo, useState } from "react";
import { Activity, ArrowDownUp, CheckCircle2, Dices, Download, RefreshCw, Save, ShieldCheck, Sparkles, XCircle } from "lucide-react";

type Method = "multiplicative" | "middle_product";
type Result = { name: string; statistic: number; critical_value: number; alpha: number; passed: boolean; message: string; details: { category: string; observed: number; expected: number; contribution: number }[] };
const API = process.env.NEXT_PUBLIC_API_URL ?? (typeof window !== "undefined" && window.location.hostname === "localhost" ? "http://localhost:8000" : "/api");

export default function Home() {
  const [method, setMethod] = useState<Method>("multiplicative");
  const [form, setForm] = useState({ count: "100", seed: "7", multiplier: "13", modulus: "127", seed_a: "1234", seed_b: "5678", digits: "4" });
  const [values, setValues] = useState<number[]>([]);
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTest, setActiveTest] = useState<"poker" | "runs">("poker");
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const numbers = useMemo(() => values.map((value, index) => ({ index: index + 1, value: value.toFixed(6) })), [values]);
  const update = (key: string, value: string) => setForm((old) => ({ ...old, [key]: value }));

  useEffect(() => {
    const saved = localStorage.getItem("randomlab-sample");
    if (!saved) return;
    try {
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed.values)) { setValues(parsed.values); setMethod(parsed.method); setSavedAt(parsed.savedAt); }
    } catch { localStorage.removeItem("randomlab-sample"); }
  }, []);

  function saveSample(download = false) {
    if (!values.length) return;
    const sample = { method, values, savedAt: new Date().toLocaleString("es-CO") };
    localStorage.setItem("randomlab-sample", JSON.stringify(sample));
    setSavedAt(sample.savedAt);
    if (download) {
      const url = URL.createObjectURL(new Blob([JSON.stringify(sample, null, 2)], { type: "application/json" }));
      const link = document.createElement("a"); link.href = url; link.download = "randomlab-muestra.json"; link.click(); URL.revokeObjectURL(url);
    }
  }

  async function generate() {
    setLoading(true); setError(""); setResult(null);
    const payload = method === "multiplicative"
      ? { method, count: +form.count, seed: +form.seed, multiplier: +form.multiplier, modulus: +form.modulus }
      : { method, count: +form.count, seed_a: +form.seed_a, seed_b: +form.seed_b, digits: +form.digits };
    try {
      const response = await fetch(`${API}/generate`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "No se pudo generar la muestra.");
      setValues(data.values);
    } catch (err) { setError(err instanceof Error ? err.message : "Error inesperado."); }
    finally { setLoading(false); }
  }
  async function runTest(test: "poker" | "runs") {
    if (!values.length) return;
    setActiveTest(test); setLoading(true); setError("");
    try {
      const response = await fetch(`${API}/test`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ test, values }) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "No se pudo ejecutar la prueba.");
      setResult(data);
    } catch (err) { setError(err instanceof Error ? err.message : "Error inesperado."); }
    finally { setLoading(false); }
  }
  const fields = method === "multiplicative"
    ? [["seed", "Semilla (X₀)"], ["multiplier", "Multiplicador (a)"], ["modulus", "Módulo (m)"]]
    : [["seed_a", "Semilla X₀"], ["seed_b", "Semilla X₁"], ["digits", "Dígitos centrales"]];
  return <main className="mx-auto max-w-7xl px-4 py-7 sm:px-6 lg:px-8">
    <header className="mb-8 flex items-center justify-between fade-in"><div><div className="mb-2 flex items-center gap-2 text-sm font-medium text-cyan-300"><Sparkles size={16}/> Laboratorio de simulación</div><h1 className="text-3xl font-bold tracking-tight sm:text-4xl">Random<span className="text-cyan-400">Lab</span></h1></div><div className="hidden items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1.5 text-xs text-emerald-300 sm:flex"><span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"/> API lista</div></header>
    <div className="grid gap-5 lg:grid-cols-[390px_1fr]">
      <section className="card h-fit fade-in"><div className="mb-5"><h2 className="text-lg font-semibold">Crear una muestra</h2><p className="mt-1 text-sm text-slate-400">Elige el método y configura sus parámetros.</p></div>
        <div className="mb-5 grid grid-cols-2 rounded-2xl bg-white/[.045] p-1"><button onClick={() => setMethod("multiplicative")} className={`rounded-xl px-3 py-2.5 text-xs font-medium transition ${method === "multiplicative" ? "bg-cyan-400 text-slate-950 shadow-lg" : "text-slate-400 hover:text-white"}`}>Congruencial<br/>multiplicativo</button><button onClick={() => setMethod("middle_product")} className={`rounded-xl px-3 py-2.5 text-xs font-medium transition ${method === "middle_product" ? "bg-cyan-400 text-slate-950 shadow-lg" : "text-slate-400 hover:text-white"}`}>No congruencial<br/>productos medios</button></div>
        <div className="space-y-4">{fields.map(([key, label]) => <label key={key} className="block text-xs font-medium text-slate-300">{label}<input type="number" value={form[key as keyof typeof form]} onChange={(e) => update(key, e.target.value)} className="mt-1.5" /></label>)}<label className="block text-xs font-medium text-slate-300">Cantidad de números<input type="number" min="2" max="10000" value={form.count} onChange={(e) => update("count", e.target.value)} className="mt-1.5" /></label></div>
        <button onClick={generate} disabled={loading} className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-cyan-400 to-teal-300 px-4 py-3 text-sm font-bold text-slate-950 transition hover:brightness-110 disabled:opacity-60"><RefreshCw size={16} className={loading ? "animate-spin" : ""}/>{values.length ? "Generar nueva muestra" : "Generar números"}</button>
      </section>
      <section className="space-y-5"><div className="card min-h-[245px] fade-in"><div className="mb-5 flex flex-wrap items-start justify-between gap-3"><div><h2 className="flex items-center gap-2 text-lg font-semibold"><Dices size={19} className="text-cyan-400"/> Muestra generada</h2><p className="mt-1 text-sm text-slate-400">{values.length ? `${values.length} valores uniformes en [0, 1)` : "Aún no has creado una muestra."}</p></div>{values.length > 0 && <div className="flex items-center gap-2"><button title="Guardar muestra" onClick={() => saveSample()} className="rounded-lg border border-white/10 p-2 text-slate-300 transition hover:bg-white/10"><Save size={15}/></button><button title="Descargar JSON" onClick={() => saveSample(true)} className="rounded-lg border border-white/10 p-2 text-slate-300 transition hover:bg-white/10"><Download size={15}/></button><span className="rounded-full bg-cyan-400/10 px-3 py-1 text-xs font-medium text-cyan-300">{method === "multiplicative" ? "Multiplicativo" : "Productos medios"}</span></div>}</div>
        {values.length ? <div className="grid grid-cols-2 gap-2 sm:grid-cols-4 xl:grid-cols-5">{numbers.slice(0, 20).map(({ index, value }) => <div key={index} className="rounded-xl border border-white/[.07] bg-white/[.035] px-3 py-2"><span className="text-[10px] uppercase tracking-wider text-slate-500">#{index}</span><div className="font-mono text-sm text-slate-200">{value}</div></div>)}</div> : <div className="flex h-32 flex-col items-center justify-center rounded-2xl border border-dashed border-white/10 text-slate-500"><Activity size={24} className="mb-2"/>Configura y genera para empezar</div>}
      {savedAt && values.length > 0 && <p className="mt-3 text-xs text-emerald-300">Muestra guardada localmente · {savedAt}</p>}</div>
      <div className="card fade-in"><div className="mb-5"><h2 className="flex items-center gap-2 text-lg font-semibold"><ShieldCheck size={19} className="text-violet-400"/> Validar aleatoriedad</h2><p className="mt-1 text-sm text-slate-400">Contrasta la muestra con pruebas estadísticas de nivel α = 0.05.</p></div><div className="grid gap-3 sm:grid-cols-2"><button disabled={!values.length || loading} onClick={() => runTest("poker")} className={`rounded-2xl border p-4 text-left transition disabled:opacity-40 ${activeTest === "poker" ? "border-violet-400/60 bg-violet-400/10" : "border-white/10 bg-white/[.03] hover:bg-white/[.06]"}`}><span className="mb-2 flex items-center gap-2 text-sm font-semibold"><Dices size={16} className="text-violet-300"/>Prueba de Póker</span><p className="text-xs leading-5 text-slate-400">Evalúa patrones de repetición en cinco dígitos.</p></button><button disabled={!values.length || loading} onClick={() => runTest("runs")} className={`rounded-2xl border p-4 text-left transition disabled:opacity-40 ${activeTest === "runs" ? "border-violet-400/60 bg-violet-400/10" : "border-white/10 bg-white/[.03] hover:bg-white/[.06]"}`}><span className="mb-2 flex items-center gap-2 text-sm font-semibold"><ArrowDownUp size={16} className="text-violet-300"/>Corridas A/B</span><p className="text-xs leading-5 text-slate-400">Comprueba el orden ascendente y descendente.</p></button></div></div>
      {result && <div className={`card fade-in border ${result.passed ? "border-emerald-400/30" : "border-rose-400/30"}`}><div className="flex gap-3"><div className={`mt-0.5 rounded-xl p-2 ${result.passed ? "bg-emerald-400/15 text-emerald-300" : "bg-rose-400/15 text-rose-300"}`}>{result.passed ? <CheckCircle2 size={22}/> : <XCircle size={22}/>}</div><div><h3 className="font-semibold">{result.name}</h3><p className={`mt-1 text-sm ${result.passed ? "text-emerald-200" : "text-rose-200"}`}>{result.message}</p></div></div><div className="mt-5 grid grid-cols-3 gap-2 text-center"><Metric label="Estadístico" value={result.statistic}/><Metric label="Valor crítico" value={result.critical_value}/><Metric label="Nivel α" value={result.alpha}/></div></div>}
      {error && <div className="rounded-xl border border-rose-400/30 bg-rose-400/10 px-4 py-3 text-sm text-rose-200">{error}</div>}
    </section></div><footer className="mt-8 text-center text-xs text-slate-600">Generación pseudoaleatoria · Pruebas de hipótesis estadísticas</footer></main>;
}
function Metric({ label, value }: { label: string; value: number }) { return <div className="rounded-xl bg-white/[.045] p-3"><div className="text-[10px] uppercase tracking-wider text-slate-500">{label}</div><div className="mt-1 font-mono text-sm text-slate-200">{value}</div></div>; }
