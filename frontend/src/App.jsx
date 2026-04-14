
// import { useState, useEffect, useCallback, useRef } from "react";
// import axios from "axios";
// // ─── CONSTANTS ────────────────────────────────────────────────────────────────
// const api = axios.create({ baseURL: "/api", timeout: 30000000 });
// const runPipelineApi     = (body) => api.post("/run-pipeline", body);
// const submitHitlDecision = (b)    => api.post("/hitl/decision", b);
// const submitBulkHitl     = (b)    => api.post("/hitl/bulk", b);
// const getAuditLog        = (id)   => api.get(`/audit/${id}`);
// const getHitlQueue       = (id)   => api.get(`/hitl/${id}`);
// const fetchDbTrades      = ()     => api.get("/sources/db");
// const fetchCsvTrades     = ()     => api.get("/sources/csv");
// const fetchAllTrades = () => api.get("/sources/all");

// // ─── SAMPLE (UI source) ───────────────────────────────────────────────────────
// const UI_SAMPLE = [
//   { trade_id:"T5001_PASS", trade_datetime:"2024-03-10T09:00:00Z", isin:"US0378331005",
//     executing_entity_lei:"5493001KJTIIGC8Y1R12", buyer_lei:"213800D1EI4B9WTWWD28",
//     seller_lei:"529900T8BM49AURSDO55", price:"180", currency:"USD", quantity:"30",
//     venue:"XNAS", notional_amount:"5400", report_status:"NEWT", instrument_type:"EQUITY",
//     source_channel:"ui" },
//   { trade_id:"T5002_HITL", trade_datetime:"2024-03-10T10:00:00Z", isin:"US02079K3059",
//     executing_entity_lei:"5493001KJTIIGC8Y1R12", buyer_lei:"213800D1EI4B9WTWWD28",
//     seller_lei:"213800D1EI4B9WTWWD28", price:"150", currency:"USD", quantity:"70",
//     venue:"XNAS", notional_amount:"10500", report_status:"NEWT", instrument_type:"EQUITY",
//     source_channel:"ui" },
//   { trade_id:"T5003_FAIL", trade_datetime:"", isin:"INVALID123",
//     executing_entity_lei:"BAD_LEI", buyer_lei:"213800D1EI4B9WTWWD28",
//     seller_lei:"529900T8BM49AURSDO55", price:"-50", currency:"XXX", quantity:"-10",
//     venue:"UNKOWN", notional_amount:"500", report_status:"WRONG", instrument_type:"EQUITY",
//     source_channel:"ui" },
// ];

// // ─── DESIGN TOKENS ────────────────────────────────────────────────────────────
// const C = {
//   blue: "#0056C5", blueHov: "#0047A8", blueDark: "#003D8F", blueTint: "#EBF2FF",
//   bg: "#F4F6F9", surface: "#FFFFFF", surfaceAlt: "#F8FAFC",
//   border: "rgba(15,23,42,0.08)", borderMid: "rgba(15,23,42,0.13)",
//   ink: "#0F172A", inkMid: "#334155", inkMuted: "#64748B", inkFaint: "#94A3B8",
//   green: "#0F7B52", greenTint: "#ECFDF5", greenBorder: "rgba(15,123,82,0.2)",
//   amber: "#B45309", amberTint: "#FFFBEB", amberBorder: "rgba(180,83,9,0.2)",
//   red: "#BE123C", redTint: "#FFF1F2", redBorder: "rgba(190,18,60,0.2)",
//   violet: "#6D28D9", violetTint: "#F5F3FF", violetBorder: "rgba(109,40,217,0.18)",
//   cyan: "#0E7490", cyanTint: "#ECFEFF",
//   warning: "#92400E",
// };
// const FONT = {
//   display: "'Plus Jakarta Sans','DM Sans',system-ui,sans-serif",
//   body: "'DM Sans',system-ui,sans-serif",
//   mono: "'DM Mono','SF Mono',monospace",
// };
// // ─── ICONS ────────────────────────────────────────────────────────────────────
// const mk = (children, vb = "0 0 24 24") => (p) => (
//   <svg {...p} viewBox={vb} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{children}</svg>
// );
// const Ic = {
//   Home: mk(<><rect x="3" y="3" width="7" height="7" rx="1.5" /><rect x="14" y="3" width="7" height="7" rx="1.5" /><rect x="3" y="14" width="7" height="7" rx="1.5" /><rect x="14" y="14" width="7" height="7" rx="1.5" /></>),
//   Shield: mk(<><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></>),
//   Alert: mk(<><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><circle cx="12" cy="17" r=".5" fill="currentColor" /></>),
//   Users: mk(<><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" /></>),
//   Audit: mk(<><path d="M9 11l3 3L22 4" /><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" /></>),
//   Report: mk(<><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" /><polyline points="14,2 14,8 20,8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /></>),
//   Upload: mk(<><polyline points="16,16 12,12 8,16" /><line x1="12" y1="12" x2="12" y2="21" /><path d="M20.39 18.39A5 5 0 0018 9h-1.26A8 8 0 103 16.3" /></>),
//   Check: mk(<polyline points="20,6 9,17 4,12" strokeWidth="2.5" />),
//   X: mk(<><line x1="18" y1="6" x2="6" y2="18" strokeWidth="2.5" /><line x1="6" y1="6" x2="18" y2="18" strokeWidth="2.5" /></>),
//   Edit: mk(<><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" /><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" /></>),
//   Refresh: mk(<><polyline points="23,4 23,10 17,10" /><path d="M20.49 15a9 9 0 11-2.12-9.36L23 10" /></>),
//   Download: mk(<><polyline points="8,17 12,21 16,17" /><line x1="12" y1="12" x2="12" y2="21" /><path d="M20.88 18.09A5 5 0 0018 9h-1.26A8 8 0 103 16.3" /></>),
//   ChevR: mk(<polyline points="9,18 15,12 9,6" strokeWidth="2" />),
//   ChevD: mk(<polyline points="6,9 12,15 18,9" strokeWidth="2" />),
//   Chat: mk(
//   <>
//     <path d="M21 15a4 4 0 0 1-4 4H8l-5 4V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z" />
//   </>
// ),
//   Menu: mk(<><line x1="3" y1="12" x2="21" y2="12" strokeWidth="2" /><line x1="3" y1="6" x2="21" y2="6" strokeWidth="2" /><line x1="3" y1="18" x2="21" y2="18" strokeWidth="2" /></>),
//   Wand: mk(<><path d="M15 4V2M15 16v-2M8 9h2M20 9h2M17.8 11.8L19.2 13.2M15 9h0M17.8 6.2L19.2 4.8M3 21l9-9M12.2 6.2L10.8 4.8" /></>),
//   Layer: mk(<><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2" /><line x1="12" y1="22" x2="12" y2="15.5" /><polyline points="22 8.5 12 15.5 2 8.5" /></>),
//   Copy: mk(<><rect x="9" y="9" width="13" height="13" rx="2" /><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" /></>),
//   Info: mk(<><circle cx="12" cy="12" r="10" /><line x1="12" y1="16" x2="12" y2="12" /><line x1="12" y1="8" x2="12.01" y2="8" /></>),
//   Zap: mk(<><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" /></>),
//   Plus: mk(<><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></>),
// };
// // ─── PRIMITIVES ───────────────────────────────────────────────────────────────
// function Spinner({ size = 16, color = C.blue }) {
//   return <span style={{ display: "inline-block", width: size, height: size, border: `2px solid ${color}25`, borderTopColor: color, borderRadius: "50%", animation: "spin .75s linear infinite", flexShrink: 0 }} />;
// }

// // ─── FIX 1 & 2: Updated SEV mapping — FAIL added ─────────────────────────────
// const SEV = {
//   PASS: [C.greenTint, C.green, C.greenBorder],
//   APPROVED: [C.greenTint, C.green, C.greenBorder],
//   true: [C.greenTint, C.green, C.greenBorder],
//   LOW: [C.greenTint, C.green, C.greenBorder],
//   HITL: [C.amberTint, C.amber, C.amberBorder],
//   PENDING: [C.amberTint, C.amber, C.amberBorder],
//   MEDIUM: [C.amberTint, C.amber, C.amberBorder],
//   FAIL: [C.redTint, C.red, C.redBorder],   // ✅ FIX 2: FAIL added
//   HIGH: [C.redTint, C.red, C.redBorder],
//   CRITICAL: [C.redTint, C.red, C.redBorder],
//   REJECTED: [C.redTint, C.red, C.redBorder],
//   false: [C.redTint, C.red, C.redBorder],
//   APPLIED: [C.violetTint, C.violet, C.violetBorder],
//   MODIFIED: [C.blueTint, C.blue, "rgba(0,86,197,.2)"],
//   NEWT: [C.blueTint, C.blue, "rgba(0,86,197,.2)"],
//   AMND: [C.cyanTint, C.cyan, "rgba(14,116,144,.2)"],
//   NONE: [C.surfaceAlt, C.inkFaint, C.border],
// };

// function Badge({ status, size = "sm", pulse = false }) {
//   const [bg, fg, bd] = SEV[String(status)] || [C.surfaceAlt, C.inkMuted, C.border];
//   const fs = size === "lg" ? 12 : size === "xs" ? 10 : 11;
//   const px = size === "lg" ? 10 : size === "xs" ? 6 : 8;
//   return (
//     <span style={{ display: "inline-flex", alignItems: "center", gap: 5, background: bg, color: fg, border: `1px solid ${bd}`, borderRadius: size === "lg" ? 4 : 2, padding: `${size === "lg" ? 4 : 2}px ${px}px`, fontSize: fs, fontWeight: 700, whiteSpace: "nowrap", fontFamily: FONT.mono, letterSpacing: ".03em" }}>
//       <span style={{ width: 5, height: 5, borderRadius: "50%", background: fg, flexShrink: 0, ...(pulse ? { animation: "pulseRing 1.5s ease infinite" } : {}) }} />
//       {String(status).toUpperCase()}
//     </span>
//   );
// }

// // ─── FIX 1: Updated ConfBar — status-aware coloring with FAIL support ─────────
// function ConfBar({ value, status, compact = false }) {
//   const pct = Math.max(0, Math.min(100, Math.round((value || 0) * 100)));
//   let color;
//   if (status === "PASS" || status === "APPROVED" || status === true) {
//     color = C.green;
//   } else if (status === "HITL" || status === "PENDING") {
//     color = C.amber;
//   } else if (status === "FAIL" || status === "REJECTED" || status === false) {
//     color = C.red;
//   } else {
//     // Fallback: derive from percentage when status unknown
//     color = pct >= 70 ? C.green : pct >= 40 ? C.amber : C.red;
//   }
//   return (
//     <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
//       <div style={{ flex: 1, height: compact ? 4 : 6, background: C.border, borderRadius: 4, overflow: "hidden" }}>
//         <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 4 }} />
//       </div>
//       <span style={{ fontSize: 11, color: color, minWidth: 28, textAlign: "right", fontFamily: FONT.mono, fontWeight: 700 }}>
//         {pct}%
//       </span>
//     </div>
//   );
// }

// function Btn({ children, variant = "primary", onClick, disabled, icon: Icon, size = "md", full = false, loading = false }) {
//   const [hov, sH] = useState(false);
//   const V = {
//     primary: { bg: hov && !disabled ? C.blueHov : C.blue, fg: "#fff", bd: "none" },
//     secondary: { bg: hov && !disabled ? C.bg : C.surface, fg: C.inkMid, bd: `1px solid ${C.borderMid}` },
//     ghost: { bg: hov && !disabled ? C.bg : "transparent", fg: C.blue, bd: `1px solid ${C.borderMid}` },
//     danger: { bg: hov && !disabled ? "#9F1239" : C.red, fg: "#fff", bd: "none" },
//     success: { bg: hov && !disabled ? "#065F46" : C.green, fg: "#fff", bd: "none" },
//     amber: { bg: hov && !disabled ? "#92400E" : C.amber, fg: "#fff", bd: "none" },
//     violet: { bg: hov && !disabled ? "#5B21B6" : C.violet, fg: "#fff", bd: "none" },
//   }[variant] || {};
//   const sz = size === "sm" ? { p: "5px 12px", fs: 12 } : size === "xs" ? { p: "3px 9px", fs: 11 } : { p: "8px 16px", fs: 13 };
//   return (
//     <button onClick={disabled ? undefined : onClick} onMouseEnter={() => sH(true)} onMouseLeave={() => sH(false)} disabled={disabled}
//       style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: sz.p, fontSize: sz.fs, fontWeight: 600, borderRadius: 7, border: V.bd, background: V.bg, color: V.fg, cursor: disabled ? "not-allowed" : "pointer", opacity: disabled ? .55 : 1, transition: "all .14s", fontFamily: FONT.body, width: full ? "100%" : "auto", justifyContent: "center" }}>
//       {loading ? <Spinner size={size === "sm" ? 12 : 14} color={V.fg} /> : Icon ? <Icon style={{ width: size === "sm" ? 13 : 15, height: size === "sm" ? 13 : 15, flexShrink: 0 }} /> : null}
//       {children}
//     </button>
//   );
// }
// function Card({ children, style, accent, noPad = false, onClick }) {
//   const [hov, sH] = useState(false);
//   return (
//     <div onClick={onClick} onMouseEnter={() => onClick && sH(true)} onMouseLeave={() => onClick && sH(false)}
//       style={{ background: C.surface, borderRadius: 12, border: `1px solid ${C.border}`, boxShadow: hov ? "0 8px 24px rgba(15,23,42,.09)" : "0 1px 4px rgba(15,23,42,.04)", transition: "box-shadow .2s,transform .15s", transform: hov && onClick ? "translateY(-1px)" : "none", cursor: onClick ? "pointer" : "default", overflow: "hidden", position: "relative", ...(accent && { borderTop: `3px solid ${accent}` }), ...style }}>
//       {children}
//     </div>
//   );
// }
// function CardHeader({ title, sub, right, border = true }) {
//   return (
//     <div style={{ padding: "13px 18px", ...(border && { borderBottom: `1px solid ${C.border}` }), display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
//       <div>
//         <p style={{ margin: 0, fontSize: 13, fontWeight: 700, color: C.ink, fontFamily: FONT.display }}>{title}</p>
//         {sub && <p style={{ margin: "2px 0 0", fontSize: 11, color: C.inkFaint }}>{sub}</p>}
//       </div>
//       {right && <div style={{ flexShrink: 0 }}>{right}</div>}
//     </div>
//   );
// }
// function StatCard({ label, value, sub, accent, icon: Icon }) {
//   return (
//     <Card style={{ padding: "18px 20px" }} accent={accent}>
//       <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
//         <div style={{ flex: 1, minWidth: 0 }}>
//           <p style={{ margin: 0, fontSize: 10, fontWeight: 700, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".08em" }}>{label}</p>
//           <p style={{ margin: "7px 0 0", fontSize: 28, fontWeight: 800, color: C.ink, fontFamily: FONT.display, lineHeight: 1, letterSpacing: "-.02em" }}>{value ?? '—'}</p>
//           {sub && <p style={{ margin: "5px 0 0", fontSize: 11, color: C.inkMuted }}>{sub}</p>}
//         </div>
//         {Icon && <div style={{ width: 38, height: 38, borderRadius: 10, background: accent + "18", display: "flex", alignItems: "center", justifyContent: "center", color: accent, flexShrink: 0 }}><Icon style={{ width: 18, height: 18 }} /></div>}
//       </div>
//     </Card>
//   );
// }
// function Empty({ icon: Icon = Ic.Layer, title, sub }) {
//   return (
//     <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "64px 24px", textAlign: "center" }}>
//       <div style={{ width: 52, height: 52, borderRadius: 14, background: C.bg, border: `1px solid ${C.border}`, display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 14 }}>
//         <Icon style={{ width: 22, height: 22, color: C.inkFaint }} />
//       </div>
//       <p style={{ margin: 0, fontSize: 14, fontWeight: 700, color: C.ink, fontFamily: FONT.display }}>{title}</p>
//       {sub && <p style={{ margin: "6px 0 0", fontSize: 12, color: C.inkMuted, maxWidth: 320 }}>{sub}</p>}
//     </div>
//   );
// }
// function SectionHeader({ title, sub, actions }) {
//   return (
//     <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 20, gap: 16 }}>
//       <div>
//         <h2 style={{ margin: 0, fontSize: 20, fontWeight: 800, color: C.ink, fontFamily: FONT.display, letterSpacing: "-.02em" }}>{title}</h2>
//         {sub && <p style={{ margin: "5px 0 0", fontSize: 13, color: C.inkMuted }}>{sub}</p>}
//       </div>
//       {actions && <div style={{ display: "flex", gap: 8, flexShrink: 0, flexWrap: "wrap", justifyContent: "flex-end" }}>{actions}</div>}
//     </div>
//   );
// }
// function Pill({ label, color = C.blue }) {
//   return (
//     <span style={{ display: "inline-flex", alignItems: "center", gap: 5, padding: "3px 10px", background: color + "15", color, borderRadius: 20, fontSize: 11, fontWeight: 700, letterSpacing: ".04em", border: `1px solid ${color}20`, fontFamily: FONT.mono }}>
//       <span style={{ width: 5, height: 5, borderRadius: "50%", background: color, animation: "pulseRing 2s ease infinite" }} />
//       {label}
//     </span>
//   );
// }
// // ─── MODIFY MODAL ─────────────────────────────────────────────────────────────
// function ModifyModal({ trade, runId, onClose, onSuccess }) {
//   const FIELDS = ["isin", "executing_entity_lei", "buyer_lei", "seller_lei", "price", "currency", "quantity", "venue", "notional_amount", "report_status", "instrument_type", "trade_datetime"];
//   const [fields, setFields] = useState(() => { const o = {}; FIELDS.forEach(k => { if (trade[k] !== undefined) o[k] = String(trade[k]); }); return o; });
//   const [note, setNote] = useState(""); const [busy, setBusy] = useState(false); const [err, setErr] = useState(null);
//   const submit = async () => {
//     setBusy(true); setErr(null);
//     try { const res = await submitHitlDecision({ run_id: runId, trade_id: trade.trade_id, decision: "MODIFIED", modified_fields: { ...fields, trade_id: trade.trade_id }, reviewer_note: note }); onSuccess(res.data); }
//     catch (e) { setErr(e.response?.data?.detail || e.message); setBusy(false); }
//   };
//   return (
//     <div style={{ position: "fixed", inset: 0, background: "rgba(15,23,42,.55)", backdropFilter: "blur(8px)", zIndex: 1000, display: "flex", alignItems: "center", justifyContent: "center", padding: 16 }}>
//       <div style={{ background: C.surface, borderRadius: 16, width: "100%", maxWidth: 660, maxHeight: "92vh", overflowY: "auto", boxShadow: "0 32px 80px rgba(15,23,42,.22)", border: `1px solid ${C.border}` }}>
//         <div style={{ padding: "18px 22px", borderBottom: `1px solid ${C.border}`, display: "flex", justifyContent: "space-between", alignItems: "center", position: "sticky", top: 0, background: C.surface, zIndex: 1 }}>
//           <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
//             <div style={{ width: 32, height: 32, borderRadius: 8, background: C.amberTint, border: `1px solid ${C.amberBorder}`, display: "flex", alignItems: "center", justifyContent: "center", color: C.amber }}><Ic.Edit style={{ width: 15, height: 15 }} /></div>
//             <div><h3 style={{ margin: 0, fontSize: 15, fontWeight: 800, color: C.ink, fontFamily: FONT.display }}>Modify Trade Fields</h3><p style={{ margin: 0, fontSize: 11, color: C.inkFaint, fontFamily: FONT.mono }}>{trade.trade_id}</p></div>
//           </div>
//           <button onClick={onClose} style={{ background: C.bg, border: `1px solid ${C.border}`, borderRadius: 7, cursor: "pointer", color: C.inkMuted, padding: 6, display: "flex" }}><Ic.X style={{ width: 15, height: 15 }} /></button>
//         </div>
//         <div style={{ padding: "20px 22px" }}>
//           <div style={{ background: C.amberTint, border: `1px solid ${C.amberBorder}`, borderRadius: 8, padding: "10px 14px", marginBottom: 18, display: "flex", gap: 8 }}>
//             <Ic.Info style={{ width: 14, height: 14, color: C.amber, flexShrink: 0, marginTop: 1 }} />
//             <p style={{ margin: 0, fontSize: 12, color: C.warning, lineHeight: 1.5 }}>Modifying and re-running will reprocess this trade through the full pipeline. Original values are preserved in the audit trail.</p>
//           </div>
//           <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 16 }}>
//             {Object.entries(fields).map(([k, v]) => (
//               <div key={k}>
//                 <label style={{ display: "block", fontSize: 10, fontWeight: 700, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".08em", marginBottom: 5 }}>{k.replace(/_/g, " ")}</label>
//                 <input value={v} onChange={e => setFields(f => ({ ...f, [k]: e.target.value }))}
//                   onFocus={e => { e.target.style.borderColor = C.blue; e.target.style.boxShadow = `0 0 0 3px ${C.blue}15`; }}
//                   onBlur={e => { e.target.style.borderColor = C.border; e.target.style.boxShadow = "none"; }}
//                   style={{ width: "100%", padding: "8px 11px", border: `1px solid ${C.border}`, borderRadius: 7, fontSize: 12, color: C.ink, background: C.surfaceAlt, outline: "none", fontFamily: FONT.mono, boxSizing: "border-box", transition: "border-color .14s,box-shadow .14s" }} />
//               </div>
//             ))}
//           </div>
//           <label style={{ display: "block", fontSize: 10, fontWeight: 700, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".08em", marginBottom: 5 }}>Reviewer Note</label>
//           <textarea value={note} onChange={e => setNote(e.target.value)} rows={3} placeholder="Explain the correction rationale…"
//             style={{ width: "100%", padding: "10px 12px", border: `1px solid ${C.border}`, borderRadius: 7, fontSize: 13, color: C.ink, background: C.surfaceAlt, outline: "none", resize: "vertical", fontFamily: FONT.body, boxSizing: "border-box" }} />
//           {err && <div style={{ marginTop: 12, padding: "10px 13px", background: C.redTint, border: `1px solid ${C.redBorder}`, borderRadius: 7, fontSize: 12, color: C.red, display: "flex", gap: 8 }}><Ic.Alert style={{ width: 13, height: 13, flexShrink: 0 }} />{err}</div>}
//         </div>
//         <div style={{ padding: "14px 22px", borderTop: `1px solid ${C.border}`, display: "flex", gap: 8, justifyContent: "flex-end", background: C.surfaceAlt }}>
//           <Btn variant="secondary" onClick={onClose}>Cancel</Btn>
//           <Btn variant="amber" onClick={submit} disabled={busy} icon={busy ? null : Ic.Refresh} loading={busy}>{busy ? "Re-processing…" : "Submit & Re-run Pipeline"}</Btn>
//         </div>
//       </div>
//     </div>
//   );
// }
// // ─── INPUT TAB ────────────────────────────────────────────────────────────────
// const SAMPLE = JSON.stringify([
//   { trade_id: "T5001_PASS", trade_datetime: "2024-03-10T09:00:00Z", isin: "US0378331005", executing_entity_lei: "5493001KJTIIGC8Y1R12", buyer_lei: "213800D1EI4B9WTWWD28", seller_lei: "529900T8BM49AURSDO55", price: "180", currency: "USD", quantity: "30", venue: "XNAS", notional_amount: "5400", report_status: "NEWT", instrument_type: "EQUITY" },
//   { trade_id: "T5002_HITL", trade_datetime: "2024-03-10T10:00:00Z", isin: "US02079K3059", executing_entity_lei: "5493001KJTIIGC8Y1R12", buyer_lei: "213800D1EI4B9WTWWD28", seller_lei: "213800D1EI4B9WTWWD28", price: "150", currency: "USD", quantity: "70", venue: "XNAS", notional_amount: "10500", report_status: "NEWT", instrument_type: "EQUITY" },
//   { trade_id: "T5003_FAIL", trade_datetime: "", isin: "INVALID123", executing_entity_lei: "BAD_LEI", buyer_lei: "213800D1EI4B9WTWWD28", seller_lei: "529900T8BM49AURSDO55", price: "-50", currency: "XXX", quantity: "-10", venue: "UNKOWN", notional_amount: "500", report_status: "WRONG", instrument_type: "EQUITY" },
// ], null, 2);
// const STEPS = [
//   "Ingesting trade data…",
//   "Enriching ISIN & LEI references…",
//   "Running validation, risk & compliance in parallel…",
//   "Decision engine routing…",
//   "Generating compliance report…",
// ];

// // ─── SOURCE CONFIG ────────────────────────────────────────────────────────────
// const SOURCES = [
//   {
//     key: "ui",
//     label: "UI Input",
//     icon: Ic.Upload,
//     color: C.blue,
//     description: "Paste JSON directly — manual trade entry from the analyst desk.",
//   },
//   {
//     key: "db",
//     label: "Trading System DB",
//     icon: Ic.Layer,
//     color: C.green,
//     description: "Pre-loaded trades from the in-memory trading system database (simulates overnight batch from core banking).",
//   },
//   {
//     key: "csv",
//     label: "CSV File",
//     icon: Ic.Report,
//     color: C.violet,
//     description: "Trades read from a CSV file on disk (simulates file drop from an upstream reporting system).",
//   },
// ];
// // ─── Merge TAB ────────────────────────────────────────────────────────────────

// function MergeTab({ onComplete }) {
//   const [loading, setLoading] = useState(false);
//   const [running, setRunning] = useState(false);
//   const [err, setErr] = useState(null);

//   const [sourceFilter, setSourceFilter] = useState("all");
//   const [allTrades, setAllTrades] = useState([]);
//   const [selected, setSelected] = useState(new Set());

//   const [mergedJson, setMergedJson] = useState("");

//   const loadMerged = useCallback(async () => {
//     setLoading(true);
//     setErr(null);
//     try {
//       const res = await fetchAllTrades();
//       const trades = res.data?.trades || [];
//       setAllTrades(trades);
//       setSelected(new Set());
//       setMergedJson(JSON.stringify(trades, null, 2));
//     } catch (e) {
//       setErr(e.response?.data?.detail || e.message || "Failed to load merged trades");
//     } finally {
//       setLoading(false);
//     }
//   }, []);

//   useEffect(() => {
//     loadMerged();
//   }, [loadMerged]);

//   const filteredTrades =
//     sourceFilter === "all"
//       ? allTrades
//       : allTrades.filter(t => (t.source_channel || "") === sourceFilter);

//   const toggleOne = (tradeId) => {
//     setSelected(prev => {
//       const next = new Set(prev);
//       if (next.has(tradeId)) next.delete(tradeId);
//       else next.add(tradeId);
//       return next;
//     });
//   };

//   const toggleAll = () => {
//     const ids = filteredTrades.map(t => t.trade_id);
//     const allSelected = ids.length > 0 && ids.every(id => selected.has(id));

//     setSelected(prev => {
//       const next = new Set(prev);
//       if (allSelected) {
//         ids.forEach(id => next.delete(id));
//       } else {
//         ids.forEach(id => next.add(id));
//       }
//       return next;
//     });
//   };

//   const loadSelectedIntoJson = () => {
//     const tradesToLoad = filteredTrades.filter(t => selected.has(t.trade_id));
//     const payload = tradesToLoad.length ? tradesToLoad : filteredTrades;
//     setMergedJson(JSON.stringify(payload, null, 2));
//   };

//   const runPipelineFromMergedJson = async () => {
//     setRunning(true);
//     setErr(null);

//     try {
//       let trades = [];

//       if (selected.size > 0) {
//         trades = filteredTrades.filter(t => selected.has(t.trade_id));
//       } else {
//         const parsed = JSON.parse(mergedJson || "[]");
//         trades = Array.isArray(parsed) ? parsed : [parsed];
//       }

//       if (!trades.length) {
//         throw new Error("No trades found to run.");
//       }

//       const res = await runPipelineApi({
//         trades,
//         source_channel: "merged",
//       });

//       onComplete(res.data);
//     } catch (e) {
//       setErr(e.response?.data?.detail || e.message || "Failed to run pipeline");
//     } finally {
//       setRunning(false);
//     }
//   };

//   return (
//     <div style={{ maxWidth: 1150, margin: "0 auto" }}>
//       <SectionHeader
//         title="Merge Trade Sources"
//         sub="Load trades from DB + CSV into one view, filter by source, then run the pipeline."
//         actions={
//           <>
//             <Btn variant="secondary" size="sm" icon={Ic.Refresh} onClick={loadMerged} disabled={loading}>
//               {loading ? "Loading..." : "Refresh"}
//             </Btn>
//             <Btn variant="secondary" size="sm" icon={Ic.Copy} onClick={loadSelectedIntoJson} disabled={!filteredTrades.length}>
//               Load Selected into JSON
//             </Btn>
//             <Btn variant="primary" size="sm" icon={Ic.Zap} onClick={runPipelineFromMergedJson} disabled={running}>
//               {running ? "Running..." : "Run Pipeline"}
//             </Btn>
//           </>
//         }
//       />

//       <div style={{ display: "flex", gap: 8, marginBottom: 14, flexWrap: "wrap" }}>
//         {[
//           { key: "all", label: "All Sources" },
//           { key: "in_memory_db", label: "Trading DB" },
//           { key: "csv_file", label: "CSV File" },
//         ].map(item => (
//           <Btn
//             key={item.key}
//             variant={sourceFilter === item.key ? "primary" : "secondary"}
//             size="sm"
//             onClick={() => setSourceFilter(item.key)}
//           >
//             {item.label}
//           </Btn>
//         ))}
//       </div>

//       {err && (
//         <div style={{
//           padding: "11px 14px",
//           background: C.redTint,
//           border: `1px solid ${C.redBorder}`,
//           borderRadius: 8,
//           marginBottom: 14,
//           display: "flex",
//           gap: 8,
//           color: C.red,
//           fontSize: 13
//         }}>
//           <Ic.Alert style={{ width: 15, height: 15, color: C.red, flexShrink: 0 }} />
//           <span>{err}</span>
//         </div>
//       )}

//       <Card noPad style={{ marginBottom: 14 }}>
//         <div style={{
//           padding: "12px 16px",
//           borderBottom: `1px solid ${C.border}`,
//           display: "flex",
//           justifyContent: "space-between",
//           alignItems: "center",
//           background: C.surfaceAlt,
//         }}>
//           <div>
//             <p style={{ margin: 0, fontSize: 13, fontWeight: 700, color: C.ink, fontFamily: FONT.display }}>
//               Merged Trades
//             </p>
//             <p style={{ margin: "2px 0 0", fontSize: 11, color: C.inkFaint }}>
//               Showing {filteredTrades.length} of {allTrades.length} trades · Selected {selected.size}
//             </p>
//           </div>

//           <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
//             <Btn variant="secondary" size="xs" onClick={toggleAll} disabled={!filteredTrades.length}>
//               {filteredTrades.length > 0 && filteredTrades.every(t => selected.has(t.trade_id))
//                 ? "Deselect All"
//                 : "Select All"}
//             </Btn>
//             <Btn variant="secondary" size="xs" onClick={() => setSelected(new Set())}>
//               Clear
//             </Btn>
//           </div>
//         </div>

//         {loading ? (
//           <div style={{ padding: 40, display: "flex", justifyContent: "center" }}>
//             <Spinner size={24} />
//           </div>
//         ) : (
//           <div style={{ overflowX: "auto" }}>
//             <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
//               <thead>
//                 <tr style={{ background: C.surfaceAlt }}>
//                   <th style={{ padding: "10px 14px", width: 44 }}>
//                     <input
//                       type="checkbox"
//                       checked={filteredTrades.length > 0 && filteredTrades.every(t => selected.has(t.trade_id))}
//                       onChange={toggleAll}
//                       style={{ accentColor: C.blue, cursor: "pointer" }}
//                     />
//                   </th>
//                   {["Trade ID", "Source", "ISIN", "Price", "CCY", "Qty", "Venue", "Status"].map(h => (
//                     <th key={h} style={{
//                       padding: "10px 14px",
//                       textAlign: "left",
//                       fontSize: 10,
//                       color: C.inkFaint,
//                       textTransform: "uppercase",
//                       letterSpacing: ".07em",
//                       fontWeight: 700,
//                       borderBottom: `1px solid ${C.border}`,
//                       whiteSpace: "nowrap",
//                     }}>
//                       {h}
//                     </th>
//                   ))}
//                 </tr>
//               </thead>

//               <tbody>
//                 {filteredTrades.map((t, i) => {
//                   const isSel = selected.has(t.trade_id);
//                   const src = t.source_channel || "merged";
//                   const srcColor = src === "in_memory_db" ? C.green : src === "csv_file" ? C.violet : C.blue;

//                   return (
//                     <tr
//                       key={`${src}-${t.trade_id}-${i}`}
//                       onClick={() => toggleOne(t.trade_id)}
//                       style={{
//                         borderBottom: `1px solid ${C.border}`,
//                         background: isSel ? srcColor + "08" : (i % 2 ? C.surfaceAlt : C.surface),
//                         cursor: "pointer",
//                       }}
//                     >
//                       <td style={{ padding: "10px 14px" }}>
//                         <input
//                           type="checkbox"
//                           checked={isSel}
//                           onChange={() => toggleOne(t.trade_id)}
//                           onClick={e => e.stopPropagation()}
//                           style={{ cursor: "pointer", accentColor: srcColor }}
//                         />
//                       </td>
//                       <td style={{ padding: "10px 14px", fontFamily: FONT.mono, fontSize: 11, color: srcColor, fontWeight: 700 }}>
//                         {t.trade_id}
//                       </td>
//                       <td style={{ padding: "10px 14px", fontSize: 11, color: C.inkMuted, fontFamily: FONT.mono }}>
//                         {t._source_label || src}
//                       </td>
//                       <td style={{ padding: "10px 14px" }}>{t.isin}</td>
//                       <td style={{ padding: "10px 14px" }}>{t.price}</td>
//                       <td style={{ padding: "10px 14px" }}>{t.currency}</td>
//                       <td style={{ padding: "10px 14px" }}>{t.quantity}</td>
//                       <td style={{ padding: "10px 14px", fontFamily: FONT.mono, fontSize: 11 }}>{t.venue}</td>
//                       <td style={{ padding: "10px 14px" }}>
//                         <Badge status={t.report_status || "NEWT"} size="xs" />
//                       </td>
//                     </tr>
//                   );
//                 })}
//               </tbody>
//             </table>
//           </div>
//         )}
//       </Card>

//       <Card noPad>
//         <div style={{
//           padding: "12px 16px",
//           borderBottom: `1px solid ${C.border}`,
//           display: "flex",
//           justifyContent: "space-between",
//           alignItems: "center",
//           background: C.surfaceAlt,
//         }}>
//           <div>
//             <p style={{ margin: 0, fontSize: 13, fontWeight: 700, color: C.ink, fontFamily: FONT.display }}>
//               Merged JSON Payload
//             </p>
//             <p style={{ margin: "2px 0 0", fontSize: 11, color: C.inkFaint }}>
//               This is what will be sent to the existing pipeline.
//             </p>
//           </div>
//           <Btn variant="secondary" size="xs" icon={Ic.Copy} onClick={loadSelectedIntoJson}>
//             Load Selected / All
//           </Btn>
//         </div>

//         <textarea
//           value={mergedJson}
//           onChange={e => setMergedJson(e.target.value)}
//           spellCheck={false}
//           style={{
//             width: "100%",
//             minHeight: 280,
//             border: "none",
//             padding: "16px 20px",
//             fontSize: 12.5,
//             color: C.ink,
//             fontFamily: FONT.mono,
//             lineHeight: 1.8,
//             background: C.surfaceAlt,
//             outline: "none",
//             resize: "vertical",
//             boxSizing: "border-box",
//             display: "block",
//           }}
//         />
//       </Card>
//     </div>
//   );
// }

// function DbTab({ onAddToPipeline }) {
//   const [trades, setTrades] = useState([]);
//   const [selected, setSelected] = useState([]);

//   const fetchData = async () => {
//     const res = await api.get("/buffer/by-source/db");
//     setTrades(res.data.trades || []);
//   };

//   useEffect(() => {
//     fetchData();
//   }, []);

//   const toggleSelect = (tradeId) => {
//     setSelected((prev) =>
//       prev.includes(tradeId)
//         ? prev.filter((id) => id !== tradeId)
//         : [...prev, tradeId]
//     );
//   };

//   const addSelected = async () => {
//     if (!selected.length) return;

//     await api.post("/pipeline/add", {
//       trade_ids: selected,
//     });

//     setSelected([]);
//     fetchData(); // refresh after move
//   };

//   return (
//     <div style={{ maxWidth: 900, margin: "0 auto" }}>
//       <h3>DB Trades</h3>

//       <table style={{ width: "100%", borderCollapse: "collapse" }}>
//         <thead>
//           <tr>
//             <th>Select</th>
//             <th>Trade ID</th>
//             <th>Source</th>
//           </tr>
//         </thead>

//         <tbody>
//           {trades.map((t) => (
//             <tr key={t.trade_id}>
//               <td>
//                 <input
//                   type="checkbox"
//                   checked={selected.includes(t.trade_id)}
//                   onChange={() => toggleSelect(t.trade_id)}
//                 />
//               </td>
//               <td>{t.trade_id}</td>
//               <td>{t.source}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>

//       <button
//         onClick={addSelected}
//         style={{
//           marginTop: 16,
//           padding: "10px 14px",
//           background: "#2563eb",
//           color: "#fff",
//           border: "none",
//           borderRadius: 6,
//         }}
//       >
//         Add Selected to Pipeline
//       </button>
//     </div>
//   );
// }

// function AuditChatTab({ onComplete }) {
//   const [messages, setMessages] = useState([
//     {
//       role: "system",
//       text: "MiFID II Audit Assistant ready. Ask about trades, exceptions, HITL cases, T+1 checks, or compliance summaries.",
//     },
//   ]);
//   const [query, setQuery] = useState("");
//   const [busy, setBusy] = useState(false);
//   const [lastResult, setLastResult] = useState(null);
//   const [copied, setCopied] = useState(false);
//   const bottomRef = useRef(null);
//   const inputRef = useRef(null);

//   const lastRunId = lastResult?.run_id || null;

//   useEffect(() => {
//     bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
//   }, [messages, busy]);

//   useEffect(() => {
//     inputRef.current?.focus();
//   }, []);

//   const sendQuery = async () => {
//     const text = query.trim();
//     if (!text || busy) return;

//     setMessages((prev) => [...prev, { role: "user", text }]);
//     setQuery("");
//     setBusy(true);

//     try {
//       const res = await api.post("/audit-query", { query: text });
//       const data = res.data || {};
//       setLastResult(data);

//       if (typeof onComplete === "function") {
//         onComplete(data);
//       }

//       setMessages((prev) => [
//         ...prev,
//         {
//           role: "assistant",
//           text: data.response || "No narrative returned.",
//           run_id: data.run_id || "",
//           stats: data.stats || {},
//           source_breakdown: data.source_breakdown || {},
//         },
//       ]);
//     } catch (e) {
//       setMessages((prev) => [
//         ...prev,
//         {
//           role: "error",
//           text: e.response?.data?.detail || e.message || "Audit query failed.",
//         },
//       ]);
//     } finally {
//       setBusy(false);
//     }
//   };

//   const onKeyDown = (e) => {
//     if (e.key === "Enter" && !e.shiftKey) {
//       e.preventDefault();
//       sendQuery();
//     }
//   };

//   const copyLastResponse = async () => {
//     const lastAssistant = [...messages].reverse().find((m) => m.role === "assistant");
//     if (!lastAssistant) return;

//     try {
//       await navigator.clipboard.writeText(lastAssistant.text);
//       setCopied(true);
//       setTimeout(() => setCopied(false), 1400);
//     } catch {}
//   };

//   const quickQueries = [
//     "Show me failed trades from yesterday",
//     "Run a T+1 compliance summary for this month",
//     "Show trades requiring human review",
//     "Show execution records for trade T1001",
//   ];

//   return (
//     <div style={{ maxWidth: 1200, margin: "0 auto", display: "flex", flexDirection: "column", gap: 16 }}>
      
//       {/* HEADER */}
//       <div
//         style={{
//           background: `linear-gradient(135deg, ${C.blue} 0%, ${C.blueDark} 100%)`,
//           color: "#fff",
//           borderRadius: 18,
//           padding: "20px 22px",
//         }}
//       >
//         <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap" }}>
//           <div>
//             <div style={{ display: "inline-flex", gap: 8, alignItems: "center", marginBottom: 10 }}>
//               <Ic.Wand style={{ width: 16, height: 16 }} />
//               <span style={{ fontSize: 11, fontWeight: 700 }}>
//                 Auditor Intelligence Layer
//               </span>
//             </div>
//             <h2 style={{ margin: 0 }}>MiFID II Audit Chat</h2>
//           </div>
//         </div>
//       </div>

//       {/* CHAT BOX */}
//       <div style={{ display: "grid", gridTemplateColumns: "1.35fr .65fr", gap: 16 }}>
        
//         <div style={{ background: C.surface, border: `1px solid ${C.border}`, borderRadius: 16, display: "flex", flexDirection: "column" }}>
          
//           {/* TOP BAR */}
//           <div style={{ padding: 14, borderBottom: `1px solid ${C.border}` }}>
//             <b>Conversation</b>
//           </div>

//           {/* MESSAGES */}
//           <div style={{ flex: 1, overflowY: "auto", padding: 16 }}>
//             {messages.map((m, i) => (
//               <div key={i} style={{ marginBottom: 10 }}>
//                 <b>{m.role}:</b> {m.text}
//               </div>
//             ))}

//             {busy && <div>Running...</div>}
//             <div ref={bottomRef} />
//           </div>

//           {/* INPUT */}
//           <div style={{ padding: 14, borderTop: `1px solid ${C.border}` }}>
//             <textarea
//               ref={inputRef}
//               value={query}
//               onChange={(e) => setQuery(e.target.value)}
//               onKeyDown={onKeyDown}
//               rows={2}
//               style={{ width: "100%" }}
//             />

//             <button onClick={sendQuery} disabled={busy}>
//               {busy ? "Running..." : "Ask"}
//             </button>
//           </div>
//         </div>

//         {/* SIDE PANEL */}
//         <div style={{ background: C.surface, border: `1px solid ${C.border}`, borderRadius: 16, padding: 16 }}>
//           <b>Run Summary</b>
//           <div>Run ID: {lastResult?.run_id || "-"}</div>
//           <div>Passed: {lastResult?.stats?.passed ?? 0}</div>
//           <div>HITL: {lastResult?.stats?.hitl ?? 0}</div>
//           <div>Failed: {lastResult?.stats?.fail ?? 0}</div>
//         </div>
//       </div>
//     </div>
//   );
// }

// // ─── DASHBOARD ────────────────────────────────────────────────────────────────
// function DashboardTab({ data }) {
//   if (!data) return (
//     <Empty
//       icon={Ic.Home}
//       title="No pipeline run yet"
//       sub="Navigate to Input and execute your first trade batch to see results here."
//     />
//   );

//   const { stats = {}, final_trades = [], agent_log = [], risk_results = [] } = data;

//   const hitlCount =
//     data.hitl_queue?.length ||
//     final_trades.filter(t => t.final_status === "HITL").length;

//   const autoFixed = stats.auto_fixed || data.corrections?.length || 0;
//   const failCount = final_trades.filter(t => t.final_status === "FAIL").length;

//   // ✅ NEW: Source Summary
//   const sourceSummary = {};
//   final_trades.forEach(t => {
//     const s = t.source_channel || "ui";
//     sourceSummary[s] = (sourceSummary[s] || 0) + 1;
//   });

//   const logRef = useRef(null);

//   useEffect(() => {
//     if (logRef.current)
//       logRef.current.scrollTop = logRef.current.scrollHeight;
//   }, [agent_log]);

//   const acol = l =>
//     l.includes("Ingestion")
//       ? C.blue
//       : l.includes("Enrichment")
//         ? C.violet
//         : l.includes("Validation")
//           ? C.green
//           : l.includes("Risk")
//             ? C.amber
//             : l.includes("Compliance")
//               ? "#DB2777"
//               : l.includes("Decision")
//                 ? C.blue
//                 : l.includes("Report")
//                   ? C.cyan
//                   : C.inkFaint;

//   return (
//     <div>
//       <SectionHeader
//         title="Operations Center"
//         sub="Real-time agentic pipeline results & trade analytics."
//         actions={
//           <Pill
//             label={`PIPELINE COMPLETE — ${data.run_id}`}
//             color={C.green}
//           />
//         }
//       />

//       {/* Stats */}
//       <div style={{
//         display: "grid",
//         gridTemplateColumns: "repeat(5,1fr)",
//         gap: 12,
//         marginBottom: 20
//       }}>
//         <StatCard label="Total Trades" value={stats.total || 0} accent={C.blue} icon={Ic.Layer} />
//         <StatCard label="Passed" value={stats.passed || 0} accent={C.green} icon={Ic.Check} />
//         <StatCard label="HITL Required" value={hitlCount} accent={C.amber} icon={Ic.Users} />
//         <StatCard label="Failed" value={failCount} accent={C.red} icon={Ic.Alert} />
//         <StatCard label="Auto-Corrected" value={autoFixed} accent={C.violet} icon={Ic.Wand} />
//       </div>

//       {/* ✅ NEW: Source Summary */}
//       <div style={{ marginBottom: 14, display: "flex", gap: 10, flexWrap: "wrap" }}>
//         {Object.entries(sourceSummary).map(([k, v]) => (
//           <span key={k} style={{
//             padding: "5px 10px",
//             background: C.blueTint,
//             border: `1px solid ${C.border}`,
//             borderRadius: 6,
//             fontSize: 11,
//             fontWeight: 700,
//             fontFamily: FONT.mono
//           }}>
//             {k.toUpperCase()}: {v}
//           </span>
//         ))}
//       </div>

//       <div style={{ display: "grid", gridTemplateColumns: "1fr 340px", gap: 14, marginBottom: 14 }}>

//         {/* TABLE */}
//         <Card noPad>
//           <CardHeader
//             title="Final Trade Decisions"
//             right={<span style={{ fontSize: 11 }}>{final_trades.length} records</span>}
//           />

//           <div style={{ overflowX: "auto" }}>
//             <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>

//               <thead>
//                 <tr style={{ background: C.surfaceAlt }}>
//                   {["Trade ID", "Source", "ISIN", "Qty", "CCY", "Price", "Auto Fix", "Status", "Confidence"]
//                     .map(h => (
//                       <th key={h} style={{
//                         padding: "9px 14px",
//                         textAlign: "left",
//                         fontSize: 10,
//                         color: C.inkFaint,
//                         textTransform: "uppercase",
//                         fontWeight: 700,
//                         borderBottom: `1px solid ${C.border}`
//                       }}>
//                         {h}
//                       </th>
//                     ))}
//                 </tr>
//               </thead>

//               <tbody>
//                 {final_trades.map((t, i) => {
//                   const isFail = t.final_status === "FAIL";
//                   const bg = isFail ? C.redTint + "60" : (i % 2 ? C.surfaceAlt : C.surface);

//                   return (
//                     <tr key={t.trade_id}
//                       style={{
//                         background: bg,
//                         borderBottom: `1px solid ${C.border}`,
//                         ...(isFail && { borderLeft: `3px solid ${C.red}` })
//                       }}
//                     >
//                       <td style={{ padding: 10, fontFamily: FONT.mono, color: isFail ? C.red : C.blue }}>
//                         {t._original_trade_id || t.trade_id}
//                       </td>

//                       {/* ✅ SOURCE COLUMN */}
//                       <td style={{ padding: 10, fontSize: 11 }}>
//                         {t.source_channel || "ui"}
//                       </td>

//                       <td style={{ padding: 10 }}>{t.isin}</td>
//                       <td style={{ padding: 10 }}>{t.quantity}</td>
//                       <td style={{ padding: 10 }}>{t.currency}</td>
//                       <td style={{ padding: 10 }}>{t.price}</td>

//                       <td style={{ padding: 10 }}>
//                         <Badge status={t.auto_fix_applied ? "APPLIED" : "NONE"} size="xs" />
//                       </td>

//                       <td style={{ padding: 10 }}>
//                         <Badge status={t.final_status} />
//                       </td>

//                       <td style={{ padding: 10 }}>
//                         <ConfBar value={t.decision_confidence} status={t.final_status} compact />
//                       </td>
//                     </tr>
//                   );
//                 })}
//               </tbody>
//             </table>
//           </div>
//         </Card>

//         {/* LOG */}
//         <Card noPad style={{ display: "flex", flexDirection: "column", maxHeight: 420 }}>
//           <CardHeader title="Agent Execution Log" />

//           <div ref={logRef} style={{ overflowY: "auto", padding: 10 }}>
//             {agent_log.map((log, i) => (
//               <div key={i} style={{ fontSize: 11, color: acol(log), marginBottom: 4 }}>
//                 {log}
//               </div>
//             ))}
//           </div>
//         </Card>
//       </div>

//       {/* RISK */}
//       {risk_results.length > 0 && (
//         <Card style={{ padding: 16 }}>
//           <p style={{ fontWeight: 700 }}>Risk Distribution</p>

//           {risk_results.map(r => (
//             <div key={r.trade_id} style={{ marginBottom: 8 }}>
//               <Badge status={r.risk_level} />
//               <ConfBar value={r.confidence} status={r.risk_level} />
//             </div>
//           ))}
//         </Card>
//       )}
//     </div>
//   );
// }
// // ─── VALIDATION ───────────────────────────────────────────────────────────────
// function ValidationTab({ results = [], complianceResults = [] }) {
//   if (!results.length) return <Empty icon={Ic.Shield} title="No validation data" sub="Run a pipeline to see field-level validation results." />;
//   return (
//     <div>
//       <SectionHeader title="Validation Results" sub="MiFID II field-level validation with RAG-augmented rule retrieval and deterministic safety net." />
//       <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
//         {results.map(r => {
//           const comp = complianceResults.find(c => c.trade_id === r.trade_id) || {};
//           return (
//             <Card key={r.trade_id} noPad style={{ borderLeft: `3px solid ${r.passed ? C.green : C.red}` }}>
//               <div style={{ padding: "13px 18px", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
//                 <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
//                   <span style={{ fontFamily: FONT.mono, fontSize: 12, color: C.blue, fontWeight: 700 }}>{r.trade_id}</span>
//                   <Badge status={r.passed ? "PASS" : "false"} />
//                   {comp.compliant !== undefined && <Badge status={comp.compliant ? "true" : "false"} />}
//                 </div>
//                 <div style={{ display: "flex", gap: 14, alignItems: "center", flexShrink: 0 }}>
//                   <div style={{ textAlign: "right" }}>
//                     <p style={{ margin: "0 0 4px", fontSize: 9, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".07em", fontWeight: 700 }}>Confidence</p>
//                     <div style={{ width: 110 }}><ConfBar value={r.confidence} status={r.passed ? "PASS" : "FAIL"} compact /></div>
//                   </div>
//                   <div style={{ textAlign: "right" }}>
//                     <p style={{ margin: "0 0 2px", fontSize: 9, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".07em", fontWeight: 700 }}>RAG</p>
//                     <span style={{ fontSize: 13, fontWeight: 800, color: C.ink, fontFamily: FONT.mono }}>{Math.round((r.rag_confidence || 0) * 100)}%</span>
//                   </div>
//                 </div>
//               </div>
//               {r.summary && <div style={{ padding: "8px 18px", background: C.surfaceAlt, borderTop: `1px solid ${C.border}` }}><p style={{ margin: 0, fontSize: 12, color: C.inkMuted, lineHeight: 1.6 }}>{r.summary}</p></div>}
//               {r.issues?.length > 0 && (
//                 <div style={{ borderTop: `1px solid ${C.border}` }}>
//                   <table style={{ width: "100%", borderCollapse: "collapse" }}>
//                     <thead><tr style={{ background: C.surfaceAlt }}>
//                       <th style={{ padding: "7px 18px", textAlign: "left", fontSize: 10, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".07em", fontWeight: 700 }}>Field</th>
//                       <th style={{ padding: "7px 18px", textAlign: "left", fontSize: 10, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".07em", fontWeight: 700 }}>Error</th>
//                       <th style={{ padding: "7px 18px", textAlign: "right", fontSize: 10, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".07em", fontWeight: 700 }}>Severity</th>
//                     </tr></thead>
//                     <tbody>{r.issues.map((iss, i) => (
//                       <tr key={i} style={{ borderTop: `1px solid ${C.border}` }}>
//                         <td style={{ padding: "9px 18px", fontSize: 12, fontFamily: FONT.mono, color: C.ink, fontWeight: 700, minWidth: 160 }}>{iss.field}</td>
//                         <td style={{ padding: "9px 18px", fontSize: 12, color: C.inkMuted, lineHeight: 1.5 }}>{iss.error}</td>
//                         <td style={{ padding: "9px 18px", textAlign: "right" }}><Badge status={iss.severity} size="xs" /></td>
//                       </tr>
//                     ))}</tbody>
//                   </table>
//                 </div>
//               )}
//             </Card>
//           );
//         })}
//       </div>
//     </div>
//   );
// }
// // ─── RISK ─────────────────────────────────────────────────────────────────────
// function RiskTab({ results = [] }) {
//   if (!results.length) return <Empty icon={Ic.Alert} title="No risk data" sub="Run a pipeline to see risk assessment results." />;
//   return (
//     <div>
//       <SectionHeader title="Risk Assessment" sub="AI-driven risk scoring with deterministic baseline across 9 risk drivers." />
//       <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
//         {results.map(r => (
//           <Card key={r.trade_id} noPad style={{ borderLeft: `3px solid ${r.risk_level === "HIGH" ? C.red : r.risk_level === "MEDIUM" ? C.amber : C.green}` }}>
//             <div style={{ padding: "13px 18px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
//               <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
//                 <span style={{ fontFamily: FONT.mono, fontSize: 12, color: C.blue, fontWeight: 700 }}>{r.trade_id}</span>
//                 <Badge status={r.risk_level || "LOW"} />
//               </div>
//               <div style={{ width: 150 }}><ConfBar value={r.confidence} status={r.risk_level} compact /></div>
//             </div>
//             {r.summary && <div style={{ padding: "0 18px 12px" }}><p style={{ margin: 0, fontSize: 12, color: C.inkMuted, lineHeight: 1.6 }}>{r.summary}</p></div>}
//             {r.drivers?.length > 0 && (
//               <div style={{ padding: "10px 18px 14px", borderTop: `1px solid ${C.border}`, display: "flex", flexDirection: "column", gap: 6 }}>
//                 {r.drivers.map((d, i) => (
//                   <div key={i} style={{ display: "flex", gap: 10, padding: "8px 12px", background: C.blueTint, borderRadius: 7, borderLeft: `2px solid ${C.blue}` }}>
//                     <Ic.Info style={{ width: 13, height: 13, color: C.blue, flexShrink: 0, marginTop: 1 }} />
//                     <p style={{ margin: 0, fontSize: 12, color: C.inkMid, lineHeight: 1.5 }}>{typeof d === "object" ? `[${d.rule_id}] ${d.description || "—"}` : d}</p>
//                   </div>
//                 ))}
//               </div>
//             )}
//           </Card>
//         ))}
//       </div>
//     </div>
//   );
// }
// // ─── HITL ─────────────────────────────────────────────────────────────────────
// function HITLTab({ data, runId, onDecision }) {
//   const [decisions, setDec] = useState({});
//   const [modTrade, setMod] = useState(null);
//   const [busy, setBusy] = useState({});
//   const [selected, setSel] = useState(new Set());
//   const [bulkBusy, setBB] = useState(false);
//   const [errs, setErrs] = useState({});
//   const [liveItems, setLive] = useState([]);
//   const [refreshing, setRef] = useState(false);
//   const validations = data?.validation_results || [];
//   const refresh = useCallback(async () => { if (!runId) return; setRef(true); try { const r = await getHitlQueue(runId); setLive(Array.isArray(r.data?.items) ? r.data.items : []); } catch { } finally { setRef(false); } }, [runId]);
//   useEffect(() => { refresh(); const t = setInterval(refresh, 8000); return () => clearInterval(t); }, [refresh]);

//   // ─── FIX 5: FAIL trades excluded from HITL queue ─────────────────────────
//   const hitlTrades = (() => {
//     const src = liveItems.length ? liveItems : (data?.hitl_queue || []);
//     if (src.length) return src.map(h => ({ ...(h.trade || {}), trade_id: h.trade_id || h?.trade?.trade_id, decision_reason: h.reason, decision_confidence: h.confidence, _meta: h }));
//     // Only HITL status — FAIL goes to dashboard, not here
//     return (data?.final_trades || []).filter(t => t.final_status === "HITL");
//   })();

//   const decide = async (trade, dec) => { setBusy(b => ({ ...b, [trade.trade_id]: true })); setErrs(e => ({ ...e, [trade.trade_id]: null })); try { const res = await submitHitlDecision({ run_id: runId, trade_id: trade.trade_id, decision: dec, reviewer_note: "" }); setDec(d => ({ ...d, [trade.trade_id]: { dec, result: res.data } })); setLive(p => p.filter(x => (x.trade_id || x?.trade?.trade_id) !== trade.trade_id)); onDecision(trade.trade_id, dec, res.data); } catch (e) { setErrs(er => ({ ...er, [trade.trade_id]: e.response?.data?.detail || e.message })); } finally { setBusy(b => ({ ...b, [trade.trade_id]: false })); } };
//   const bulk = async (dec) => { if (!selected.size) return; setBB(true); try { await submitBulkHitl({ run_id: runId, trade_ids: [...selected], decision: dec }); selected.forEach(id => setDec(d => ({ ...d, [id]: { dec } }))); setSel(new Set()); refresh(); } catch (e) { alert("Bulk failed: " + e.message); } finally { setBB(false); } };
//   const modSuccess = (result, id) => { setDec(d => ({ ...d, [id]: { dec: "MODIFIED", result } })); setMod(null); refresh(); onDecision(id, "MODIFIED", result); };
//   if (!hitlTrades.length) return <div><SectionHeader title="Human-In-The-Loop Review" sub="Manual validation queue." /><Empty icon={Ic.Users} title="No trades pending review" sub="All trades were auto-processed. Run a new batch to populate the HITL queue." /></div>;
//   const pending = hitlTrades.filter(t => !decisions[t.trade_id]);
//   const resolved = hitlTrades.filter(t => !!decisions[t.trade_id]);
//   return (
//     <div>
//       <SectionHeader title="Human-In-The-Loop Review" sub={`${pending.length} trade${pending.length !== 1 ? "s" : ""} require manual validation.`}
//         actions={<><Btn variant="secondary" size="sm" icon={Ic.Refresh} onClick={refresh} disabled={refreshing} loading={refreshing}>{refreshing ? "Refreshing…" : "Refresh"}</Btn>{selected.size > 0 && <><Btn variant="success" size="sm" icon={Ic.Check} onClick={() => bulk("APPROVED")} disabled={bulkBusy}>Approve {selected.size}</Btn><Btn variant="danger" size="sm" icon={Ic.X} onClick={() => bulk("REJECTED")} disabled={bulkBusy}>Reject {selected.size}</Btn></>}</>} />
//       <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 12, marginBottom: 20 }}>
//         <StatCard label="Pending Review" value={pending.length} accent={C.amber} icon={Ic.Users} />
//         <StatCard label="Resolved" value={resolved.length} accent={C.green} icon={Ic.Check} />
//         <StatCard label="Total HITL" value={hitlTrades.length} accent={C.blue} icon={Ic.Layer} />
//       </div>
//       <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
//         {hitlTrades.map(trade => {
//           const dec = decisions[trade.trade_id]; const val = validations.find(v => v.trade_id === trade.trade_id) || {};
//           const isBusy = !!busy[trade.trade_id]; const isSel = selected.has(trade.trade_id); const err = errs[trade.trade_id];
//           const bc = dec ? dec.dec === "APPROVED" ? C.greenBorder : dec.dec === "REJECTED" ? C.redBorder : "rgba(0,86,197,.25)" : C.border;
//           return (
//             <div key={trade.trade_id} style={{ background: C.surface, borderRadius: 12, border: `1px solid ${bc}`, boxShadow: "0 2px 12px rgba(15,23,42,.06)", overflow: "hidden", transition: "border-color .25s" }}>
//               <div style={{ padding: "13px 18px", borderBottom: `1px solid ${C.border}`, display: "flex", alignItems: "center", gap: 10, background: dec ? (dec.dec === "APPROVED" ? C.greenTint : dec.dec === "REJECTED" ? C.redTint : C.blueTint) + "80" : C.surfaceAlt }}>
//                 {!dec && <input type="checkbox" checked={isSel} onChange={e => setSel(s => { const n = new Set(s); e.target.checked ? n.add(trade.trade_id) : n.delete(trade.trade_id); return n; })} style={{ width: 15, height: 15, cursor: "pointer", flexShrink: 0, accentColor: C.blue }} />}
//                 <div style={{ flex: 1, minWidth: 0 }}>
//                   <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
//                     <span style={{ fontFamily: FONT.mono, fontSize: 13, fontWeight: 700, color: C.blue }}>{trade.trade_id}</span>
//                     {trade.isin && <span style={{ fontSize: 11, color: C.inkMuted }}>{trade.isin}</span>}
//                     {trade.currency && <><span style={{ color: C.border }}>·</span><span style={{ fontSize: 11, color: C.inkMuted }}>{trade.currency} {parseFloat(trade.price || 0).toLocaleString()}</span></>}
//                     {trade.quantity && <><span style={{ color: C.border }}>·</span><span style={{ fontSize: 11, color: C.inkMuted }}>Qty {trade.quantity}</span></>}
//                   </div>
//                 </div>
//                 <Badge status={dec ? dec.dec : "HITL"} pulse={!dec} />
//               </div>
//               <div style={{ padding: "14px 18px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
//                 <div>
//                   <p style={{ margin: "0 0 7px", fontSize: 9, fontWeight: 700, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".09em" }}>AI Decision Reasoning</p>
//                   <div style={{ padding: "10px 13px", background: C.blueTint, borderRadius: 8, borderLeft: `3px solid ${C.blue}` }}>
//                     <p style={{ margin: 0, fontSize: 12, color: C.inkMid, lineHeight: 1.7 }}>{trade.decision_reason || "No reasoning provided."}</p>
//                   </div>
//                 </div>
//                 <div>
//                   <p style={{ margin: "0 0 7px", fontSize: 9, fontWeight: 700, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".09em" }}>Validation Issues ({val.issues?.length || 0})</p>
//                   <div style={{ display: "flex", flexDirection: "column", gap: 4, maxHeight: 150, overflowY: "auto" }}>
//                     {!(val.issues?.length) ? <p style={{ fontSize: 12, color: C.inkFaint, fontStyle: "italic" }}>No validation issues recorded.</p>
//                       : val.issues.map((iss, i) => (
//                         <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", padding: "6px 9px", background: C.surfaceAlt, borderRadius: 6, gap: 8, border: `1px solid ${C.border}` }}>
//                           <span style={{ fontSize: 11, fontFamily: FONT.mono, color: C.ink, fontWeight: 700, flexShrink: 0 }}>{iss.field}</span>
//                           <span style={{ fontSize: 11, color: C.inkMuted, flex: 1, textAlign: "right", lineHeight: 1.4 }}>{iss.error}</span>
//                           <Badge status={iss.severity} size="xs" />
//                         </div>
//                       ))}
//                   </div>
//                 </div>
//               </div>
//               {err && <div style={{ margin: "0 18px 10px", padding: "9px 12px", background: C.redTint, border: `1px solid ${C.redBorder}`, borderRadius: 7, fontSize: 12, color: C.red, display: "flex", gap: 7 }}><Ic.Alert style={{ width: 13, height: 13, flexShrink: 0 }} />{err}</div>}
//               {!dec && (
//                 <div style={{ padding: "12px 18px", borderTop: `1px solid ${C.border}`, display: "flex", gap: 8, alignItems: "center", background: C.surfaceAlt }}>
//                   <Btn variant="success" icon={isBusy ? null : Ic.Check} onClick={() => decide(trade, "APPROVED")} disabled={isBusy} loading={isBusy}>{isBusy ? "Processing…" : "Approve"}</Btn>
//                   <Btn variant="danger" icon={Ic.X} onClick={() => decide(trade, "REJECTED")} disabled={isBusy}>Reject</Btn>
//                   <Btn variant="amber" icon={Ic.Edit} onClick={() => setMod(trade)} disabled={isBusy}>Modify & Re-run</Btn>
//                   <div style={{ flex: 1 }} />
//                   <div style={{ textAlign: "right" }}>
//                     <p style={{ margin: 0, fontSize: 9, color: C.inkFaint, textTransform: "uppercase", letterSpacing: ".08em", fontWeight: 700 }}>Confidence</p>
//                     <span style={{ fontSize: 14, fontWeight: 800, color: C.ink, fontFamily: FONT.mono }}>{Math.round((trade.decision_confidence || 0) * 100)}%</span>
//                   </div>
//                 </div>
//               )}
//               {dec && (
//                 <div style={{ padding: "11px 18px", borderTop: `1px solid ${C.border}`, display: "flex", gap: 8, alignItems: "center", background: dec.dec === "APPROVED" ? C.greenTint : dec.dec === "REJECTED" ? C.redTint : C.blueTint }}>
//                   {dec.dec === "APPROVED" ? <Ic.Check style={{ width: 15, height: 15, color: C.green }} /> : dec.dec === "REJECTED" ? <Ic.X style={{ width: 15, height: 15, color: C.red }} /> : <Ic.Edit style={{ width: 15, height: 15, color: C.blue }} />}
//                   <span style={{ fontSize: 12, fontWeight: 700, color: dec.dec === "APPROVED" ? C.green : dec.dec === "REJECTED" ? C.red : C.blue }}>
//                     {dec.dec === "APPROVED" ? "Trade approved — will appear as PASS in final report" : dec.dec === "REJECTED" ? "Trade rejected — moved to exceptions report" : "Trade modified and reprocessed through full pipeline"}
//                   </span>
//                   {dec.result?.new_status && <Badge status={dec.result.new_status} />}
//                 </div>
//               )}
//             </div>
//           );
//         })}
//       </div>
//       {modTrade && <ModifyModal trade={modTrade} runId={runId} onClose={() => setMod(null)} onSuccess={r => modSuccess(r, modTrade.trade_id)} />}
//     </div>
//   );
// }
// // ─── AUDIT ────────────────────────────────────────────────────────────────────
// function AuditTab({ runId }) {
//   const [logs, setLogs] = useState([]);
//   const [loading, setLoad] = useState(false);
//   const [err, setErr] = useState(null);
//   useEffect(() => { if (!runId) return; setLoad(true); setErr(null); getAuditLog(runId).then(r => { setLogs(r.data.entries || []); setLoad(false); }).catch(e => { setErr(e.message); setLoad(false); }); }, [runId]);
//   if (!runId) return <Empty icon={Ic.Audit} title="No run selected" sub="Run a pipeline to generate the immutable audit trail." />;
//   const acol = a => a?.includes("APPROVED") || a?.includes("PASS") ? C.green : a?.includes("REJECTED") || a?.includes("REJECT") ? C.red : a?.includes("HITL") || a?.includes("MODIFIED") ? C.amber : a?.includes("FAIL") ? C.red : a?.includes("ENRICHED") || a?.includes("VALIDATED") ? C.blue : C.inkFaint;
//   return (
//     <div>
//       <SectionHeader title="Immutable Audit Log" sub={`Complete activity trace for ${runId}. Every agent and human action permanently recorded.`}
//         actions={<Btn variant="secondary" size="sm" icon={Ic.Download}>Export Report</Btn>} />
//       {loading && <div style={{ display: "flex", justifyContent: "center", padding: 48 }}><Spinner size={24} /></div>}
//       {err && <div style={{ padding: "11px 14px", background: C.redTint, borderRadius: 8, fontSize: 12, color: C.red, marginBottom: 14 }}>{err}</div>}
//       {!loading && !err && (
//         <div style={{ position: "relative" }}>
//           <div style={{ position: "absolute", left: 22, top: 12, bottom: 0, width: 1, background: C.border }} />
//           {logs.map((log, idx) => {
//             let detail = {}; try { detail = JSON.parse(log.detail || "{}"); } catch { } const isHuman = log.agent === "HumanReviewer"; const col = acol(log.action);
//             return (
//               <div key={log.id} style={{ display: "flex", gap: 16, paddingBottom: 14, paddingLeft: 12, animation: `fadeUp .2s ease ${idx * .025}s both` }}>
//                 <div style={{ width: 22, height: 22, borderRadius: "50%", background: isHuman ? C.blue : C.surface, border: `2px solid ${isHuman ? C.blue : C.border}`, flexShrink: 0, zIndex: 1, display: "flex", alignItems: "center", justifyContent: "center", marginTop: 10 }}>
//                   {isHuman ? <Ic.Users style={{ width: 10, height: 10, color: "#fff" }} /> : <span style={{ width: 7, height: 7, borderRadius: "50%", background: col, display: "block" }} />}
//                 </div>
//                 <Card style={{ flex: 1, padding: "12px 16px", borderRadius: 9 }}>
//                   <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6, gap: 8 }}>
//                     <div style={{ display: "flex", gap: 7, alignItems: "center", flexWrap: "wrap" }}>
//                       <span style={{ fontSize: 13, fontWeight: 700, color: C.ink, fontFamily: FONT.display }}>{log.agent}</span>
//                       <span style={{ padding: "2px 7px", background: col + "15", color: col, borderRadius: 4, fontSize: 10, fontWeight: 700, fontFamily: FONT.mono }}>{log.action}</span>
//                       {isHuman && <span style={{ padding: "2px 7px", background: C.blueTint, color: C.blue, borderRadius: 4, fontSize: 10, fontWeight: 700, fontFamily: FONT.mono }}>MANUAL OVERRIDE</span>}
//                     </div>
//                     <span style={{ fontSize: 10, color: C.inkFaint, fontFamily: FONT.mono, whiteSpace: "nowrap", flexShrink: 0 }}>{log.timestamp ? new Date(log.timestamp).toLocaleString() : ""}</span>
//                   </div>
//                   <p style={{ margin: "0 0 4px", fontSize: 11, color: C.inkFaint, fontFamily: FONT.mono }}>Trade: {log.trade_id}</p>
//                   {detail.reviewer_note && <div style={{ padding: "6px 10px", background: C.surfaceAlt, borderRadius: 5, borderLeft: `2px solid ${C.blue}`, marginTop: 6 }}><p style={{ margin: 0, fontSize: 11, color: C.inkMuted, lineHeight: 1.5 }}>{detail.reviewer_note}</p></div>}
//                 </Card>
//               </div>
//             );
//           })}
//           {!logs.length && <Empty icon={Ic.Audit} title="No audit entries yet" sub="Entries appear as agents process each trade." />}
//         </div>
//       )}
//     </div>
//   );
// }
// // ─── REPORT TAB ───────────────────────────────────────────────────────────────
// function ReportTab({ data }) {
//   if (!data) return <Empty icon={Ic.Report} title="No report generated" sub="Run a pipeline to generate the MiFID II compliance report." />;
//   const { stats = {}, mifid_report_csv = "", run_id = "" } = data;
//   const corrections = data?.corrections || data?.report_json?.corrections || [];
//   const [copied, setCopied] = useState(false);
//   const [activeTab, setActiveTab] = useState("table");
//   const { headers, rows } = (() => {
//     if (!mifid_report_csv) return { headers: [], rows: [] };
//     const lines = mifid_report_csv.trim().split("\n").filter(Boolean);
//     if (!lines.length) return { headers: [], rows: [] };
//     const parseRow = (line) => {
//       const result = []; let cur = ""; let inQ = false;
//       for (let i = 0; i < line.length; i++) {
//         const ch = line[i];
//         if (ch === '"') { if (inQ && line[i + 1] === '"') { cur += '"'; i++; } else inQ = !inQ; }
//         else if (ch === ',' && !inQ) { result.push(cur.trim()); cur = ""; }
//         else { cur += ch; }
//       }
//       result.push(cur.trim()); return result;
//     };
//     const headers = parseRow(lines[0]);
//     const rows = lines.slice(1).map(parseRow);
//     return { headers, rows };
//   })();
//   const dl = () => { const b = new Blob([mifid_report_csv], { type: "text/csv" }); const a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = `${run_id}_mifid.csv`; a.click(); };
//   const copy = () => { navigator.clipboard?.writeText(mifid_report_csv); setCopied(true); setTimeout(() => setCopied(false), 2000); };
//   const getCellStyle = (header, value) => {
//     const h = (header || "").toLowerCase(); const v = (value || "").toUpperCase();
//     if (h === "final_status" || h === "status") {
//       const map = {
//         PASS: { color: C.green, bg: C.greenTint, border: C.greenBorder },
//         HITL: { color: C.amber, bg: C.amberTint, border: C.amberBorder },
//         FAIL: { color: C.red, bg: C.redTint, border: C.redBorder }, // ✅ FAIL in table
//         REJECTED: { color: C.red, bg: C.redTint, border: C.redBorder },
//         APPLIED: { color: C.violet, bg: C.violetTint, border: C.violetBorder },
//       };
//       return map[v] || null;
//     }
//     if (h === "risk_level") {
//       const map = {
//         HIGH: { color: C.red, bg: C.redTint, border: C.redBorder },
//         MEDIUM: { color: C.amber, bg: C.amberTint, border: C.amberBorder },
//         LOW: { color: C.green, bg: C.greenTint, border: C.greenBorder },
//       };
//       return map[v] || null;
//     }
//     if (h === "passed" || h === "compliant") {
//       if (v === "TRUE") return { color: C.green, bg: C.greenTint, border: C.greenBorder };
//       if (v === "FALSE") return { color: C.red, bg: C.redTint, border: C.redBorder };
//     }
//     return null;
//   };
//   const TRUNCATE_COLS = ["decision_reason", "summary", "notes", "executing_entity_lei", "buyer_lei", "seller_lei"];
//   const isTruncate = (h) => TRUNCATE_COLS.includes((h || "").toLowerCase());
//   const isIdCol = (h) => ["trade_id", "_original_trade_id"].includes((h || "").toLowerCase());
//   const isConfCol = (h) => (h || "").toLowerCase().includes("confidence");
//   const ConfCell = ({ value, rowStatus }) => {
//     const pct = Math.max(0, Math.min(100, Math.round(parseFloat(value || 0) * 100)));
//     const color = rowStatus === "FAIL" ? C.red : rowStatus === "HITL" ? C.amber : rowStatus === "PASS" ? C.green : pct >= 70 ? C.green : pct >= 40 ? C.amber : C.red;
//     return (
//       <div style={{ display: "flex", alignItems: "center", gap: 7, minWidth: 100 }}>
//         <div style={{ flex: 1, height: 5, background: C.border, borderRadius: 3, overflow: "hidden" }}>
//           <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 3, transition: "width .5s ease" }} />
//         </div>
//         <span style={{ fontSize: 10, fontWeight: 700, color, minWidth: 26, textAlign: "right", fontFamily: FONT.mono }}>{pct}%</span>
//       </div>
//     );
//   };
//   const tabStyle = (active) => ({ padding: "6px 14px", borderRadius: 7, border: "none", fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: FONT.body, background: active ? C.blue : "transparent", color: active ? "#fff" : C.inkMuted, transition: "all .13s" });
//   return (
//     <div>
//       <SectionHeader
//         title="Final Submission Portal"
//         sub="Verify compliance scoring and export the final MiFID II regulatory report."
//         actions={<><Btn variant="secondary" size="sm" icon={Ic.Refresh}>Re-verify</Btn><Btn variant="primary" size="sm" icon={Ic.Download} onClick={dl}>Export CSV</Btn></>}
//       />
//       <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 12, marginBottom: 18 }}>
//         <StatCard label="Total Records" value={(stats.total || 0).toLocaleString()} accent={C.blue} icon={Ic.Layer} sub={stats.generated_at ? new Date(stats.generated_at).toLocaleDateString() : "—"} />
//         <StatCard label="Export Status" value="Ready" accent={C.green} icon={Ic.Check} sub="Verified integrity" />
//         <StatCard label="Run Reference" value={run_id.split("-").slice(-1)[0]} accent={C.violet} icon={Ic.Audit} sub={run_id} />
//       </div>
//       <div style={{ background: `linear-gradient(135deg,${C.blue} 0%,${C.blueDark} 100%)`, borderRadius: 14, padding: "22px 28px", marginBottom: 18, display: "grid", gridTemplateColumns: "1fr auto", gap: 16, alignItems: "center", boxShadow: `0 8px 24px rgba(0,86,197,.25)` }}>
//         <div>
//           <span style={{ fontSize: 10, color: "rgba(255,255,255,.55)", textTransform: "uppercase", letterSpacing: ".12em", fontWeight: 700, fontFamily: FONT.mono }}>Generated Final Archive</span>
//           <h3 style={{ margin: "7px 0 5px", fontSize: 20, fontWeight: 800, color: "#fff", fontFamily: FONT.display, letterSpacing: "-.02em" }}>Download MiFID II Compliance Report</h3>
//           <p style={{ margin: 0, fontSize: 12, color: "rgba(255,255,255,.65)" }}>Full trade lineage, AI anomaly justifications, confidence scores, and complete decision audit trail.</p>
//         </div>
//         <Btn onClick={dl} style={{ background: "rgba(255,255,255,.15)", color: "#fff", border: "1px solid rgba(255,255,255,.25)", backdropFilter: "blur(10px)" }}>
//           <Ic.Download style={{ width: 14, height: 14 }} /> Download
//         </Btn>
//       </div>
//       {mifid_report_csv && (
//         <Card noPad style={{ marginBottom: 14 }}>
//           <div style={{ padding: "12px 16px", borderBottom: `1px solid ${C.border}`, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, background: C.surfaceAlt }}>
//             <div>
//               <p style={{ margin: 0, fontSize: 13, fontWeight: 700, color: C.ink, fontFamily: FONT.display }}>Data Preview — Report Table</p>
//               <p style={{ margin: "2px 0 0", fontSize: 11, color: C.inkFaint }}>{rows.length} record{rows.length !== 1 ? "s" : ""} · {headers.length} fields</p>
//             </div>
//             <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
//               <div style={{ display: "flex", gap: 4, padding: "4px", background: C.bg, borderRadius: 9, border: `1px solid ${C.border}` }}>
//                 <button style={tabStyle(activeTab === "table")} onClick={() => setActiveTab("table")}>Table View</button>
//                 <button style={tabStyle(activeTab === "raw")} onClick={() => setActiveTab("raw")}>Raw CSV</button>
//               </div>
//               <Btn variant="secondary" size="xs" icon={copied ? Ic.Check : Ic.Copy} onClick={copy}>{copied ? "Copied!" : "Copy"}</Btn>
//               <Btn variant="secondary" size="xs" icon={Ic.Download} onClick={dl}>Download</Btn>
//             </div>
//           </div>
//           {activeTab === "table" && (
//             <div style={{ overflowX: "auto", overflowY: "auto", maxHeight: 420, position: "relative" }}>
//               <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, minWidth: 900 }}>
//                 <thead style={{ position: "sticky", top: 0, zIndex: 2 }}>
//                   <tr style={{ background: "#EEF2F8" }}>
//                     <th style={{ padding: "10px 14px", textAlign: "left", fontSize: 10, color: C.inkFaint, fontWeight: 700, textTransform: "uppercase", letterSpacing: ".07em", borderBottom: `2px solid ${C.border}`, whiteSpace: "nowrap", position: "sticky", left: 0, background: "#EEF2F8", zIndex: 3, boxShadow: "2px 0 6px rgba(15,23,42,.06)" }}>#</th>
//                     {headers.map((h, i) => (
//                       <th key={i} style={{ padding: "10px 14px", textAlign: "left", fontSize: 10, color: C.inkFaint, fontWeight: 700, textTransform: "uppercase", letterSpacing: ".07em", borderBottom: `2px solid ${C.border}`, whiteSpace: "nowrap", borderLeft: `1px solid ${C.border}` }}>
//                         {h.replace(/_/g, " ")}
//                       </th>
//                     ))}
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {rows.map((row, ri) => {
//                     // Detect FAIL rows for table-level red tint
//                     const statusColIdx = headers.findIndex(h => h.toLowerCase() === "final_status" || h.toLowerCase() === "status");
//                     const rowStatus = statusColIdx >= 0 ? (row[statusColIdx] || "").toUpperCase() : "";
//                     const isFailRow = rowStatus === "FAIL";
//                     const baseRowBg = isFailRow ? C.redTint + "50" : (ri % 2 === 0 ? C.surface : C.surfaceAlt);
//                     return (
//                       <tr key={ri}
//                         style={{ background: baseRowBg, borderBottom: `1px solid ${C.border}`, transition: "background .1s", ...(isFailRow && { borderLeft: `3px solid ${C.red}` }) }}
//                         onMouseEnter={e => e.currentTarget.style.background = isFailRow ? C.redTint : C.blueTint + "50"}
//                         onMouseLeave={e => e.currentTarget.style.background = baseRowBg}>
//                         <td style={{ padding: "9px 14px", fontSize: 11, color: C.inkFaint, fontFamily: FONT.mono, textAlign: "center", fontWeight: 600, background: "inherit", position: "sticky", left: 0, zIndex: 1, borderRight: `2px solid ${C.border}`, boxShadow: "2px 0 6px rgba(15,23,42,.04)" }}>{ri + 1}</td>
//                         {headers.map((h, ci) => {
//                           const val = row[ci] ?? "";
//                           const badgeStyle = getCellStyle(h, val);
//                           const truncate = isTruncate(h);
//                           const isId = isIdCol(h);
//                           const isConf = isConfCol(h);
//                           return (
//                             <td key={ci} style={{ padding: "9px 14px", borderLeft: `1px solid ${C.border}`, verticalAlign: "middle" }}>
//                               {isId ? (
//                                 <span style={{ fontFamily: FONT.mono, fontSize: 11, color: isFailRow ? C.red : C.blue, fontWeight: 700 }}>{val}</span>
//                               ) : isConf ? (
//                                 <ConfCell value={val} rowStatus={rowStatus} />
//                               ) : badgeStyle ? (
//                                 <span style={{ display: "inline-flex", alignItems: "center", gap: 4, padding: "2px 8px", borderRadius: 5, fontSize: 11, fontWeight: 700, background: badgeStyle.bg, color: badgeStyle.color, border: `1px solid ${badgeStyle.border}`, fontFamily: FONT.mono, letterSpacing: ".02em", whiteSpace: "nowrap" }}>
//                                   <span style={{ width: 5, height: 5, borderRadius: "50%", background: badgeStyle.color, display: "inline-block", flexShrink: 0 }} />
//                                   {val.toUpperCase()}
//                                 </span>
//                               ) : truncate ? (
//                                 <span title={val} style={{ display: "block", maxWidth: 260, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", fontSize: 12, color: C.inkMid, lineHeight: 1.4 }}>
//                                   {val || <span style={{ color: C.inkFaint, fontStyle: "italic" }}>—</span>}
//                                 </span>
//                               ) : (
//                                 <span style={{ fontSize: 12, color: val ? C.ink : C.inkFaint, fontStyle: val ? "normal" : "italic", fontFamily: ["isin", "trade_id", "executing_entity_lei", "buyer_lei", "seller_lei", "venue"].includes(h.toLowerCase()) ? FONT.mono : FONT.body }}>
//                                   {val || "—"}
//                                 </span>
//                               )}
//                             </td>
//                           );
//                         })}
//                       </tr>
//                     );
//                   })}
//                 </tbody>
//               </table>
//               {rows.length === 0 && <div style={{ padding: "40px 24px", textAlign: "center", color: C.inkFaint, fontSize: 13 }}>No data rows found in CSV.</div>}
//             </div>
//           )}
//           {activeTab === "raw" && (
//             <pre style={{ margin: 0, padding: "14px 18px", fontSize: 11, color: C.inkMuted, overflowX: "auto", maxHeight: 380, fontFamily: FONT.mono, lineHeight: 1.8, background: C.surfaceAlt }}>{mifid_report_csv}</pre>
//           )}
//           {activeTab === "table" && rows.length > 0 && (
//             <div style={{ padding: "10px 16px", borderTop: `1px solid ${C.border}`, background: C.surfaceAlt, display: "flex", gap: 16, alignItems: "center" }}>
//               <span style={{ fontSize: 11, color: C.inkFaint }}>Showing <strong style={{ color: C.ink }}>{rows.length}</strong> records across <strong style={{ color: C.ink }}>{headers.length}</strong> fields</span>
//               <div style={{ flex: 1 }} />
//               <Btn variant="ghost" size="xs" icon={Ic.Download} onClick={dl}>Download Full CSV</Btn>
//             </div>
//           )}
//         </Card>
//       )}
//       {corrections.length > 0 && (
//         <Card noPad>
//           <CardHeader title="Auto-Fix Audit Trail" sub={`${corrections.length} field correction${corrections.length !== 1 ? "s" : ""} applied by agents`} right={<Badge status="APPLIED" />} />
//           <div style={{ padding: "14px 18px", display: "flex", flexDirection: "column", gap: 10 }}>
//             {corrections.map((c, i) => (
//               <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start", padding: "13px 15px", background: C.violetTint, border: `1px solid ${C.violetBorder}`, borderRadius: 10, borderLeft: `3px solid ${C.violet}` }}>
//                 <div style={{ width: 30, height: 30, borderRadius: 8, background: C.violet + "20", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, color: C.violet }}>
//                   <Ic.Wand style={{ width: 14, height: 14 }} />
//                 </div>
//                 <div style={{ flex: 1, minWidth: 0 }}>
//                   <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 8, flexWrap: "wrap" }}>
//                     <Badge status="APPLIED" size="xs" />
//                     <span style={{ fontFamily: FONT.mono, fontSize: 11, color: C.blue, fontWeight: 700 }}>{c.trade_id}</span>
//                     <span style={{ fontSize: 11, color: C.inkMuted }}>field: <strong style={{ color: C.ink }}>{c.field}</strong></span>
//                   </div>
//                   <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: c.reasoning ? 8 : 0 }}>
//                     <div style={{ padding: "6px 10px", background: C.redTint, border: `1px solid ${C.redBorder}`, borderRadius: 6 }}>
//                       <p style={{ margin: "0 0 3px", fontSize: 9, color: C.red, fontWeight: 700, textTransform: "uppercase", letterSpacing: ".07em" }}>Before</p>
//                       <p style={{ margin: 0, fontSize: 11, color: C.red, fontFamily: FONT.mono, wordBreak: "break-all" }}>{String(c.old_value || c.original_value || "—")}</p>
//                     </div>
//                     <div style={{ padding: "6px 10px", background: C.greenTint, border: `1px solid ${C.greenBorder}`, borderRadius: 6 }}>
//                       <p style={{ margin: "0 0 3px", fontSize: 9, color: C.green, fontWeight: 700, textTransform: "uppercase", letterSpacing: ".07em" }}>After</p>
//                       <p style={{ margin: 0, fontSize: 11, color: C.green, fontFamily: FONT.mono, wordBreak: "break-all" }}>{String(c.new_value || c.proposed_value || "—")}</p>
//                     </div>
//                   </div>
//                   {(c.reasoning || c.reason) && <p style={{ margin: 0, fontSize: 11, color: C.inkMuted, lineHeight: 1.5 }}>{c.reasoning || c.reason}</p>}
//                 </div>
//               </div>
//             ))}
//           </div>
//         </Card>
//       )}
//     </div>
//   );
// }
// // ─── ROOT ─────────────────────────────────────────────────────────────────────
// const NAV = [
//   { id: "merge", label: "Merge", Icon: Ic.Layer },
//   { id: "dashboard", label: "Dashboard", Icon: Ic.Home },
//   { id: "validation", label: "Validation", Icon: Ic.Shield },
//   { id: "risk", label: "Risk", Icon: Ic.Alert },
//   { id: "hitl", label: "HITL Queue", Icon: Ic.Users },
//   { id: "audit", label: "Audit Trail", Icon: Ic.Audit },
//   { id: "report", label: "Reports", Icon: Ic.Report },
//   { id: "auditchat", label: "Audit Chat", Icon: Ic.Chat },
// ];
// export default function App() {
//   const [tab, setTab] = useState("auditchat");
//   const [data, setData] = useState(null);
//   const [hitlDec, setHD] = useState({});
//   const [sidebar, setSB] = useState(true);
//   const onComplete = useCallback(result => {
//     setData({ ...result, hitl_queue: result.hitl_queue || [], corrections: result.corrections || result.report_json?.corrections || [], report_json: result.report_json || {} });
//     setHD({}); setTab("dashboard");
//   }, []);
//   const onDecision = useCallback((id, dec, res) => { setHD(d => ({ ...d, [id]: { dec, res } })); }, []);
//   const totalHITL = data?.hitl_queue?.length || (data?.final_trades || []).filter(t => t.final_status === "HITL").length;
//   const pendingHITL = Math.max(0, totalHITL - Object.keys(hitlDec).length);
//   return (
//     <>
//       <style>{`@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap'); *,*::before,*::after{box-sizing:border-box;margin:0;padding:0} html,body,#root{height:100%} body{font-family:${FONT.body};background:${C.bg};color:${C.ink};-webkit-font-smoothing:antialiased;font-size:14px;line-height:1.5} @keyframes spin{to{transform:rotate(360deg)}} @keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}} @keyframes pulseRing{0%,100%{opacity:1}50%{opacity:.5}} ::-webkit-scrollbar{width:5px;height:5px} ::-webkit-scrollbar-thumb{background:${C.border};border-radius:3px} ::-webkit-scrollbar-thumb:hover{background:${C.borderMid}} ::selection{background:rgba(0,86,197,.15)} textarea,input,button{font-family:inherit} textarea{resize:vertical} main > div{animation:fadeUp .22s ease both}`}</style>
//       <div style={{ display: "flex", height: "100vh", overflow: "hidden", background: C.bg }}>
//         {/* SIDEBAR */}
//         <aside style={{ width: sidebar ? 216 : 60, background: C.surface, borderRight: `1px solid ${C.border}`, display: "flex", flexDirection: "column", flexShrink: 0, transition: "width .24s cubic-bezier(.4,0,.2,1)", overflow: "hidden" }}>
//           <div style={{ padding: "16px", borderBottom: `1px solid ${C.border}`, display: "flex", alignItems: "center", gap: 9, minHeight: 58 }}>
//             <div style={{ width: 30, height: 30, borderRadius: 9, background: `linear-gradient(135deg,${C.blue},${C.blueDark})`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, boxShadow: `0 4px 10px rgba(0,86,197,.3)` }}>
//               <Ic.Shield style={{ width: 14, height: 14, color: "#fff" }} />
//             </div>
//             {sidebar && <div style={{ overflow: "hidden", flex: 1 }}>
//               <p style={{ margin: 0, fontSize: 13, fontWeight: 800, color: C.ink, fontFamily: FONT.display, letterSpacing: "-.02em", whiteSpace: "nowrap" }}>MiFID II AI</p>
//               <p style={{ margin: 0, fontSize: 10, color: C.inkFaint, whiteSpace: "nowrap" }}>Agentic Control Center</p>
//             </div>}
//             <button onClick={() => setSB(s => !s)} style={{ background: "none", border: "none", cursor: "pointer", color: C.inkFaint, padding: 3, marginLeft: sidebar ? "0" : "auto", flexShrink: 0, display: "flex" }}>
//               <Ic.ChevR style={{ width: 14, height: 14, transform: sidebar ? "rotate(180deg)" : "none", transition: "transform .2s" }} />
//             </button>
//           </div>
//           <nav style={{ padding: "8px", flex: 1, overflowY: "auto" }}>
//             {NAV.map(({ id, label, Icon }) => {
//               const active = tab === id; const badge = id === "hitl" && pendingHITL > 0 ? pendingHITL : null;
//               return (
//                 <button key={id} onClick={() => setTab(id)}
//                   style={{ width: "100%", display: "flex", alignItems: "center", gap: 9, padding: sidebar ? "9px 11px" : "9px", borderRadius: 8, border: "none", background: active ? C.blueTint : "transparent", color: active ? C.blue : C.inkMuted, fontSize: 13, fontWeight: active ? 700 : 400, transition: "all .13s", marginBottom: 2, cursor: "pointer", textAlign: "left", fontFamily: FONT.body, whiteSpace: "nowrap", overflow: "hidden", position: "relative" }}
//                   onMouseEnter={e => { if (!active) e.currentTarget.style.background = C.bg; }}
//                   onMouseLeave={e => { if (!active) e.currentTarget.style.background = "transparent"; }}>
//                   {active && <span style={{ position: "absolute", left: 0, top: "18%", bottom: "18%", width: 3, background: C.blue, borderRadius: "0 2px 2px 0" }} />}
//                   <Icon style={{ width: 17, height: 17, flexShrink: 0 }} />
//                   {sidebar && <><span style={{ flex: 1 }}>{label}</span>{badge && <span style={{ background: C.amberTint, color: C.amber, borderRadius: 10, padding: "1px 7px", fontSize: 10, fontWeight: 700, fontFamily: FONT.mono, border: `1px solid ${C.amberBorder}` }}>{badge}</span>}</>}
//                 </button>
//               );
//             })}
//           </nav>
//           {sidebar && data && (
//             <div style={{ padding: "12px 14px", borderTop: `1px solid ${C.border}` }}>
//               <div style={{ padding: "9px 11px", background: C.greenTint, borderRadius: 8, border: `1px solid ${C.greenBorder}` }}>
//                 <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 3 }}>
//                   <span style={{ width: 6, height: 6, borderRadius: "50%", background: C.green, animation: "pulseRing 1.5s ease infinite", boxShadow: `0 0 5px ${C.green}` }} />
//                   <span style={{ fontSize: 10, fontWeight: 700, color: C.green, fontFamily: FONT.mono }}>SYSTEM ONLINE</span>
//                 </div>
//                 <p style={{ margin: 0, fontSize: 10, color: C.inkMuted, fontFamily: FONT.mono, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{data.run_id}</p>
//               </div>
//             </div>
//           )}
//         </aside>
//         {/* MAIN */}
//         <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
//           <header style={{ height: 54, background: C.surface, borderBottom: `1px solid ${C.border}`, display: "flex", alignItems: "center", padding: "0 20px", gap: 14, flexShrink: 0 }}>
//             <button onClick={() => setSB(s => !s)} style={{ background: "none", border: "none", cursor: "pointer", color: C.inkMuted, padding: 6, borderRadius: 6, display: "flex", marginRight: 2 }}>
//               <Ic.Menu style={{ width: 15, height: 15 }} />
//             </button>
//             <div style={{ width: 1, height: 18, background: C.border }} />
//             <div style={{ display: "flex", gap: 5, alignItems: "center", fontSize: 13 }}>
//               <span style={{ color: C.inkFaint }}>MiFID AI</span>
//               <Ic.ChevR style={{ width: 12, height: 12, color: C.border }} />
//               <span style={{ color: C.ink, fontWeight: 600 }}>{NAV.find(n => n.id === tab)?.label}</span>
//             </div>
//             <div style={{ flex: 1 }} />
//             {data && (
//               <div style={{ display: "flex", gap: 6, padding: "5px 12px", background: C.surfaceAlt, borderRadius: 8, fontSize: 11, color: C.inkMuted, border: `1px solid ${C.border}`, fontFamily: FONT.mono }}>
//                 <span>Total:<strong style={{ color: C.ink, marginLeft: 4 }}>{data.stats?.total || 0}</strong></span>
//                 <span style={{ color: C.border }}>|</span>
//                 <span>Pass:<strong style={{ color: C.green, marginLeft: 4 }}>{data.stats?.passed || 0}</strong></span>
//                 <span style={{ color: C.border }}>|</span>
//                 <span>HITL:<strong style={{ color: C.amber, marginLeft: 4 }}>{pendingHITL}</strong></span>
//                 <span style={{ color: C.border }}>|</span>
//                 <span>Fail:<strong style={{ color: C.red, marginLeft: 4 }}>{(data?.final_trades || []).filter(t => t.final_status === "FAIL").length}</strong></span>
//               </div>
//             )}
//             <div style={{ width: 30, height: 30, borderRadius: "50%", background: `linear-gradient(135deg,${C.blue},${C.blueDark})`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 800, color: "#fff", fontFamily: FONT.display, flexShrink: 0 }}>A</div>
//           </header>
//           <main style={{ flex: 1, overflowY: "auto", padding: 22 }}>
//             <div>
              
//               {tab === "merge" && <MergeTab onComplete={onComplete} />}
//               {tab === "auditchat" && <AuditChatTab onComplete={onComplete} />}
//               {tab === "dashboard" && <DashboardTab data={data} />}
//               {tab === "validation" && <ValidationTab results={data?.validation_results || []} complianceResults={data?.compliance_results || []} />}
//               {tab === "risk" && <RiskTab results={data?.risk_results || []} />}
//               {tab === "hitl" && <HITLTab data={data} runId={data?.run_id} onDecision={onDecision} />}
//               {tab === "audit" && <AuditTab runId={data?.run_id} />}
//               {tab === "report" && <ReportTab data={data} />}
//               {tab === "db" && <DbTab />}
//               {tab === "auditchat" && <AuditChatTab />}
//             </div>
//           </main>
//         </div>
//       </div>
//     </>
//   );
// }





import { useState, useEffect, useCallback, useRef } from "react";
import axios from "axios";

// ─── API ──────────────────────────────────────────────────────────────────────
const api = axios.create({ baseURL: "/api", timeout: 30000000 });
const runPipelineApi     = (body) => api.post("/run-pipeline", body);
const submitHitlDecision = (b)    => api.post("/hitl/decision", b);
const submitBulkHitl     = (b)    => api.post("/hitl/bulk", b);
const getAuditLog        = (id)   => api.get(`/audit/${id}`);
const getHitlQueue       = (id)   => api.get(`/hitl/${id}`);
const fetchDbTrades      = ()     => api.get("/sources/db");
const fetchCsvTrades     = ()     => api.get("/sources/csv");
const fetchAllTrades     = ()     => api.get("/sources/all");
const sendAuditQuery     = (q)    => api.post("/audit-query", { query: q });

// ─── DESIGN TOKENS ────────────────────────────────────────────────────────────
const C = {
  blue:"#0056C5", blueHov:"#0047A8", blueDark:"#003D8F", blueTint:"#EBF2FF",
  bg:"#F4F6F9", surface:"#FFFFFF", surfaceAlt:"#F8FAFC",
  border:"rgba(15,23,42,0.08)", borderMid:"rgba(15,23,42,0.13)",
  ink:"#0F172A", inkMid:"#334155", inkMuted:"#64748B", inkFaint:"#94A3B8",
  green:"#0F7B52", greenTint:"#ECFDF5", greenBorder:"rgba(15,123,82,0.2)",
  amber:"#B45309", amberTint:"#FFFBEB", amberBorder:"rgba(180,83,9,0.2)",
  red:"#BE123C", redTint:"#FFF1F2", redBorder:"rgba(190,18,60,0.2)",
  violet:"#6D28D9", violetTint:"#F5F3FF", violetBorder:"rgba(109,40,217,0.18)",
  cyan:"#0E7490", cyanTint:"#ECFEFF",
  warning:"#92400E",
};
const FONT = {
  display:"'Plus Jakarta Sans','DM Sans',system-ui,sans-serif",
  body:"'DM Sans',system-ui,sans-serif",
  mono:"'DM Mono','SF Mono',monospace",
};

// ─── ICONS ────────────────────────────────────────────────────────────────────
const mk = (children, vb="0 0 24 24") => (p) => (
  <svg {...p} viewBox={vb} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{children}</svg>
);
const Ic = {
  Home:     mk(<><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></>),
  Shield:   mk(<><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></>),
  Alert:    mk(<><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><circle cx="12" cy="17" r=".5" fill="currentColor"/></>),
  Users:    mk(<><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></>),
  Audit:    mk(<><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></>),
  Report:   mk(<><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></>),
  Upload:   mk(<><polyline points="16,16 12,12 8,16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0018 9h-1.26A8 8 0 103 16.3"/></>),
  Check:    mk(<polyline points="20,6 9,17 4,12" strokeWidth="2.5"/>),
  X:        mk(<><line x1="18" y1="6" x2="6" y2="18" strokeWidth="2.5"/><line x1="6" y1="6" x2="18" y2="18" strokeWidth="2.5"/></>),
  Edit:     mk(<><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></>),
  Refresh:  mk(<><polyline points="23,4 23,10 17,10"/><path d="M20.49 15a9 9 0 11-2.12-9.36L23 10"/></>),
  Download: mk(<><polyline points="8,17 12,21 16,17"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.88 18.09A5 5 0 0018 9h-1.26A8 8 0 103 16.3"/></>),
  ChevR:    mk(<polyline points="9,18 15,12 9,6" strokeWidth="2"/>),
  Menu:     mk(<><line x1="3" y1="12" x2="21" y2="12" strokeWidth="2"/><line x1="3" y1="6" x2="21" y2="6" strokeWidth="2"/><line x1="3" y1="18" x2="21" y2="18" strokeWidth="2"/></>),
  Wand:     mk(<><path d="M15 4V2M15 16v-2M8 9h2M20 9h2M17.8 11.8L19.2 13.2M15 9h0M17.8 6.2L19.2 4.8M3 21l9-9M12.2 6.2L10.8 4.8"/></>),
  Layer:    mk(<><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"/><line x1="12" y1="22" x2="12" y2="15.5"/><polyline points="22 8.5 12 15.5 2 8.5"/></>),
  Copy:     mk(<><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></>),
  Info:     mk(<><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></>),
  Zap:      mk(<><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></>),
  Send:     mk(<><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></>),
  Chat:     mk(<><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></>),
  Bot:      mk(<><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4M8 15h0M16 15h0"/></>),
  Sparkle:  mk(<><path d="M12 3L13.5 8.5L19 10L13.5 11.5L12 17L10.5 11.5L5 10L10.5 8.5L12 3Z"/><path d="M5 3l.8 2.2L8 6l-2.2.8L5 9l-.8-2.2L2 6l2.2-.8L5 3Z" strokeWidth="1.2"/></>),
  Database: mk(<><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></>),
  Clock:    mk(<><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></>),
  TrendUp:  mk(<><polyline points="23,6 13.5,15.5 8.5,10.5 1,18"/><polyline points="17,6 23,6 23,12"/></>),
};

// ─── PRIMITIVES ───────────────────────────────────────────────────────────────
function Spinner({ size=16, color=C.blue }) {
  return <span style={{ display:"inline-block", width:size, height:size, border:`2px solid ${color}25`, borderTopColor:color, borderRadius:"50%", animation:"spin .75s linear infinite", flexShrink:0 }} />;
}

const SEV = {
  PASS:[C.greenTint,C.green,C.greenBorder], APPROVED:[C.greenTint,C.green,C.greenBorder],
  true:[C.greenTint,C.green,C.greenBorder], LOW:[C.greenTint,C.green,C.greenBorder],
  HITL:[C.amberTint,C.amber,C.amberBorder], PENDING:[C.amberTint,C.amber,C.amberBorder],
  MEDIUM:[C.amberTint,C.amber,C.amberBorder],
  FAIL:[C.redTint,C.red,C.redBorder], HIGH:[C.redTint,C.red,C.redBorder],
  CRITICAL:[C.redTint,C.red,C.redBorder], REJECTED:[C.redTint,C.red,C.redBorder],
  false:[C.redTint,C.red,C.redBorder],
  APPLIED:[C.violetTint,C.violet,C.violetBorder],
  MODIFIED:[C.blueTint,C.blue,"rgba(0,86,197,.2)"], NEWT:[C.blueTint,C.blue,"rgba(0,86,197,.2)"],
  AMND:[C.cyanTint,C.cyan,"rgba(14,116,144,.2)"], NONE:[C.surfaceAlt,C.inkFaint,C.border],
};

function Badge({ status, size="sm", pulse=false }) {
  const [bg,fg,bd] = SEV[String(status)] || [C.surfaceAlt,C.inkMuted,C.border];
  const fs = size==="lg"?12:size==="xs"?10:11;
  const px = size==="lg"?10:size==="xs"?6:8;
  return (
    <span style={{ display:"inline-flex", alignItems:"center", gap:5, background:bg, color:fg, border:`1px solid ${bd}`, borderRadius:4, padding:`${size==="lg"?4:2}px ${px}px`, fontSize:fs, fontWeight:700, whiteSpace:"nowrap", fontFamily:FONT.mono, letterSpacing:".03em" }}>
      <span style={{ width:5, height:5, borderRadius:"50%", background:fg, flexShrink:0, ...(pulse?{animation:"pulseRing 1.5s ease infinite"}:{}) }} />
      {String(status).toUpperCase()}
    </span>
  );
}

function ConfBar({ value, status, compact=false }) {
  const pct = Math.max(0, Math.min(100, Math.round((value||0)*100)));
  let color = status==="PASS"||status==="APPROVED"||status===true ? C.green
    : status==="HITL"||status==="PENDING" ? C.amber
    : status==="FAIL"||status==="REJECTED"||status===false ? C.red
    : pct>=70 ? C.green : pct>=40 ? C.amber : C.red;
  return (
    <div style={{ display:"flex", alignItems:"center", gap:8 }}>
      <div style={{ flex:1, height:compact?4:6, background:C.border, borderRadius:4, overflow:"hidden" }}>
        <div style={{ width:`${pct}%`, height:"100%", background:color, borderRadius:4, transition:"width .5s ease" }} />
      </div>
      <span style={{ fontSize:11, color, minWidth:28, textAlign:"right", fontFamily:FONT.mono, fontWeight:700 }}>{pct}%</span>
    </div>
  );
}

function Btn({ children, variant="primary", onClick, disabled, icon:Icon, size="md", full=false, loading=false, style:extraStyle }) {
  const [hov,sH] = useState(false);
  const V = {
    primary:  {bg:hov&&!disabled?C.blueHov:C.blue, fg:"#fff", bd:"none"},
    secondary:{bg:hov&&!disabled?C.bg:C.surface, fg:C.inkMid, bd:`1px solid ${C.borderMid}`},
    ghost:    {bg:hov&&!disabled?C.bg:"transparent", fg:C.blue, bd:`1px solid ${C.borderMid}`},
    danger:   {bg:hov&&!disabled?"#9F1239":C.red, fg:"#fff", bd:"none"},
    success:  {bg:hov&&!disabled?"#065F46":C.green, fg:"#fff", bd:"none"},
    amber:    {bg:hov&&!disabled?"#92400E":C.amber, fg:"#fff", bd:"none"},
    violet:   {bg:hov&&!disabled?"#5B21B6":C.violet, fg:"#fff", bd:"none"},
  }[variant]||{};
  const sz = size==="sm"?{p:"5px 12px",fs:12}:size==="xs"?{p:"3px 9px",fs:11}:{p:"8px 16px",fs:13};
  return (
    <button onClick={disabled?undefined:onClick} onMouseEnter={()=>sH(true)} onMouseLeave={()=>sH(false)} disabled={disabled}
      style={{ display:"inline-flex", alignItems:"center", gap:6, padding:sz.p, fontSize:sz.fs, fontWeight:600, borderRadius:7, border:V.bd, background:V.bg, color:V.fg, cursor:disabled?"not-allowed":"pointer", opacity:disabled?.55:1, transition:"all .14s", fontFamily:FONT.body, width:full?"100%":"auto", justifyContent:"center", ...extraStyle }}>
      {loading?<Spinner size={size==="sm"?12:14} color={V.fg}/>:Icon?<Icon style={{ width:size==="sm"?13:15, height:size==="sm"?13:15, flexShrink:0 }}/>:null}
      {children}
    </button>
  );
}

function Card({ children, style, accent, noPad=false, onClick }) {
  const [hov,sH] = useState(false);
  return (
    <div onClick={onClick} onMouseEnter={()=>onClick&&sH(true)} onMouseLeave={()=>onClick&&sH(false)}
      style={{ background:C.surface, borderRadius:12, border:`1px solid ${C.border}`, boxShadow:hov?"0 8px 24px rgba(15,23,42,.09)":"0 1px 4px rgba(15,23,42,.04)", transition:"box-shadow .2s,transform .15s", transform:hov&&onClick?"translateY(-1px)":"none", cursor:onClick?"pointer":"default", overflow:"hidden", position:"relative", ...(accent&&{borderTop:`3px solid ${accent}`}), ...style }}>
      {children}
    </div>
  );
}

function CardHeader({ title, sub, right, border=true }) {
  return (
    <div style={{ padding:"13px 18px", ...(border&&{borderBottom:`1px solid ${C.border}`}), display:"flex", justifyContent:"space-between", alignItems:"center", gap:12 }}>
      <div>
        <p style={{ margin:0, fontSize:13, fontWeight:700, color:C.ink, fontFamily:FONT.display }}>{title}</p>
        {sub&&<p style={{ margin:"2px 0 0", fontSize:11, color:C.inkFaint }}>{sub}</p>}
      </div>
      {right&&<div style={{ flexShrink:0 }}>{right}</div>}
    </div>
  );
}

function StatCard({ label, value, sub, accent, icon:Icon }) {
  return (
    <Card style={{ padding:"18px 20px" }} accent={accent}>
      <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start" }}>
        <div style={{ flex:1, minWidth:0 }}>
          <p style={{ margin:0, fontSize:10, fontWeight:700, color:C.inkFaint, textTransform:"uppercase", letterSpacing:".08em" }}>{label}</p>
          <p style={{ margin:"7px 0 0", fontSize:28, fontWeight:800, color:C.ink, fontFamily:FONT.display, lineHeight:1, letterSpacing:"-.02em" }}>{value??'—'}</p>
          {sub&&<p style={{ margin:"5px 0 0", fontSize:11, color:C.inkMuted }}>{sub}</p>}
        </div>
        {Icon&&<div style={{ width:38, height:38, borderRadius:10, background:accent+"18", display:"flex", alignItems:"center", justifyContent:"center", color:accent, flexShrink:0 }}><Icon style={{ width:18,height:18 }}/></div>}
      </div>
    </Card>
  );
}

function Empty({ icon:Icon=Ic.Layer, title, sub }) {
  return (
    <div style={{ display:"flex", flexDirection:"column", alignItems:"center", padding:"64px 24px", textAlign:"center" }}>
      <div style={{ width:52, height:52, borderRadius:14, background:C.bg, border:`1px solid ${C.border}`, display:"flex", alignItems:"center", justifyContent:"center", marginBottom:14 }}>
        <Icon style={{ width:22, height:22, color:C.inkFaint }}/>
      </div>
      <p style={{ margin:0, fontSize:14, fontWeight:700, color:C.ink, fontFamily:FONT.display }}>{title}</p>
      {sub&&<p style={{ margin:"6px 0 0", fontSize:12, color:C.inkMuted, maxWidth:320 }}>{sub}</p>}
    </div>
  );
}

function SectionHeader({ title, sub, actions }) {
  return (
    <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start", marginBottom:20, gap:16 }}>
      <div>
        <h2 style={{ margin:0, fontSize:20, fontWeight:800, color:C.ink, fontFamily:FONT.display, letterSpacing:"-.02em" }}>{title}</h2>
        {sub&&<p style={{ margin:"5px 0 0", fontSize:13, color:C.inkMuted }}>{sub}</p>}
      </div>
      {actions&&<div style={{ display:"flex", gap:8, flexShrink:0, flexWrap:"wrap", justifyContent:"flex-end" }}>{actions}</div>}
    </div>
  );
}

function Pill({ label, color=C.blue }) {
  return (
    <span style={{ display:"inline-flex", alignItems:"center", gap:5, padding:"3px 10px", background:color+"15", color, borderRadius:20, fontSize:11, fontWeight:700, letterSpacing:".04em", border:`1px solid ${color}20`, fontFamily:FONT.mono }}>
      <span style={{ width:5, height:5, borderRadius:"50%", background:color, animation:"pulseRing 2s ease infinite" }}/>
      {label}
    </span>
  );
}

// ─── MODIFY MODAL ─────────────────────────────────────────────────────────────
function ModifyModal({ trade, runId, onClose, onSuccess }) {
  const FIELDS = ["isin","executing_entity_lei","buyer_lei","seller_lei","price","currency","quantity","venue","notional_amount","report_status","instrument_type","trade_datetime"];
  const [fields,setFields] = useState(() => { const o={}; FIELDS.forEach(k=>{ if(trade[k]!==undefined) o[k]=String(trade[k]); }); return o; });
  const [note,setNote] = useState(""); const [busy,setBusy] = useState(false); const [err,setErr] = useState(null);
  const submit = async () => {
    setBusy(true); setErr(null);
    try { const res=await submitHitlDecision({ run_id:runId, trade_id:trade.trade_id, decision:"MODIFIED", modified_fields:{...fields,trade_id:trade.trade_id}, reviewer_note:note }); onSuccess(res.data); }
    catch(e){ setErr(e.response?.data?.detail||e.message); setBusy(false); }
  };
  return (
    <div style={{ position:"fixed", inset:0, background:"rgba(15,23,42,.55)", backdropFilter:"blur(8px)", zIndex:1000, display:"flex", alignItems:"center", justifyContent:"center", padding:16 }}>
      <div style={{ background:C.surface, borderRadius:16, width:"100%", maxWidth:660, maxHeight:"92vh", overflowY:"auto", boxShadow:"0 32px 80px rgba(15,23,42,.22)", border:`1px solid ${C.border}` }}>
        <div style={{ padding:"18px 22px", borderBottom:`1px solid ${C.border}`, display:"flex", justifyContent:"space-between", alignItems:"center", position:"sticky", top:0, background:C.surface, zIndex:1 }}>
          <div style={{ display:"flex", gap:10, alignItems:"center" }}>
            <div style={{ width:32,height:32,borderRadius:8,background:C.amberTint,border:`1px solid ${C.amberBorder}`,display:"flex",alignItems:"center",justifyContent:"center",color:C.amber }}><Ic.Edit style={{ width:15,height:15 }}/></div>
            <div><h3 style={{ margin:0,fontSize:15,fontWeight:800,color:C.ink,fontFamily:FONT.display }}>Modify Trade Fields</h3><p style={{ margin:0,fontSize:11,color:C.inkFaint,fontFamily:FONT.mono }}>{trade.trade_id}</p></div>
          </div>
          <button onClick={onClose} style={{ background:C.bg,border:`1px solid ${C.border}`,borderRadius:7,cursor:"pointer",color:C.inkMuted,padding:6,display:"flex" }}><Ic.X style={{ width:15,height:15 }}/></button>
        </div>
        <div style={{ padding:"20px 22px" }}>
          <div style={{ background:C.amberTint,border:`1px solid ${C.amberBorder}`,borderRadius:8,padding:"10px 14px",marginBottom:18,display:"flex",gap:8 }}>
            <Ic.Info style={{ width:14,height:14,color:C.amber,flexShrink:0,marginTop:1 }}/>
            <p style={{ margin:0,fontSize:12,color:C.warning,lineHeight:1.5 }}>Modifying and re-running will reprocess this trade through the full pipeline. Original values are preserved in the audit trail.</p>
          </div>
          <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,marginBottom:16 }}>
            {Object.entries(fields).map(([k,v])=>(
              <div key={k}>
                <label style={{ display:"block",fontSize:10,fontWeight:700,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".08em",marginBottom:5 }}>{k.replace(/_/g," ")}</label>
                <input value={v} onChange={e=>setFields(f=>({...f,[k]:e.target.value}))}
                  onFocus={e=>{e.target.style.borderColor=C.blue;e.target.style.boxShadow=`0 0 0 3px ${C.blue}15`;}}
                  onBlur={e=>{e.target.style.borderColor=C.border;e.target.style.boxShadow="none";}}
                  style={{ width:"100%",padding:"8px 11px",border:`1px solid ${C.border}`,borderRadius:7,fontSize:12,color:C.ink,background:C.surfaceAlt,outline:"none",fontFamily:FONT.mono,boxSizing:"border-box",transition:"border-color .14s,box-shadow .14s" }}/>
              </div>
            ))}
          </div>
          <label style={{ display:"block",fontSize:10,fontWeight:700,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".08em",marginBottom:5 }}>Reviewer Note</label>
          <textarea value={note} onChange={e=>setNote(e.target.value)} rows={3} placeholder="Explain the correction rationale…"
            style={{ width:"100%",padding:"10px 12px",border:`1px solid ${C.border}`,borderRadius:7,fontSize:13,color:C.ink,background:C.surfaceAlt,outline:"none",resize:"vertical",fontFamily:FONT.body,boxSizing:"border-box" }}/>
          {err&&<div style={{ marginTop:12,padding:"10px 13px",background:C.redTint,border:`1px solid ${C.redBorder}`,borderRadius:7,fontSize:12,color:C.red,display:"flex",gap:8 }}><Ic.Alert style={{ width:13,height:13,flexShrink:0 }}/>{err}</div>}
        </div>
        <div style={{ padding:"14px 22px",borderTop:`1px solid ${C.border}`,display:"flex",gap:8,justifyContent:"flex-end",background:C.surfaceAlt }}>
          <Btn variant="secondary" onClick={onClose}>Cancel</Btn>
          <Btn variant="amber" onClick={submit} disabled={busy} icon={busy?null:Ic.Refresh} loading={busy}>{busy?"Re-processing…":"Submit & Re-run Pipeline"}</Btn>
        </div>
      </div>
    </div>
  );
}

// ─── AUDIT CHAT TAB ───────────────────────────────────────────────────────────
const QUICK_QUERIES = [
  { label:"Failed trades today",     icon:Ic.Alert,    query:"Show me all trades that failed validation today" },
  { label:"T+1 sweep",               icon:Ic.Clock,    query:"Run a T+1 compliance check for yesterday's unreported trades" },
  { label:"HITL queue review",       icon:Ic.Users,    query:"Show me all trades currently waiting for human review" },
  { label:"Compliance summary",      icon:Ic.Shield,   query:"Give me a compliance summary for this week's trades" },
  { label:"Auto-corrected trades",   icon:Ic.Wand,     query:"Show me all trades that were auto-corrected by the enrichment agent" },
  { label:"Wash trade alerts",       icon:Ic.TrendUp,  query:"Are there any wash trade violations detected in recent batches?" },
];

function TypingDots() {
  return (
    <div style={{ display:"flex", gap:4, alignItems:"center", padding:"4px 0" }}>
      {[0,1,2].map(i=>(
        <span key={i} style={{ width:7, height:7, borderRadius:"50%", background:C.inkFaint, display:"block", animation:`typingBounce .9s ease-in-out ${i*0.15}s infinite` }}/>
      ))}
    </div>
  );
}

function ChatBubble({ msg }) {
  const isUser      = msg.role === "user";
  const isAssistant = msg.role === "assistant";
  const isSystem    = msg.role === "system";
  const isError     = msg.role === "error";

  if (isSystem) {
    return (
      <div style={{ display:"flex", justifyContent:"center", marginBottom:16 }}>
        <div style={{ background:C.blueTint, border:`1px solid ${C.border}`, borderRadius:20, padding:"6px 16px", fontSize:12, color:C.blue, fontWeight:600 }}>
          {msg.text}
        </div>
      </div>
    );
  }

  if (isUser) {
    return (
      <div style={{ display:"flex", justifyContent:"flex-end", marginBottom:16 }}>
        <div style={{ maxWidth:"72%", background:C.blue, color:"#fff", borderRadius:"18px 18px 4px 18px", padding:"12px 16px", fontSize:13, lineHeight:1.6, fontFamily:FONT.body, boxShadow:"0 2px 8px rgba(0,86,197,.25)" }}>
          {msg.text}
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div style={{ display:"flex", gap:10, marginBottom:16, alignItems:"flex-start" }}>
        <div style={{ width:32, height:32, borderRadius:"50%", background:C.redTint, border:`1px solid ${C.redBorder}`, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
          <Ic.Alert style={{ width:14, height:14, color:C.red }}/>
        </div>
        <div style={{ background:C.redTint, border:`1px solid ${C.redBorder}`, borderRadius:"4px 18px 18px 18px", padding:"12px 16px", fontSize:13, color:C.red, maxWidth:"80%" }}>
          {msg.text}
        </div>
      </div>
    );
  }

  // Assistant message
  const stats = msg.stats || {};
  const hasStats = stats.total > 0;
  const breakdown = msg.source_breakdown || {};

  return (
    <div style={{ display:"flex", gap:10, marginBottom:20, alignItems:"flex-start" }}>
      {/* Avatar */}
      <div style={{ width:32, height:32, borderRadius:"50%", background:`linear-gradient(135deg,${C.blue},${C.blueDark})`, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0, boxShadow:"0 2px 8px rgba(0,86,197,.3)" }}>
        <Ic.Bot style={{ width:14, height:14, color:"#fff" }}/>
      </div>

      <div style={{ flex:1, maxWidth:"85%" }}>
        {/* Narrative */}
        <div style={{ background:C.surface, border:`1px solid ${C.border}`, borderRadius:"4px 18px 18px 18px", padding:"14px 18px", fontSize:13, color:C.inkMid, lineHeight:1.8, fontFamily:FONT.body, boxShadow:"0 1px 4px rgba(15,23,42,.04)" }}>
          {msg.text}
        </div>

        {/* Stats pills */}
        {hasStats && (
          <div style={{ display:"flex", gap:8, marginTop:10, flexWrap:"wrap" }}>
            <span style={{ display:"inline-flex", alignItems:"center", gap:5, padding:"4px 10px", background:C.blueTint, color:C.blue, borderRadius:6, fontSize:11, fontWeight:700, fontFamily:FONT.mono, border:`1px solid ${C.border}` }}>
              <Ic.Layer style={{ width:11,height:11 }}/> {stats.total} trades
            </span>
            {stats.passed>0 && <span style={{ display:"inline-flex", alignItems:"center", gap:5, padding:"4px 10px", background:C.greenTint, color:C.green, borderRadius:6, fontSize:11, fontWeight:700, fontFamily:FONT.mono, border:`1px solid ${C.greenBorder}` }}>
              <Ic.Check style={{ width:11,height:11 }}/> {stats.passed} passed
            </span>}
            {stats.hitl>0 && <span style={{ display:"inline-flex", alignItems:"center", gap:5, padding:"4px 10px", background:C.amberTint, color:C.amber, borderRadius:6, fontSize:11, fontWeight:700, fontFamily:FONT.mono, border:`1px solid ${C.amberBorder}` }}>
              <Ic.Users style={{ width:11,height:11 }}/> {stats.hitl} review needed
            </span>}
            {stats.fail>0 && <span style={{ display:"inline-flex", alignItems:"center", gap:5, padding:"4px 10px", background:C.redTint, color:C.red, borderRadius:6, fontSize:11, fontWeight:700, fontFamily:FONT.mono, border:`1px solid ${C.redBorder}` }}>
              <Ic.Alert style={{ width:11,height:11 }}/> {stats.fail} failed
            </span>}
            {stats.auto_fixed>0 && <span style={{ display:"inline-flex", alignItems:"center", gap:5, padding:"4px 10px", background:C.violetTint, color:C.violet, borderRadius:6, fontSize:11, fontWeight:700, fontFamily:FONT.mono, border:`1px solid ${C.violetBorder}` }}>
              <Ic.Wand style={{ width:11,height:11 }}/> {stats.auto_fixed} auto-fixed
            </span>}
          </div>
        )}

        {/* Run ID */}
        {msg.run_id && (
          <p style={{ margin:"8px 0 0", fontSize:10, color:C.inkFaint, fontFamily:FONT.mono }}>
            Run ID: {msg.run_id} · <span style={{ color:C.blue, cursor:"pointer" }}>View full report →</span>
          </p>
        )}
      </div>
    </div>
  );
}

function AuditChatTab({ onComplete }) {
  const [messages, setMessages] = useState([
    { role:"system", text:"MiFID II Audit Assistant — Ask about trades, exceptions, T+1 checks, compliance summaries, or HITL reviews." }
  ]);
  const [query,   setQuery]   = useState("");
  const [busy,    setBusy]    = useState(false);
  const [lastRes, setLastRes] = useState(null);
  const bottomRef = useRef(null);
  const inputRef  = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior:"smooth" }); }, [messages, busy]);
  useEffect(() => { inputRef.current?.focus(); }, []);

  const send = async (text) => {
    const q = (text || query).trim();
    if (!q || busy) return;
    setMessages(m => [...m, { role:"user", text:q }]);
    setQuery("");
    setBusy(true);
    try {
      const res = await sendAuditQuery(q);
      const data = res.data || {};
      setLastRes(data);
      if (typeof onComplete === "function" && data.run_id) onComplete(data);
      setMessages(m => [...m, {
        role:"assistant",
        text:    data.response || "Pipeline completed. No narrative returned.",
        run_id:  data.run_id   || "",
        stats:   data.stats    || {},
        source_breakdown: data.source_breakdown || {},
      }]);
    } catch(e) {
      setMessages(m => [...m, { role:"error", text: e.response?.data?.detail || e.message || "Request failed." }]);
    } finally {
      setBusy(false);
    }
  };

  const onKey = (e) => { if(e.key==="Enter"&&!e.shiftKey){ e.preventDefault(); send(); } };
  const clearChat = () => { setMessages([{ role:"system", text:"Chat cleared. Ready for your next query." }]); setLastRes(null); };

  const stats = lastRes?.stats || {};

  return (
    <div style={{ display:"grid", gridTemplateColumns:"1fr 300px", gap:16, height:"calc(100vh - 100px)", maxWidth:1200, margin:"0 auto" }}>

      {/* ─── MAIN CHAT PANEL ─────────────────────────────────────────────── */}
      <div style={{ display:"flex", flexDirection:"column", gap:0, minHeight:0 }}>

        {/* Header */}
        <div style={{ background:`linear-gradient(135deg,${C.blue} 0%,${C.blueDark} 100%)`, borderRadius:"12px 12px 0 0", padding:"18px 22px", flexShrink:0 }}>
          <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between" }}>
            <div style={{ display:"flex", alignItems:"center", gap:12 }}>
              <div style={{ width:40, height:40, borderRadius:10, background:"rgba(255,255,255,.15)", display:"flex", alignItems:"center", justifyContent:"center" }}>
                <Ic.Sparkle style={{ width:20, height:20, color:"#fff" }}/>
              </div>
              <div>
                <h2 style={{ margin:0, fontSize:16, fontWeight:800, color:"#fff", fontFamily:FONT.display }}>MiFID II Audit Intelligence</h2>
                <p style={{ margin:0, fontSize:11, color:"rgba(255,255,255,.6)" }}>Ask in plain English — system fetches, validates, and reports automatically</p>
              </div>
            </div>
            <div style={{ display:"flex", gap:8, alignItems:"center" }}>
              <div style={{ display:"flex", alignItems:"center", gap:5, background:"rgba(255,255,255,.12)", borderRadius:20, padding:"4px 12px" }}>
                <span style={{ width:6, height:6, borderRadius:"50%", background:"#4ade80", animation:"pulseRing 1.5s ease infinite" }}/>
                <span style={{ fontSize:11, color:"rgba(255,255,255,.85)", fontWeight:600, fontFamily:FONT.mono }}>LIVE</span>
              </div>
              <button onClick={clearChat} style={{ background:"rgba(255,255,255,.12)", border:"1px solid rgba(255,255,255,.2)", borderRadius:7, cursor:"pointer", color:"rgba(255,255,255,.7)", padding:"5px 10px", fontSize:11, display:"flex", alignItems:"center", gap:5 }}>
                <Ic.Refresh style={{ width:12,height:12 }}/> Clear
              </button>
            </div>
          </div>
        </div>

        {/* Messages area */}
        <div style={{ flex:1, overflowY:"auto", padding:"20px 20px 0", background:C.surfaceAlt, border:`1px solid ${C.border}`, borderTop:"none", minHeight:0 }}>
          {messages.map((m,i) => <ChatBubble key={i} msg={m}/>)}
          {busy && (
            <div style={{ display:"flex", gap:10, marginBottom:16, alignItems:"flex-start" }}>
              <div style={{ width:32, height:32, borderRadius:"50%", background:`linear-gradient(135deg,${C.blue},${C.blueDark})`, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
                <Ic.Bot style={{ width:14, height:14, color:"#fff" }}/>
              </div>
              <div style={{ background:C.surface, border:`1px solid ${C.border}`, borderRadius:"4px 18px 18px 18px", padding:"14px 18px" }}>
                <TypingDots/>
                <p style={{ margin:"6px 0 0", fontSize:11, color:C.inkFaint }}>Analyzing query → fetching trades → running pipeline…</p>
              </div>
            </div>
          )}
          <div ref={bottomRef}/>
        </div>

        {/* Quick queries */}
        <div style={{ padding:"10px 16px", background:C.surface, borderLeft:`1px solid ${C.border}`, borderRight:`1px solid ${C.border}`, display:"flex", gap:6, flexWrap:"wrap", borderTop:`1px solid ${C.border}` }}>
          {QUICK_QUERIES.map(({ label, icon:QIcon, query:q }) => (
            <button key={label} onClick={()=>send(q)} disabled={busy}
              style={{ display:"inline-flex", alignItems:"center", gap:5, padding:"5px 11px", background:C.bg, border:`1px solid ${C.border}`, borderRadius:20, fontSize:11, fontWeight:600, color:C.inkMid, cursor:"pointer", fontFamily:FONT.body, transition:"all .13s", opacity:busy?.5:1 }}
              onMouseEnter={e=>{e.target.style.borderColor=C.blue;e.target.style.color=C.blue;}}
              onMouseLeave={e=>{e.target.style.borderColor=C.border;e.target.style.color=C.inkMid;}}>
              <QIcon style={{ width:11,height:11 }}/> {label}
            </button>
          ))}
        </div>

        {/* Input */}
        <div style={{ background:C.surface, border:`1px solid ${C.border}`, borderTop:"none", borderRadius:"0 0 12px 12px", padding:"14px 16px", flexShrink:0 }}>
          <div style={{ display:"flex", gap:10, alignItems:"flex-end" }}>
            <textarea
              ref={inputRef}
              value={query}
              onChange={e=>setQuery(e.target.value)}
              onKeyDown={onKey}
              rows={2}
              placeholder='e.g. "Show me all failed trades from yesterday" or "Run T+1 check for XLON venue"'
              disabled={busy}
              style={{ flex:1, padding:"11px 14px", border:`1px solid ${C.border}`, borderRadius:10, fontSize:13, color:C.ink, background:busy?C.bg:C.surfaceAlt, outline:"none", resize:"none", fontFamily:FONT.body, lineHeight:1.5, transition:"border-color .14s", boxSizing:"border-box" }}
              onFocus={e=>{e.target.style.borderColor=C.blue;e.target.style.boxShadow=`0 0 0 3px ${C.blue}15`;}}
              onBlur={e=>{e.target.style.borderColor=C.border;e.target.style.boxShadow="none";}}
            />
            <button onClick={()=>send()} disabled={busy||!query.trim()}
              style={{ width:44, height:44, borderRadius:10, background:(!busy&&query.trim())?C.blue:C.border, border:"none", cursor:(!busy&&query.trim())?"pointer":"not-allowed", display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0, transition:"background .14s" }}>
              {busy ? <Spinner size={16} color="#fff"/> : <Ic.Send style={{ width:16,height:16,color:"#fff" }}/>}
            </button>
          </div>
          <p style={{ margin:"8px 0 0", fontSize:10, color:C.inkFaint, fontFamily:FONT.mono }}>
            Press Enter to send · Shift+Enter for new line · Intelligence layer fetches data automatically
          </p>
        </div>
      </div>

      {/* ─── RIGHT SIDE PANEL ────────────────────────────────────────────── */}
      <div style={{ display:"flex", flexDirection:"column", gap:12, overflowY:"auto" }}>

        {/* How it works */}
        <Card accent={C.blue}>
          <CardHeader title="How it works" sub="Agentic intelligence layer" border={false}/>
          <div style={{ padding:"0 18px 16px", display:"flex", flexDirection:"column", gap:8 }}>
            {[
              [Ic.Sparkle, C.violet, "Intent detection", "Classifies your query type"],
              [Ic.Bot,     C.blue,   "Planning agent",   "Decides what data to fetch"],
              [Ic.Database,C.green,  "Tool execution",   "Queries DB/GCS/Pub-Sub/BQ"],
              [Ic.Shield,  C.amber,  "Pipeline run",     "Full validation & compliance"],
              [Ic.Report,  C.cyan,   "LLM formatter",    "Produces readable report"],
            ].map(([Icon,color,label,sub],i)=>(
              <div key={i} style={{ display:"flex", gap:10, alignItems:"flex-start" }}>
                <div style={{ width:28, height:28, borderRadius:7, background:color+"15", display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0, color }}>
                  <Icon style={{ width:13,height:13 }}/>
                </div>
                <div>
                  <p style={{ margin:0, fontSize:12, fontWeight:700, color:C.ink }}>{label}</p>
                  <p style={{ margin:0, fontSize:11, color:C.inkFaint }}>{sub}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Last run stats */}
        <Card accent={C.green}>
          <CardHeader title="Last run summary" sub={lastRes?.run_id ? `Run: ${lastRes.run_id.slice(-8)}` : "No run yet"} border={false}/>
          <div style={{ padding:"0 18px 16px", display:"grid", gridTemplateColumns:"1fr 1fr", gap:8 }}>
            {[
              [stats.total||0,  "Total",       C.blue],
              [stats.passed||0, "Passed",      C.green],
              [stats.hitl||0,   "Review",      C.amber],
              [stats.fail||0,   "Failed",      C.red],
            ].map(([val,label,color])=>(
              <div key={label} style={{ padding:"10px 12px", background:color+"08", borderRadius:8, border:`1px solid ${color}20`, textAlign:"center" }}>
                <p style={{ margin:0, fontSize:20, fontWeight:800, color, fontFamily:FONT.display }}>{val}</p>
                <p style={{ margin:"2px 0 0", fontSize:10, color:C.inkFaint, textTransform:"uppercase", letterSpacing:".07em", fontWeight:700 }}>{label}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Example queries */}
        <Card>
          <CardHeader title="Example queries" sub="Click to try" border/>
          <div style={{ padding:"8px 12px 12px", display:"flex", flexDirection:"column", gap:4 }}>
            {[
              "Show all trades from PostgreSQL that failed BR-001 this week",
              "Pull yesterday's GCS file drop and validate all equity trades",
              "Which XLON trades are pending HITL approval?",
              "Run a full compliance sweep for SAP SE (DE0007164600)",
              "Show me all auto-corrected notional amounts from last batch",
            ].map((q,i)=>(
              <button key={i} onClick={()=>send(q)} disabled={busy}
                style={{ textAlign:"left", padding:"8px 10px", background:C.bg, border:`1px solid ${C.border}`, borderRadius:7, fontSize:11, color:C.inkMid, cursor:"pointer", lineHeight:1.4, fontFamily:FONT.body, opacity:busy?.5:1, transition:"all .13s" }}
                onMouseEnter={e=>{e.currentTarget.style.background=C.blueTint;e.currentTarget.style.borderColor=C.blue;e.currentTarget.style.color=C.blue;}}
                onMouseLeave={e=>{e.currentTarget.style.background=C.bg;e.currentTarget.style.borderColor=C.border;e.currentTarget.style.color=C.inkMid;}}>
                "{q}"
              </button>
            ))}
          </div>
        </Card>

        {/* Data sources status */}
        <Card>
          <CardHeader title="Data sources" sub="Intelligence layer targets" border/>
          <div style={{ padding:"8px 12px 12px", display:"flex", flexDirection:"column", gap:6 }}>
            {[
              [Ic.Database, C.green,  "PostgreSQL",    "Trade transactions DB"],
              [Ic.Layer,    C.violet, "GCS Bucket",    "CSV / JSON file drops"],
              [Ic.TrendUp,  C.amber,  "Pub/Sub",       "Real-time trade events"],
              [Ic.Zap,      C.blue,   "BigQuery",      "Historical analytics"],
            ].map(([Icon,color,name,desc])=>(
              <div key={name} style={{ display:"flex", gap:10, alignItems:"center", padding:"8px 10px", background:C.surfaceAlt, borderRadius:8, border:`1px solid ${C.border}` }}>
                <div style={{ width:28, height:28, borderRadius:6, background:color+"15", display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0, color }}>
                  <Icon style={{ width:13,height:13 }}/>
                </div>
                <div style={{ flex:1, minWidth:0 }}>
                  <p style={{ margin:0, fontSize:12, fontWeight:700, color:C.ink }}>{name}</p>
                  <p style={{ margin:0, fontSize:10, color:C.inkFaint }}>{desc}</p>
                </div>
                <span style={{ width:6, height:6, borderRadius:"50%", background:C.green, flexShrink:0, animation:"pulseRing 2s ease infinite" }}/>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}

// ─── INPUT TAB ────────────────────────────────────────────────────────────────
const UI_SAMPLE = [
  { trade_id:"T5001_PASS", trade_datetime:"2024-03-10T09:00:00Z", isin:"US0378331005", executing_entity_lei:"5493001KJTIIGC8Y1R12", buyer_lei:"213800D1EI4B9WTWWD28", seller_lei:"529900T8BM49AURSDO55", price:"180", currency:"USD", quantity:"30", venue:"XNAS", notional_amount:"5400", report_status:"NEWT", instrument_type:"EQUITY", source_channel:"ui" },
  { trade_id:"T5002_HITL", trade_datetime:"2024-03-10T10:00:00Z", isin:"US02079K3059", executing_entity_lei:"5493001KJTIIGC8Y1R12", buyer_lei:"213800D1EI4B9WTWWD28", seller_lei:"213800D1EI4B9WTWWD28", price:"150", currency:"USD", quantity:"70", venue:"XNAS", notional_amount:"10500", report_status:"NEWT", instrument_type:"EQUITY", source_channel:"ui" },
  { trade_id:"T5003_FAIL", trade_datetime:"", isin:"INVALID123", executing_entity_lei:"BAD_LEI", buyer_lei:"213800D1EI4B9WTWWD28", seller_lei:"529900T8BM49AURSDO55", price:"-50", currency:"XXX", quantity:"-10", venue:"UNKOWN", notional_amount:"500", report_status:"WRONG", instrument_type:"EQUITY", source_channel:"ui" },
];
const STEPS = ["Ingesting trade data…","Enriching ISIN & LEI references…","Running validation, risk & compliance in parallel…","Decision engine routing…","Generating compliance report…"];

const SOURCES = [
  { key:"ui",  label:"UI Input",         icon:Ic.Upload, color:C.blue,   description:"Paste JSON directly — manual trade entry from the analyst desk." },
  { key:"db",  label:"Trading System DB",icon:Ic.Layer,  color:C.green,  description:"Pre-loaded trades from the in-memory trading system database." },
  { key:"csv", label:"CSV File",          icon:Ic.Report, color:C.violet, description:"Trades read from a CSV file on disk (simulates upstream file drop)." },
];

function InputTab({ onComplete }) {
  const [activeSource, setActiveSource] = useState("ui");
  const [uiInput,   setUiInput]   = useState(JSON.stringify(UI_SAMPLE, null, 2));
  const [dbTrades,  setDbTrades]  = useState([]);
  const [csvTrades, setCsvTrades] = useState([]);
  const [selected,  setSelected]  = useState([]);
  const [loading,   setLoading]   = useState(false);
  const [running,   setRunning]   = useState(false);
  const [step,      setStep]      = useState(0);
  const [err,       setErr]       = useState(null);

  useEffect(()=>{ if(!running)return; const t=setInterval(()=>setStep(s=>(s+1)%STEPS.length),2400); return()=>clearInterval(t); },[running]);
  useEffect(()=>{ setSelected([]); setErr(null); if(activeSource==="db") loadDb(); if(activeSource==="csv") loadCsv(); },[activeSource]);

  const loadDb  = async()=>{ setLoading(true); try{ const r=await fetchDbTrades(); setDbTrades(r.data.trades||[]); }catch(e){ setErr("Failed to load DB: "+e.message); } finally{ setLoading(false); } };
  const loadCsv = async()=>{ setLoading(true); try{ const r=await fetchCsvTrades(); setCsvTrades(r.data.trades||[]); }catch(e){ setErr("Failed to load CSV: "+e.message); } finally{ setLoading(false); } };

  const toggleSelect = (id) => setSelected(p=>p.includes(id)?p.filter(x=>x!==id):[...p,id]);
  const toggleAll    = (trades) => { const ids=trades.map(t=>t.trade_id); const allSel=ids.every(id=>selected.includes(id)); setSelected(allSel?[]:[...ids]); };

  const buildTrades = () => {
    if(activeSource==="ui"){ const p=JSON.parse(uiInput); return (Array.isArray(p)?p:[p]).map(t=>({...t,source_channel:"ui"})); }
    const src = activeSource==="db" ? dbTrades : csvTrades;
    const toRun = selected.length ? src.filter(t=>selected.includes(t.trade_id)) : src;
    if(!toRun.length) throw new Error("No trades selected.");
    return toRun.map(t=>({...t,source_channel:activeSource==="db"?"in_memory_db":"csv_file"}));
  };

  const handleRun = async()=>{
    setErr(null); setRunning(true);
    try{ const trades=buildTrades(); const res=await runPipelineApi({ trades, source_channel:activeSource==="ui"?"ui":activeSource==="db"?"in_memory_db":"csv_file" }); onComplete(res.data); }
    catch(e){ setErr(e.response?.data?.detail||e.message); setRunning(false); }
    finally{ if(!err) setRunning(false); }
  };

  const displayTrades = activeSource==="db" ? dbTrades : activeSource==="csv" ? csvTrades : [];
  const currentSrc    = SOURCES.find(s=>s.key===activeSource);

  return (
    <div style={{ maxWidth:900, margin:"0 auto" }}>
      <SectionHeader title="Multi-Source Trade Input" sub="Select a data source, review the trades, then execute the agentic pipeline."/>

      {/* Source tabs */}
      <div style={{ display:"flex", gap:10, marginBottom:20 }}>
        {SOURCES.map(({ key, label, icon:Icon, color, description })=>{
          const active = activeSource===key;
          return (
            <button key={key} onClick={()=>setActiveSource(key)}
              style={{ flex:1, padding:"14px 16px", borderRadius:10, border:`2px solid ${active?color:C.border}`, background:active?color+"10":C.surface, cursor:"pointer", textAlign:"left", transition:"all .15s" }}>
              <div style={{ display:"flex", alignItems:"center", gap:8, marginBottom:6 }}>
                <div style={{ width:28,height:28,borderRadius:7,background:active?color:C.bg,display:"flex",alignItems:"center",justifyContent:"center",color:active?color:C.inkFaint }}>
                  <Icon style={{ width:14,height:14 }}/>
                </div>
                <span style={{ fontSize:13,fontWeight:700,color:active?color:C.inkMuted,fontFamily:FONT.display }}>{label}</span>
                {active&&<span style={{ marginLeft:"auto",fontSize:9,fontWeight:700,color,background:color+"15",padding:"2px 7px",borderRadius:4,fontFamily:FONT.mono }}>ACTIVE</span>}
              </div>
              <p style={{ margin:0,fontSize:11,color:C.inkMuted,lineHeight:1.5 }}>{description}</p>
            </button>
          );
        })}
      </div>

      {err&&<div style={{ padding:"11px 14px",background:C.redTint,border:`1px solid ${C.redBorder}`,borderRadius:8,marginBottom:14,display:"flex",gap:8 }}><Ic.Alert style={{ width:15,height:15,color:C.red,flexShrink:0 }}/><span style={{ fontSize:13,color:C.red }}>{err}</span></div>}

      {/* UI textarea */}
      {activeSource==="ui"&&(
        <Card noPad style={{ marginBottom:14 }}>
          <div style={{ padding:"10px 16px",borderBottom:`1px solid ${C.border}`,display:"flex",alignItems:"center",gap:10,background:C.surfaceAlt }}>
            <div style={{ display:"flex",gap:5 }}>{["#FF6058","#FFBD2E","#28CA41"].map(c=><span key={c} style={{ width:10,height:10,borderRadius:"50%",background:c,display:"block" }}/>)}</div>
            <span style={{ fontSize:11,color:C.inkFaint,fontFamily:FONT.mono }}>trade_payload.json</span>
            <span style={{ marginLeft:"auto",fontSize:11,color:C.inkFaint }}>{uiInput.split('\n').length} lines</span>
            <Btn variant="secondary" size="xs" icon={Ic.Copy} onClick={()=>setUiInput(JSON.stringify(UI_SAMPLE,null,2))}>Load Sample</Btn>
          </div>
          <textarea value={uiInput} onChange={e=>setUiInput(e.target.value)} spellCheck={false}
            style={{ width:"100%",minHeight:320,border:"none",padding:"16px 20px",fontSize:12.5,color:C.ink,fontFamily:FONT.mono,lineHeight:1.8,background:C.surfaceAlt,outline:"none",resize:"vertical",boxSizing:"border-box",display:"block" }}/>
        </Card>
      )}

      {/* DB / CSV trade table */}
      {activeSource!=="ui"&&(
        <Card noPad style={{ marginBottom:14 }}>
          <div style={{ padding:"12px 16px",borderBottom:`1px solid ${C.border}`,display:"flex",alignItems:"center",gap:12,background:C.surfaceAlt }}>
            <div>
              <p style={{ margin:0,fontSize:13,fontWeight:700,color:C.ink,fontFamily:FONT.display }}>{currentSrc?.label}</p>
              <p style={{ margin:"2px 0 0",fontSize:11,color:C.inkFaint }}>{loading?"Loading…":`${displayTrades.length} trades available`}{selected.length>0&&` · ${selected.length} selected`}</p>
            </div>
            <div style={{ marginLeft:"auto",display:"flex",gap:8 }}>
              <Btn variant="secondary" size="sm" icon={Ic.Refresh} onClick={activeSource==="db"?loadDb:loadCsv} disabled={loading}>{loading?"Loading…":"Refresh"}</Btn>
              {displayTrades.length>0&&<Btn variant="secondary" size="sm" onClick={()=>toggleAll(displayTrades)}>{displayTrades.every(t=>selected.includes(t.trade_id))?"Deselect All":"Select All"}</Btn>}
            </div>
          </div>
          {loading ? <div style={{ padding:40,display:"flex",justifyContent:"center" }}><Spinner size={24}/></div>
          : displayTrades.length===0 ? <Empty icon={Ic.Layer} title="No trades found" sub="The data source returned no records."/>
          : (
            <div style={{ overflowX:"auto" }}>
              <table style={{ width:"100%",borderCollapse:"collapse",fontSize:12 }}>
                <thead><tr style={{ background:C.surfaceAlt }}>
                  <th style={{ padding:"9px 14px",width:40 }}>
                    <input type="checkbox" checked={displayTrades.every(t=>selected.includes(t.trade_id))} onChange={()=>toggleAll(displayTrades)} style={{ cursor:"pointer",accentColor:currentSrc?.color }}/>
                  </th>
                  {["Trade ID","ISIN","Price","CCY","Qty","Venue","Status","Source"].map(h=>(
                    <th key={h} style={{ padding:"9px 14px",textAlign:"left",fontSize:10,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".07em",fontWeight:700,borderBottom:`1px solid ${C.border}`,whiteSpace:"nowrap" }}>{h}</th>
                  ))}
                </tr></thead>
                <tbody>
                  {displayTrades.map((t,i)=>{
                    const isSel=selected.includes(t.trade_id);
                    const srcColor=activeSource==="db"?C.green:C.violet;
                    return (
                      <tr key={t.trade_id} onClick={()=>toggleSelect(t.trade_id)} style={{ borderBottom:`1px solid ${C.border}`,background:isSel?srcColor+"08":i%2?C.surfaceAlt:C.surface,cursor:"pointer",transition:"background .1s" }}
                        onMouseEnter={e=>{if(!isSel)e.currentTarget.style.background=C.bg;}}
                        onMouseLeave={e=>{e.currentTarget.style.background=isSel?srcColor+"08":i%2?C.surfaceAlt:C.surface;}}>
                        <td style={{ padding:"10px 14px" }}><input type="checkbox" checked={isSel} onChange={()=>toggleSelect(t.trade_id)} onClick={e=>e.stopPropagation()} style={{ cursor:"pointer",accentColor:srcColor }}/></td>
                        <td style={{ padding:"10px 14px",fontFamily:FONT.mono,fontSize:11,color:srcColor,fontWeight:700 }}>{t.trade_id}</td>
                        <td style={{ padding:"10px 14px",fontSize:11,color:C.inkMuted,fontFamily:FONT.mono }}>{t.isin}</td>
                        <td style={{ padding:"10px 14px",fontFamily:FONT.mono }}>{t.price}</td>
                        <td style={{ padding:"10px 14px" }}>{t.currency}</td>
                        <td style={{ padding:"10px 14px" }}>{t.quantity}</td>
                        <td style={{ padding:"10px 14px",fontFamily:FONT.mono,fontSize:11 }}>{t.venue}</td>
                        <td style={{ padding:"10px 14px" }}><Badge status={t.report_status||"NEWT"} size="xs"/></td>
                        <td style={{ padding:"10px 14px" }}><span style={{ fontSize:10,fontWeight:700,color:srcColor,background:srcColor+"15",padding:"2px 7px",borderRadius:4,fontFamily:FONT.mono }}>{t._source_label||activeSource.toUpperCase()}</span></td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
          {displayTrades.length>0&&(
            <div style={{ padding:"10px 16px",borderTop:`1px solid ${C.border}`,background:C.surfaceAlt,display:"flex",alignItems:"center",gap:12 }}>
              <span style={{ fontSize:11,color:C.inkFaint }}>{selected.length===0?"No trades selected — all trades will run":`${selected.length} of ${displayTrades.length} selected`}</span>
              {selected.length>0&&<Btn variant="secondary" size="xs" onClick={()=>setSelected([])}>Clear selection</Btn>}
            </div>
          )}
        </Card>
      )}

      {/* Feature cards */}
      <div style={{ display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:12,marginBottom:16 }}>
        {[[Ic.Database,C.green,"In-Memory DB","Simulates overnight batch from core banking"],[Ic.Report,C.violet,"CSV File Source","Simulates upstream reporting file drop"],[Ic.Upload,C.blue,"Manual UI Entry","Direct analyst paste — any JSON format"]].map(([Icon,color,label,desc])=>(
          <div key={label} style={{ background:C.surface,borderRadius:10,padding:14,border:`1px solid ${C.border}`,borderTop:`3px solid ${color}` }}>
            <div style={{ width:30,height:30,borderRadius:8,background:color+"15",display:"flex",alignItems:"center",justifyContent:"center",marginBottom:8,color }}><Icon style={{ width:15,height:15 }}/></div>
            <p style={{ margin:"0 0 4px",fontSize:12,fontWeight:700,color:C.ink,fontFamily:FONT.display }}>{label}</p>
            <p style={{ margin:0,fontSize:11,color:C.inkMuted,lineHeight:1.5 }}>{desc}</p>
          </div>
        ))}
      </div>

      {/* Run button */}
      <button onClick={running?undefined:handleRun} disabled={running}
        style={{ width:"100%",padding:"13px",background:running?C.bg:`linear-gradient(135deg,${C.blue} 0%,${C.blueDark} 100%)`,color:running?C.inkMuted:"#fff",border:running?`1px solid ${C.border}`:"none",borderRadius:10,fontSize:14,fontWeight:700,cursor:running?"not-allowed":"pointer",display:"flex",alignItems:"center",justifyContent:"center",gap:10,transition:"all .2s",fontFamily:FONT.display,boxShadow:running?"none":"0 4px 14px rgba(0,86,197,.3)" }}>
        {running?<><Spinner size={16} color={C.blue}/><span style={{ color:C.inkMid }}>{STEPS[step]}</span></>:<><Ic.Zap style={{ width:17,height:17 }}/>Execute Agentic Pipeline</>}
      </button>
    </div>
  );
}

// ─── MERGE TAB ────────────────────────────────────────────────────────────────
function MergeTab({ onComplete }) {
  const [loading,      setLoading]      = useState(false);
  const [running,      setRunning]      = useState(false);
  const [err,          setErr]          = useState(null);
  const [sourceFilter, setSourceFilter] = useState("all");
  const [allTrades,    setAllTrades]    = useState([]);
  const [selected,     setSelected]     = useState(new Set());
  const [mergedJson,   setMergedJson]   = useState("");

  const loadAll = useCallback(async()=>{ setLoading(true); setErr(null); try{ const r=await fetchAllTrades(); const t=r.data?.trades||[]; setAllTrades(t); setMergedJson(JSON.stringify(t,null,2)); }catch(e){ setErr(e.response?.data?.detail||e.message||"Failed to load trades"); } finally{ setLoading(false); } },[]);
  useEffect(()=>{ loadAll(); },[loadAll]);

  const filtered = sourceFilter==="all" ? allTrades : allTrades.filter(t=>(t.source_channel||"")===sourceFilter);
  const toggleOne = (id) => setSelected(p=>{ const n=new Set(p); n.has(id)?n.delete(id):n.add(id); return n; });
  const toggleAll = () => { const ids=filtered.map(t=>t.trade_id); const allSel=ids.length>0&&ids.every(id=>selected.has(id)); setSelected(p=>{ const n=new Set(p); allSel?ids.forEach(id=>n.delete(id)):ids.forEach(id=>n.add(id)); return n; }); };
  const loadToJson = () => { const t=selected.size>0?filtered.filter(t=>selected.has(t.trade_id)):filtered; setMergedJson(JSON.stringify(t,null,2)); };

  const run = async()=>{
    setRunning(true); setErr(null);
    try{
      let trades = selected.size>0 ? filtered.filter(t=>selected.has(t.trade_id)) : JSON.parse(mergedJson||"[]");
      if(!trades.length) throw new Error("No trades to run.");
      const res=await runPipelineApi({ trades, source_channel:"merged" });
      onComplete(res.data);
    }catch(e){ setErr(e.response?.data?.detail||e.message); }
    finally{ setRunning(false); }
  };

  return (
    <div style={{ maxWidth:1150, margin:"0 auto" }}>
      <SectionHeader title="Merge Trade Sources" sub="Load trades from all sources into one view, filter by channel, then run the pipeline."
        actions={<><Btn variant="secondary" size="sm" icon={Ic.Refresh} onClick={loadAll} disabled={loading}>{loading?"Loading…":"Refresh"}</Btn><Btn variant="secondary" size="sm" icon={Ic.Copy} onClick={loadToJson} disabled={!filtered.length}>Load Selected into JSON</Btn><Btn variant="primary" size="sm" icon={Ic.Zap} onClick={run} disabled={running}>{running?"Running…":"Run Pipeline"}</Btn></>}/>

      <div style={{ display:"flex",gap:8,marginBottom:14,flexWrap:"wrap" }}>
        {[{key:"all",label:"All Sources"},{key:"in_memory_db",label:"Trading DB"},{key:"csv_file",label:"CSV File"}].map(item=>(
          <Btn key={item.key} variant={sourceFilter===item.key?"primary":"secondary"} size="sm" onClick={()=>setSourceFilter(item.key)}>{item.label}</Btn>
        ))}
      </div>

      {err&&<div style={{ padding:"11px 14px",background:C.redTint,border:`1px solid ${C.redBorder}`,borderRadius:8,marginBottom:14,display:"flex",gap:8,color:C.red,fontSize:13 }}><Ic.Alert style={{ width:15,height:15,color:C.red,flexShrink:0 }}/><span>{err}</span></div>}

      <Card noPad style={{ marginBottom:14 }}>
        <div style={{ padding:"12px 16px",borderBottom:`1px solid ${C.border}`,display:"flex",justifyContent:"space-between",alignItems:"center",background:C.surfaceAlt }}>
          <div>
            <p style={{ margin:0,fontSize:13,fontWeight:700,color:C.ink,fontFamily:FONT.display }}>Merged Trades</p>
            <p style={{ margin:"2px 0 0",fontSize:11,color:C.inkFaint }}>Showing {filtered.length} of {allTrades.length} · Selected {selected.size}</p>
          </div>
          <div style={{ display:"flex",gap:8 }}>
            <Btn variant="secondary" size="xs" onClick={toggleAll} disabled={!filtered.length}>{filtered.every(t=>selected.has(t.trade_id))&&filtered.length>0?"Deselect All":"Select All"}</Btn>
            <Btn variant="secondary" size="xs" onClick={()=>setSelected(new Set())}>Clear</Btn>
          </div>
        </div>
        {loading ? <div style={{ padding:40,display:"flex",justifyContent:"center" }}><Spinner size={24}/></div>
        : (
          <div style={{ overflowX:"auto" }}>
            <table style={{ width:"100%",borderCollapse:"collapse",fontSize:12 }}>
              <thead><tr style={{ background:C.surfaceAlt }}>
                <th style={{ padding:"10px 14px",width:44 }}><input type="checkbox" checked={filtered.length>0&&filtered.every(t=>selected.has(t.trade_id))} onChange={toggleAll} style={{ accentColor:C.blue,cursor:"pointer" }}/></th>
                {["Trade ID","Source","ISIN","Price","CCY","Qty","Venue","Status"].map(h=><th key={h} style={{ padding:"10px 14px",textAlign:"left",fontSize:10,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".07em",fontWeight:700,borderBottom:`1px solid ${C.border}`,whiteSpace:"nowrap" }}>{h}</th>)}
              </tr></thead>
              <tbody>
                {filtered.map((t,i)=>{
                  const isSel=selected.has(t.trade_id);
                  const src=t.source_channel||"merged";
                  const srcColor=src==="in_memory_db"?C.green:src==="csv_file"?C.violet:C.blue;
                  return (
                    <tr key={`${src}-${t.trade_id}-${i}`} onClick={()=>toggleOne(t.trade_id)} style={{ borderBottom:`1px solid ${C.border}`,background:isSel?srcColor+"08":i%2?C.surfaceAlt:C.surface,cursor:"pointer" }}>
                      <td style={{ padding:"10px 14px" }}><input type="checkbox" checked={isSel} onChange={()=>toggleOne(t.trade_id)} onClick={e=>e.stopPropagation()} style={{ cursor:"pointer",accentColor:srcColor }}/></td>
                      <td style={{ padding:"10px 14px",fontFamily:FONT.mono,fontSize:11,color:srcColor,fontWeight:700 }}>{t.trade_id}</td>
                      <td style={{ padding:"10px 14px",fontSize:11 }}><span style={{ fontSize:10,fontWeight:700,color:srcColor,background:srcColor+"15",padding:"2px 7px",borderRadius:4,fontFamily:FONT.mono }}>{t._source_label||src}</span></td>
                      <td style={{ padding:"10px 14px" }}>{t.isin}</td>
                      <td style={{ padding:"10px 14px" }}>{t.price}</td>
                      <td style={{ padding:"10px 14px" }}>{t.currency}</td>
                      <td style={{ padding:"10px 14px" }}>{t.quantity}</td>
                      <td style={{ padding:"10px 14px",fontFamily:FONT.mono,fontSize:11 }}>{t.venue}</td>
                      <td style={{ padding:"10px 14px" }}><Badge status={t.report_status||"NEWT"} size="xs"/></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <Card noPad>
        <div style={{ padding:"12px 16px",borderBottom:`1px solid ${C.border}`,display:"flex",justifyContent:"space-between",alignItems:"center",background:C.surfaceAlt }}>
          <div><p style={{ margin:0,fontSize:13,fontWeight:700,color:C.ink,fontFamily:FONT.display }}>Merged JSON Payload</p><p style={{ margin:"2px 0 0",fontSize:11,color:C.inkFaint }}>Sent to pipeline on Run. Edit manually if needed.</p></div>
          <Btn variant="secondary" size="xs" icon={Ic.Copy} onClick={loadToJson}>Load Selected / All</Btn>
        </div>
        <textarea value={mergedJson} onChange={e=>setMergedJson(e.target.value)} spellCheck={false}
          style={{ width:"100%",minHeight:240,border:"none",padding:"16px 20px",fontSize:12.5,color:C.ink,fontFamily:FONT.mono,lineHeight:1.8,background:C.surfaceAlt,outline:"none",resize:"vertical",boxSizing:"border-box",display:"block" }}/>
      </Card>
    </div>
  );
}

// ─── DASHBOARD ────────────────────────────────────────────────────────────────
function DashboardTab({ data }) {
  if(!data) return <Empty icon={Ic.Home} title="No pipeline run yet" sub="Navigate to Input or use Audit Chat to execute your first trade batch."/>;
  const { stats={}, final_trades=[], agent_log=[], risk_results=[] } = data;
  const hitlCount = data.hitl_queue?.length || final_trades.filter(t=>t.final_status==="HITL").length;
  const autoFixed = stats.auto_fixed || data.corrections?.length || 0;
  const failCount = final_trades.filter(t=>t.final_status==="FAIL").length;
  const sourceSummary = {};
  final_trades.forEach(t=>{ const s=t.source_channel||"ui"; sourceSummary[s]=(sourceSummary[s]||0)+1; });
  const logRef = useRef(null);
  useEffect(()=>{ if(logRef.current) logRef.current.scrollTop=logRef.current.scrollHeight; },[agent_log]);
  const acol = l => l.includes("Ingestion")?C.blue:l.includes("Enrichment")?C.violet:l.includes("Validation")?C.green:l.includes("Risk")?C.amber:l.includes("Compliance")?"#DB2777":l.includes("Decision")?C.blue:l.includes("Report")?C.cyan:C.inkFaint;

  return (
    <div>
      <SectionHeader title="Operations Center" sub="Real-time agentic pipeline results & trade analytics." actions={<Pill label={`PIPELINE COMPLETE — ${data.run_id}`} color={C.green}/>}/>
      <div style={{ display:"grid",gridTemplateColumns:"repeat(5,1fr)",gap:12,marginBottom:20 }}>
        <StatCard label="Total Trades"   value={stats.total||0}    accent={C.blue}   icon={Ic.Layer}/>
        <StatCard label="Passed"         value={stats.passed||0}   accent={C.green}  icon={Ic.Check}/>
        <StatCard label="HITL Required"  value={hitlCount}         accent={C.amber}  icon={Ic.Users}/>
        <StatCard label="Failed"         value={failCount}         accent={C.red}    icon={Ic.Alert}/>
        <StatCard label="Auto-Corrected" value={autoFixed}         accent={C.violet} icon={Ic.Wand}/>
      </div>
      {Object.keys(sourceSummary).length>0&&(
        <div style={{ marginBottom:14,display:"flex",gap:10,flexWrap:"wrap" }}>
          {Object.entries(sourceSummary).map(([k,v])=>(
            <span key={k} style={{ padding:"5px 10px",background:C.blueTint,border:`1px solid ${C.border}`,borderRadius:6,fontSize:11,fontWeight:700,fontFamily:FONT.mono }}>{k.toUpperCase()}: {v}</span>
          ))}
        </div>
      )}
      <div style={{ display:"grid",gridTemplateColumns:"1fr 340px",gap:14,marginBottom:14 }}>
        <Card noPad>
          <CardHeader title="Final Trade Decisions" right={<span style={{ fontSize:11,color:C.inkFaint }}>{final_trades.length} records</span>}/>
          <div style={{ overflowX:"auto" }}>
            <table style={{ width:"100%",borderCollapse:"collapse",fontSize:12 }}>
              <thead><tr style={{ background:C.surfaceAlt }}>
                {["Trade ID","Source","ISIN","Qty","CCY","Price","Auto Fix","Status","Confidence"].map(h=>(
                  <th key={h} style={{ padding:"9px 14px",textAlign:"left",fontSize:10,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".07em",fontWeight:700,whiteSpace:"nowrap",borderBottom:`1px solid ${C.border}` }}>{h}</th>
                ))}
              </tr></thead>
              <tbody>
                {final_trades.map((t,i)=>{
                  const isFail=t.final_status==="FAIL";
                  const bg=isFail?C.redTint+"60":i%2?C.surfaceAlt:C.surface;
                  return (
                    <tr key={t.trade_id} style={{ background:bg,borderBottom:`1px solid ${C.border}`,transition:"background .1s",...(isFail&&{borderLeft:`3px solid ${C.red}`})}}
                      onMouseEnter={e=>e.currentTarget.style.background=isFail?C.redTint:C.blueTint+"40"}
                      onMouseLeave={e=>e.currentTarget.style.background=bg}>
                      <td style={{ padding:"10px 14px",fontFamily:FONT.mono,fontSize:11,color:isFail?C.red:C.blue,fontWeight:700 }}>{t._original_trade_id||t.trade_id}</td>
                      <td style={{ padding:"10px 14px",fontSize:11,color:C.inkMuted,fontFamily:FONT.mono }}>{t.source_channel||"ui"}</td>
                      <td style={{ padding:"10px 14px",fontSize:11,color:C.inkMuted,fontFamily:FONT.mono }}>{t.isin}</td>
                      <td style={{ padding:"10px 14px",fontSize:12 }}>{t.quantity}</td>
                      <td style={{ padding:"10px 14px",fontSize:12 }}>{t.currency}</td>
                      <td style={{ padding:"10px 14px",fontSize:12,fontFamily:FONT.mono }}>{parseFloat(t.price||0).toLocaleString()}</td>
                      <td style={{ padding:"10px 14px" }}><Badge status={t.auto_fix_applied?"APPLIED":"NONE"} size="xs"/></td>
                      <td style={{ padding:"10px 14px" }}><Badge status={t.final_status}/></td>
                      <td style={{ padding:"10px 14px",minWidth:130 }}><ConfBar value={t.decision_confidence} status={t.final_status} compact/></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
        <Card noPad style={{ display:"flex",flexDirection:"column",maxHeight:420 }}>
          <CardHeader title="Agent Execution Log" sub={`${agent_log.length} events`}
            right={<span style={{ display:"inline-flex",gap:5,alignItems:"center" }}><span style={{ width:7,height:7,borderRadius:"50%",background:C.green,boxShadow:`0 0 5px ${C.green}` }}/><span style={{ fontSize:10,color:C.green,fontWeight:700,fontFamily:FONT.mono }}>LIVE</span></span>}/>
          <div ref={logRef} style={{ flex:1,overflowY:"auto",padding:"10px 14px" }}>
            {agent_log.map((log,i)=>(
              <div key={i} style={{ display:"flex",gap:8,padding:"2.5px 0",fontSize:11,lineHeight:1.6,alignItems:"flex-start" }}>
                <span style={{ color:C.border,fontFamily:FONT.mono,minWidth:20,paddingTop:1 }}>{String(i+1).padStart(2,"0")}</span>
                <span style={{ color:acol(log),fontFamily:FONT.mono,flex:1 }}>{log}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>
      {failCount>0&&(
        <Card noPad style={{ marginBottom:14,borderLeft:`3px solid ${C.red}` }}>
          <CardHeader title="Failed Trades" sub={`${failCount} trade${failCount!==1?"s":""} rejected by the validation pipeline`} right={<Badge status="FAIL"/>}/>
          <div style={{ padding:"14px 18px",display:"flex",flexDirection:"column",gap:10 }}>
            {final_trades.filter(t=>t.final_status==="FAIL").map(t=>(
              <div key={t.trade_id} style={{ display:"flex",gap:14,alignItems:"flex-start",padding:"13px 15px",background:C.redTint,border:`1px solid ${C.redBorder}`,borderRadius:10,borderLeft:`3px solid ${C.red}` }}>
                <div style={{ width:32,height:32,borderRadius:8,background:C.red+"20",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0,color:C.red }}><Ic.Alert style={{ width:15,height:15 }}/></div>
                <div style={{ flex:1,minWidth:0 }}>
                  <div style={{ display:"flex",gap:8,alignItems:"center",marginBottom:6,flexWrap:"wrap" }}>
                    <Badge status="FAIL" size="xs"/>
                    <span style={{ fontFamily:FONT.mono,fontSize:12,color:C.red,fontWeight:700 }}>{t._original_trade_id||t.trade_id}</span>
                    {t.isin&&<span style={{ fontSize:11,color:C.inkMuted }}>ISIN: {t.isin}</span>}
                  </div>
                  {t.decision_reason&&<p style={{ margin:0,fontSize:12,color:C.inkMid,lineHeight:1.6 }}>{t.decision_reason}</p>}
                  <div style={{ marginTop:8,display:"flex",gap:8,alignItems:"center" }}>
                    <span style={{ fontSize:10,color:C.inkFaint,fontWeight:700,textTransform:"uppercase",letterSpacing:".07em" }}>Confidence</span>
                    <div style={{ width:100 }}><ConfBar value={t.decision_confidence} status="FAIL" compact/></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
      {risk_results.length>0&&(
        <Card style={{ padding:16 }}>
          <p style={{ margin:"0 0 12px",fontSize:13,fontWeight:700,color:C.ink,fontFamily:FONT.display }}>Risk Distribution</p>
          <div style={{ display:"flex",gap:10,flexWrap:"wrap" }}>
            {risk_results.map(r=>(
              <div key={r.trade_id} style={{ flex:"1 1 180px",padding:"11px 14px",background:C.surfaceAlt,borderRadius:9,border:`1px solid ${C.border}`,borderLeft:`3px solid ${r.risk_level==="HIGH"?C.red:r.risk_level==="MEDIUM"?C.amber:C.green}` }}>
                <div style={{ display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:7 }}>
                  <span style={{ fontSize:11,color:C.inkMuted,fontFamily:FONT.mono,fontWeight:600 }}>{(r.trade_id||"").split("-").slice(-1)[0]}</span>
                  <Badge status={r.risk_level||"LOW"} size="xs"/>
                </div>
                <ConfBar value={r.confidence} status={r.risk_level} compact/>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

// ─── VALIDATION ───────────────────────────────────────────────────────────────
function ValidationTab({ results=[], complianceResults=[] }) {
  if(!results.length) return <Empty icon={Ic.Shield} title="No validation data" sub="Run a pipeline to see field-level validation results."/>;
  return (
    <div>
      <SectionHeader title="Validation Results" sub="MiFID II field-level validation with RAG-augmented rule retrieval and deterministic safety net."/>
      <div style={{ display:"flex",flexDirection:"column",gap:10 }}>
        {results.map(r=>{
          const comp=complianceResults.find(c=>c.trade_id===r.trade_id)||{};
          return (
            <Card key={r.trade_id} noPad style={{ borderLeft:`3px solid ${r.passed?C.green:C.red}` }}>
              <div style={{ padding:"13px 18px",display:"flex",justifyContent:"space-between",alignItems:"center",gap:12 }}>
                <div style={{ display:"flex",gap:10,alignItems:"center",flexWrap:"wrap" }}>
                  <span style={{ fontFamily:FONT.mono,fontSize:12,color:C.blue,fontWeight:700 }}>{r.trade_id}</span>
                  <Badge status={r.passed?"PASS":"false"}/>
                  {comp.compliant!==undefined&&<Badge status={comp.compliant?"true":"false"}/>}
                </div>
                <div style={{ display:"flex",gap:14,alignItems:"center",flexShrink:0 }}>
                  <div style={{ textAlign:"right" }}><p style={{ margin:"0 0 4px",fontSize:9,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".07em",fontWeight:700 }}>Confidence</p><div style={{ width:110 }}><ConfBar value={r.confidence} status={r.passed?"PASS":"FAIL"} compact/></div></div>
                  <div style={{ textAlign:"right" }}><p style={{ margin:"0 0 2px",fontSize:9,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".07em",fontWeight:700 }}>RAG</p><span style={{ fontSize:13,fontWeight:800,color:C.ink,fontFamily:FONT.mono }}>{Math.round((r.rag_confidence||0)*100)}%</span></div>
                </div>
              </div>
              {r.summary&&<div style={{ padding:"8px 18px",background:C.surfaceAlt,borderTop:`1px solid ${C.border}` }}><p style={{ margin:0,fontSize:12,color:C.inkMuted,lineHeight:1.6 }}>{r.summary}</p></div>}
              {r.issues?.length>0&&(
                <div style={{ borderTop:`1px solid ${C.border}` }}>
                  <table style={{ width:"100%",borderCollapse:"collapse" }}>
                    <thead><tr style={{ background:C.surfaceAlt }}>
                      <th style={{ padding:"7px 18px",textAlign:"left",fontSize:10,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".07em",fontWeight:700 }}>Field</th>
                      <th style={{ padding:"7px 18px",textAlign:"left",fontSize:10,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".07em",fontWeight:700 }}>Error</th>
                      <th style={{ padding:"7px 18px",textAlign:"right",fontSize:10,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".07em",fontWeight:700 }}>Severity</th>
                    </tr></thead>
                    <tbody>{r.issues.map((iss,i)=>(
                      <tr key={i} style={{ borderTop:`1px solid ${C.border}` }}>
                        <td style={{ padding:"9px 18px",fontSize:12,fontFamily:FONT.mono,color:C.ink,fontWeight:700,minWidth:160 }}>{iss.field}</td>
                        <td style={{ padding:"9px 18px",fontSize:12,color:C.inkMuted,lineHeight:1.5 }}>{iss.error}</td>
                        <td style={{ padding:"9px 18px",textAlign:"right" }}><Badge status={iss.severity} size="xs"/></td>
                      </tr>
                    ))}</tbody>
                  </table>
                </div>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
}

// ─── RISK ─────────────────────────────────────────────────────────────────────
function RiskTab({ results=[] }) {
  if(!results.length) return <Empty icon={Ic.Alert} title="No risk data" sub="Run a pipeline to see risk assessment results."/>;
  return (
    <div>
      <SectionHeader title="Risk Assessment" sub="AI-driven risk scoring with deterministic baseline across 9 risk drivers."/>
      <div style={{ display:"flex",flexDirection:"column",gap:10 }}>
        {results.map(r=>(
          <Card key={r.trade_id} noPad style={{ borderLeft:`3px solid ${r.risk_level==="HIGH"?C.red:r.risk_level==="MEDIUM"?C.amber:C.green}` }}>
            <div style={{ padding:"13px 18px",display:"flex",justifyContent:"space-between",alignItems:"center" }}>
              <div style={{ display:"flex",gap:10,alignItems:"center" }}>
                <span style={{ fontFamily:FONT.mono,fontSize:12,color:C.blue,fontWeight:700 }}>{r.trade_id}</span>
                <Badge status={r.risk_level||"LOW"}/>
              </div>
              <div style={{ width:150 }}><ConfBar value={r.confidence} status={r.risk_level} compact/></div>
            </div>
            {r.summary&&<div style={{ padding:"0 18px 12px" }}><p style={{ margin:0,fontSize:12,color:C.inkMuted,lineHeight:1.6 }}>{r.summary}</p></div>}
            {r.drivers?.length>0&&(
              <div style={{ padding:"10px 18px 14px",borderTop:`1px solid ${C.border}`,display:"flex",flexDirection:"column",gap:6 }}>
                {r.drivers.map((d,i)=>(
                  <div key={i} style={{ display:"flex",gap:10,padding:"8px 12px",background:C.blueTint,borderRadius:7,borderLeft:`2px solid ${C.blue}` }}>
                    <Ic.Info style={{ width:13,height:13,color:C.blue,flexShrink:0,marginTop:1 }}/>
                    <p style={{ margin:0,fontSize:12,color:C.inkMid,lineHeight:1.5 }}>{typeof d==="object"?`[${d.rule_id}] ${d.description||"—"}`:d}</p>
                  </div>
                ))}
              </div>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
}

// ─── HITL ─────────────────────────────────────────────────────────────────────
function HITLTab({ data, runId, onDecision }) {
  const [decisions,setDec] = useState({});
  const [modTrade,setMod]  = useState(null);
  const [busy,setBusy]     = useState({});
  const [selected,setSel]  = useState(new Set());
  const [bulkBusy,setBB]   = useState(false);
  const [errs,setErrs]     = useState({});
  const [liveItems,setLive]= useState([]);
  const [refreshing,setRef]= useState(false);
  const validations = data?.validation_results||[];
  const refresh = useCallback(async()=>{ if(!runId)return; setRef(true); try{ const r=await getHitlQueue(runId); setLive(Array.isArray(r.data?.items)?r.data.items:[]); }catch{} finally{setRef(false);} },[runId]);
  useEffect(()=>{ refresh(); const t=setInterval(refresh,8000); return()=>clearInterval(t); },[refresh]);

  const hitlTrades=(()=>{
    const src=liveItems.length?liveItems:(data?.hitl_queue||[]);
    if(src.length) return src.map(h=>({...(h.trade||{}),trade_id:h.trade_id||h?.trade?.trade_id,decision_reason:h.reason,decision_confidence:h.confidence,_meta:h}));
    return (data?.final_trades||[]).filter(t=>t.final_status==="HITL");
  })();

  const decide=async(trade,dec)=>{ setBusy(b=>({...b,[trade.trade_id]:true})); setErrs(e=>({...e,[trade.trade_id]:null})); try{ const res=await submitHitlDecision({run_id:runId,trade_id:trade.trade_id,decision:dec,reviewer_note:""}); setDec(d=>({...d,[trade.trade_id]:{dec,result:res.data}})); setLive(p=>p.filter(x=>(x.trade_id||x?.trade?.trade_id)!==trade.trade_id)); onDecision(trade.trade_id,dec,res.data); }catch(e){ setErrs(er=>({...er,[trade.trade_id]:e.response?.data?.detail||e.message})); } finally{setBusy(b=>({...b,[trade.trade_id]:false}));} };
  const bulk=async(dec)=>{ if(!selected.size)return; setBB(true); try{ await submitBulkHitl({run_id:runId,trade_ids:[...selected],decision:dec}); selected.forEach(id=>setDec(d=>({...d,[id]:{dec}}))); setSel(new Set()); refresh(); }catch(e){alert("Bulk failed: "+e.message);} finally{setBB(false);} };
  const modSuccess=(result,id)=>{ setDec(d=>({...d,[id]:{dec:"MODIFIED",result}})); setMod(null); refresh(); onDecision(id,"MODIFIED",result); };

  if(!hitlTrades.length) return <div><SectionHeader title="Human-In-The-Loop Review" sub="Manual validation queue."/><Empty icon={Ic.Users} title="No trades pending review" sub="All trades were auto-processed. Run a new batch to populate the HITL queue."/></div>;
  const pending=hitlTrades.filter(t=>!decisions[t.trade_id]);
  const resolved=hitlTrades.filter(t=>!!decisions[t.trade_id]);

  return (
    <div>
      <SectionHeader title="Human-In-The-Loop Review" sub={`${pending.length} trade${pending.length!==1?"s":""} require manual validation.`}
        actions={<><Btn variant="secondary" size="sm" icon={Ic.Refresh} onClick={refresh} disabled={refreshing} loading={refreshing}>{refreshing?"Refreshing…":"Refresh"}</Btn>{selected.size>0&&<><Btn variant="success" size="sm" icon={Ic.Check} onClick={()=>bulk("APPROVED")} disabled={bulkBusy}>Approve {selected.size}</Btn><Btn variant="danger" size="sm" icon={Ic.X} onClick={()=>bulk("REJECTED")} disabled={bulkBusy}>Reject {selected.size}</Btn></>}</>}/>
      <div style={{ display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:12,marginBottom:20 }}>
        <StatCard label="Pending Review" value={pending.length}  accent={C.amber} icon={Ic.Users}/>
        <StatCard label="Resolved"       value={resolved.length} accent={C.green} icon={Ic.Check}/>
        <StatCard label="Total HITL"     value={hitlTrades.length} accent={C.blue} icon={Ic.Layer}/>
      </div>
      <div style={{ display:"flex",flexDirection:"column",gap:14 }}>
        {hitlTrades.map(trade=>{
          const dec=decisions[trade.trade_id]; const val=validations.find(v=>v.trade_id===trade.trade_id)||{};
          const isBusy=!!busy[trade.trade_id]; const isSel=selected.has(trade.trade_id); const err=errs[trade.trade_id];
          const bc=dec?dec.dec==="APPROVED"?C.greenBorder:dec.dec==="REJECTED"?C.redBorder:"rgba(0,86,197,.25)":C.border;
          return (
            <div key={trade.trade_id} style={{ background:C.surface,borderRadius:12,border:`1px solid ${bc}`,boxShadow:"0 2px 12px rgba(15,23,42,.06)",overflow:"hidden",transition:"border-color .25s" }}>
              <div style={{ padding:"13px 18px",borderBottom:`1px solid ${C.border}`,display:"flex",alignItems:"center",gap:10,background:dec?(dec.dec==="APPROVED"?C.greenTint:dec.dec==="REJECTED"?C.redTint:C.blueTint)+"80":C.surfaceAlt }}>
                {!dec&&<input type="checkbox" checked={isSel} onChange={e=>setSel(s=>{const n=new Set(s);e.target.checked?n.add(trade.trade_id):n.delete(trade.trade_id);return n;})} style={{ width:15,height:15,cursor:"pointer",flexShrink:0,accentColor:C.blue }}/>}
                <div style={{ flex:1,minWidth:0 }}>
                  <div style={{ display:"flex",gap:8,alignItems:"center",flexWrap:"wrap" }}>
                    <span style={{ fontFamily:FONT.mono,fontSize:13,fontWeight:700,color:C.blue }}>{trade.trade_id}</span>
                    {trade.isin&&<span style={{ fontSize:11,color:C.inkMuted }}>{trade.isin}</span>}
                    {trade.currency&&<><span style={{ color:C.border }}>·</span><span style={{ fontSize:11,color:C.inkMuted }}>{trade.currency} {parseFloat(trade.price||0).toLocaleString()}</span></>}
                    {trade.quantity&&<><span style={{ color:C.border }}>·</span><span style={{ fontSize:11,color:C.inkMuted }}>Qty {trade.quantity}</span></>}
                  </div>
                </div>
                <Badge status={dec?dec.dec:"HITL"} pulse={!dec}/>
              </div>
              <div style={{ padding:"14px 18px",display:"grid",gridTemplateColumns:"1fr 1fr",gap:16 }}>
                <div>
                  <p style={{ margin:"0 0 7px",fontSize:9,fontWeight:700,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".09em" }}>AI Decision Reasoning</p>
                  <div style={{ padding:"10px 13px",background:C.blueTint,borderRadius:8,borderLeft:`3px solid ${C.blue}` }}>
                    <p style={{ margin:0,fontSize:12,color:C.inkMid,lineHeight:1.7 }}>{trade.decision_reason||"No reasoning provided."}</p>
                  </div>
                </div>
                <div>
                  <p style={{ margin:"0 0 7px",fontSize:9,fontWeight:700,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".09em" }}>Validation Issues ({val.issues?.length||0})</p>
                  <div style={{ display:"flex",flexDirection:"column",gap:4,maxHeight:150,overflowY:"auto" }}>
                    {!(val.issues?.length)?<p style={{ fontSize:12,color:C.inkFaint,fontStyle:"italic" }}>No validation issues recorded.</p>
                    :val.issues.map((iss,i)=>(
                      <div key={i} style={{ display:"flex",justifyContent:"space-between",alignItems:"flex-start",padding:"6px 9px",background:C.surfaceAlt,borderRadius:6,gap:8,border:`1px solid ${C.border}` }}>
                        <span style={{ fontSize:11,fontFamily:FONT.mono,color:C.ink,fontWeight:700,flexShrink:0 }}>{iss.field}</span>
                        <span style={{ fontSize:11,color:C.inkMuted,flex:1,textAlign:"right",lineHeight:1.4 }}>{iss.error}</span>
                        <Badge status={iss.severity} size="xs"/>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              {err&&<div style={{ margin:"0 18px 10px",padding:"9px 12px",background:C.redTint,border:`1px solid ${C.redBorder}`,borderRadius:7,fontSize:12,color:C.red,display:"flex",gap:7 }}><Ic.Alert style={{ width:13,height:13,flexShrink:0 }}/>{err}</div>}
              {!dec&&(
                <div style={{ padding:"12px 18px",borderTop:`1px solid ${C.border}`,display:"flex",gap:8,alignItems:"center",background:C.surfaceAlt }}>
                  <Btn variant="success" icon={isBusy?null:Ic.Check} onClick={()=>decide(trade,"APPROVED")} disabled={isBusy} loading={isBusy}>{isBusy?"Processing…":"Approve"}</Btn>
                  <Btn variant="danger" icon={Ic.X} onClick={()=>decide(trade,"REJECTED")} disabled={isBusy}>Reject</Btn>
                  <Btn variant="amber" icon={Ic.Edit} onClick={()=>setMod(trade)} disabled={isBusy}>Modify & Re-run</Btn>
                  <div style={{ flex:1 }}/>
                  <div style={{ textAlign:"right" }}>
                    <p style={{ margin:0,fontSize:9,color:C.inkFaint,textTransform:"uppercase",letterSpacing:".08em",fontWeight:700 }}>Confidence</p>
                    <span style={{ fontSize:14,fontWeight:800,color:C.ink,fontFamily:FONT.mono }}>{Math.round((trade.decision_confidence||0)*100)}%</span>
                  </div>
                </div>
              )}
              {dec&&(
                <div style={{ padding:"11px 18px",borderTop:`1px solid ${C.border}`,display:"flex",gap:8,alignItems:"center",background:dec.dec==="APPROVED"?C.greenTint:dec.dec==="REJECTED"?C.redTint:C.blueTint }}>
                  {dec.dec==="APPROVED"?<Ic.Check style={{ width:15,height:15,color:C.green }}/>:dec.dec==="REJECTED"?<Ic.X style={{ width:15,height:15,color:C.red }}/>:<Ic.Edit style={{ width:15,height:15,color:C.blue }}/>}
                  <span style={{ fontSize:12,fontWeight:700,color:dec.dec==="APPROVED"?C.green:dec.dec==="REJECTED"?C.red:C.blue }}>
                    {dec.dec==="APPROVED"?"Trade approved — will appear as PASS in final report":dec.dec==="REJECTED"?"Trade rejected — moved to exceptions report":"Trade modified and reprocessed through full pipeline"}
                  </span>
                  {dec.result?.new_status&&<Badge status={dec.result.new_status}/>}
                </div>
              )}
            </div>
          );
        })}
      </div>
      {modTrade&&<ModifyModal trade={modTrade} runId={runId} onClose={()=>setMod(null)} onSuccess={r=>modSuccess(r,modTrade.trade_id)}/>}
    </div>
  );
}

// ─── AUDIT LOG ────────────────────────────────────────────────────────────────
function AuditTab({ runId }) {
  const [logs,setLogs]   = useState([]);
  const [loading,setLoad]= useState(false);
  const [err,setErr]     = useState(null);
  useEffect(()=>{ if(!runId)return; setLoad(true); setErr(null); getAuditLog(runId).then(r=>{setLogs(r.data.entries||[]);setLoad(false);}).catch(e=>{setErr(e.message);setLoad(false);}); },[runId]);
  if(!runId) return <Empty icon={Ic.Audit} title="No run selected" sub="Run a pipeline to generate the immutable audit trail."/>;
  const acol=a=>a?.includes("APPROVED")||a?.includes("PASS")?C.green:a?.includes("REJECTED")||a?.includes("REJECT")?C.red:a?.includes("HITL")||a?.includes("MODIFIED")?C.amber:a?.includes("FAIL")?C.red:a?.includes("ENRICHED")||a?.includes("VALIDATED")?C.blue:C.inkFaint;
  return (
    <div>
      <SectionHeader title="Immutable Audit Log" sub={`Complete activity trace for ${runId}. Every agent and human action permanently recorded.`}
        actions={<Btn variant="secondary" size="sm" icon={Ic.Download}>Export Report</Btn>}/>
      {loading&&<div style={{ display:"flex",justifyContent:"center",padding:48 }}><Spinner size={24}/></div>}
      {err&&<div style={{ padding:"11px 14px",background:C.redTint,borderRadius:8,fontSize:12,color:C.red,marginBottom:14 }}>{err}</div>}
      {!loading&&!err&&(
        <div style={{ position:"relative" }}>
          <div style={{ position:"absolute",left:22,top:12,bottom:0,width:1,background:C.border }}/>
          {logs.map((log,idx)=>{ let detail={}; try{detail=JSON.parse(log.detail||"{}");}catch{} const isHuman=log.agent==="HumanReviewer"; const col=acol(log.action);
            return (
              <div key={log.id} style={{ display:"flex",gap:16,paddingBottom:14,paddingLeft:12,animation:`fadeUp .2s ease ${idx*.025}s both` }}>
                <div style={{ width:22,height:22,borderRadius:"50%",background:isHuman?C.blue:C.surface,border:`2px solid ${isHuman?C.blue:C.border}`,flexShrink:0,zIndex:1,display:"flex",alignItems:"center",justifyContent:"center",marginTop:10 }}>
                  {isHuman?<Ic.Users style={{ width:10,height:10,color:"#fff" }}/>:<span style={{ width:7,height:7,borderRadius:"50%",background:col,display:"block" }}/>}
                </div>
                <Card style={{ flex:1,padding:"12px 16px",borderRadius:9 }}>
                  <div style={{ display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:6,gap:8 }}>
                    <div style={{ display:"flex",gap:7,alignItems:"center",flexWrap:"wrap" }}>
                      <span style={{ fontSize:13,fontWeight:700,color:C.ink,fontFamily:FONT.display }}>{log.agent}</span>
                      <span style={{ padding:"2px 7px",background:col+"15",color:col,borderRadius:4,fontSize:10,fontWeight:700,fontFamily:FONT.mono }}>{log.action}</span>
                      {isHuman&&<span style={{ padding:"2px 7px",background:C.blueTint,color:C.blue,borderRadius:4,fontSize:10,fontWeight:700,fontFamily:FONT.mono }}>MANUAL OVERRIDE</span>}
                    </div>
                    <span style={{ fontSize:10,color:C.inkFaint,fontFamily:FONT.mono,whiteSpace:"nowrap",flexShrink:0 }}>{log.timestamp?new Date(log.timestamp).toLocaleString():""}</span>
                  </div>
                  <p style={{ margin:"0 0 4px",fontSize:11,color:C.inkFaint,fontFamily:FONT.mono }}>Trade: {log.trade_id}</p>
                  {detail.reviewer_note&&<div style={{ padding:"6px 10px",background:C.surfaceAlt,borderRadius:5,borderLeft:`2px solid ${C.blue}`,marginTop:6 }}><p style={{ margin:0,fontSize:11,color:C.inkMuted,lineHeight:1.5 }}>{detail.reviewer_note}</p></div>}
                </Card>
              </div>
            );
          })}
          {!logs.length&&<Empty icon={Ic.Audit} title="No audit entries yet" sub="Entries appear as agents process each trade."/>}
        </div>
      )}
    </div>
  );
}

// ─── REPORT TAB ───────────────────────────────────────────────────────────────
function ReportTab({ data }) {
  if(!data) return <Empty icon={Ic.Report} title="No report generated" sub="Run a pipeline to generate the MiFID II compliance report."/>;
  const { stats={}, mifid_report_csv="", run_id="" } = data;
  const corrections = data?.corrections || data?.report_json?.corrections || [];
  const [copied,setCopied]   = useState(false);
  const [activeTab,setActiveTab] = useState("table");

  const { headers, rows } = (() => {
    if(!mifid_report_csv) return { headers:[], rows:[] };
    const lines=mifid_report_csv.trim().split("\n").filter(Boolean);
    if(!lines.length) return { headers:[], rows:[] };
    const parseRow=(line)=>{ const result=[]; let cur=""; let inQ=false; for(let i=0;i<line.length;i++){ const ch=line[i]; if(ch==='"'){ if(inQ&&line[i+1]==='"'){cur+='"';i++;}else inQ=!inQ; }else if(ch===','&&!inQ){result.push(cur.trim());cur="";}else{cur+=ch;} } result.push(cur.trim()); return result; };
    return { headers:parseRow(lines[0]), rows:lines.slice(1).map(parseRow) };
  })();

  const dl=()=>{ const b=new Blob([mifid_report_csv],{type:"text/csv"}); const a=document.createElement("a"); a.href=URL.createObjectURL(b); a.download=`${run_id}_mifid.csv`; a.click(); };
  const copy=()=>{ navigator.clipboard?.writeText(mifid_report_csv); setCopied(true); setTimeout(()=>setCopied(false),2000); };
  const getCellStyle=(h,v)=>{
    const hh=(h||"").toLowerCase(); const vv=(v||"").toUpperCase();
    if(hh==="final_status"||hh==="status") return {PASS:{color:C.green,bg:C.greenTint,border:C.greenBorder},HITL:{color:C.amber,bg:C.amberTint,border:C.amberBorder},FAIL:{color:C.red,bg:C.redTint,border:C.redBorder},REJECTED:{color:C.red,bg:C.redTint,border:C.redBorder},APPLIED:{color:C.violet,bg:C.violetTint,border:C.violetBorder}}[vv]||null;
    if(hh==="risk_level") return {HIGH:{color:C.red,bg:C.redTint,border:C.redBorder},MEDIUM:{color:C.amber,bg:C.amberTint,border:C.amberBorder},LOW:{color:C.green,bg:C.greenTint,border:C.greenBorder}}[vv]||null;
    if(hh==="passed"||hh==="compliant"){ if(vv==="TRUE") return {color:C.green,bg:C.greenTint,border:C.greenBorder}; if(vv==="FALSE") return {color:C.red,bg:C.redTint,border:C.redBorder}; }
    return null;
  };
  const TRUNCATE=["decision_reason","summary","notes","executing_entity_lei","buyer_lei","seller_lei"];
  const tabSty=(active)=>({ padding:"6px 14px",borderRadius:7,border:"none",fontSize:12,fontWeight:600,cursor:"pointer",fontFamily:FONT.body,background:active?C.blue:"transparent",color:active?"#fff":C.inkMuted,transition:"all .13s" });

  return (
    <div>
      <SectionHeader title="Final Submission Portal" sub="Verify compliance scoring and export the final MiFID II regulatory report."
        actions={<><Btn variant="secondary" size="sm" icon={Ic.Refresh}>Re-verify</Btn><Btn variant="primary" size="sm" icon={Ic.Download} onClick={dl}>Export CSV</Btn></>}/>
      <div style={{ display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:12,marginBottom:18 }}>
        <StatCard label="Total Records" value={(stats.total||0).toLocaleString()} accent={C.blue} icon={Ic.Layer} sub={stats.generated_at?new Date(stats.generated_at).toLocaleDateString():"—"}/>
        <StatCard label="Export Status" value="Ready" accent={C.green} icon={Ic.Check} sub="Verified integrity"/>
        <StatCard label="Run Reference" value={run_id.split("-").slice(-1)[0]} accent={C.violet} icon={Ic.Audit} sub={run_id}/>
      </div>
      <div style={{ background:`linear-gradient(135deg,${C.blue} 0%,${C.blueDark} 100%)`,borderRadius:14,padding:"22px 28px",marginBottom:18,display:"grid",gridTemplateColumns:"1fr auto",gap:16,alignItems:"center",boxShadow:`0 8px 24px rgba(0,86,197,.25)` }}>
        <div>
          <span style={{ fontSize:10,color:"rgba(255,255,255,.55)",textTransform:"uppercase",letterSpacing:".12em",fontWeight:700,fontFamily:FONT.mono }}>Generated Final Archive</span>
          <h3 style={{ margin:"7px 0 5px",fontSize:20,fontWeight:800,color:"#fff",fontFamily:FONT.display,letterSpacing:"-.02em" }}>Download MiFID II Compliance Report</h3>
          <p style={{ margin:0,fontSize:12,color:"rgba(255,255,255,.65)" }}>Full trade lineage, AI anomaly justifications, confidence scores, and complete decision audit trail.</p>
        </div>
        <Btn onClick={dl} style={{ background:"rgba(255,255,255,.15)",color:"#fff",border:"1px solid rgba(255,255,255,.25)" }}>
          <Ic.Download style={{ width:14,height:14 }}/> Download
        </Btn>
      </div>
      {mifid_report_csv&&(
        <Card noPad style={{ marginBottom:14 }}>
          <div style={{ padding:"12px 16px",borderBottom:`1px solid ${C.border}`,display:"flex",justifyContent:"space-between",alignItems:"center",gap:12,background:C.surfaceAlt }}>
            <div><p style={{ margin:0,fontSize:13,fontWeight:700,color:C.ink,fontFamily:FONT.display }}>Data Preview — Report Table</p><p style={{ margin:"2px 0 0",fontSize:11,color:C.inkFaint }}>{rows.length} record{rows.length!==1?"s":""} · {headers.length} fields</p></div>
            <div style={{ display:"flex",alignItems:"center",gap:8 }}>
              <div style={{ display:"flex",gap:4,padding:"4px",background:C.bg,borderRadius:9,border:`1px solid ${C.border}` }}>
                <button style={tabSty(activeTab==="table")} onClick={()=>setActiveTab("table")}>Table View</button>
                <button style={tabSty(activeTab==="raw")} onClick={()=>setActiveTab("raw")}>Raw CSV</button>
              </div>
              <Btn variant="secondary" size="xs" icon={copied?Ic.Check:Ic.Copy} onClick={copy}>{copied?"Copied!":"Copy"}</Btn>
              <Btn variant="secondary" size="xs" icon={Ic.Download} onClick={dl}>Download</Btn>
            </div>
          </div>
          {activeTab==="table"&&(
            <div style={{ overflowX:"auto",overflowY:"auto",maxHeight:420,position:"relative" }}>
              <table style={{ width:"100%",borderCollapse:"collapse",fontSize:12,minWidth:900 }}>
                <thead style={{ position:"sticky",top:0,zIndex:2 }}>
                  <tr style={{ background:"#EEF2F8" }}>
                    <th style={{ padding:"10px 14px",textAlign:"left",fontSize:10,color:C.inkFaint,fontWeight:700,textTransform:"uppercase",letterSpacing:".07em",borderBottom:`2px solid ${C.border}`,whiteSpace:"nowrap",position:"sticky",left:0,background:"#EEF2F8",zIndex:3,boxShadow:"2px 0 6px rgba(15,23,42,.06)" }}>#</th>
                    {headers.map((h,i)=><th key={i} style={{ padding:"10px 14px",textAlign:"left",fontSize:10,color:C.inkFaint,fontWeight:700,textTransform:"uppercase",letterSpacing:".07em",borderBottom:`2px solid ${C.border}`,whiteSpace:"nowrap",borderLeft:`1px solid ${C.border}` }}>{h.replace(/_/g," ")}</th>)}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row,ri)=>{
                    const statusIdx=headers.findIndex(h=>h.toLowerCase()==="final_status"||h.toLowerCase()==="status");
                    const rowStatus=statusIdx>=0?(row[statusIdx]||"").toUpperCase():"";
                    const isFail=rowStatus==="FAIL";
                    const baseBg=isFail?C.redTint+"50":ri%2===0?C.surface:C.surfaceAlt;
                    return (
                      <tr key={ri} style={{ background:baseBg,borderBottom:`1px solid ${C.border}`,transition:"background .1s",...(isFail&&{borderLeft:`3px solid ${C.red}`})}}
                        onMouseEnter={e=>e.currentTarget.style.background=isFail?C.redTint:C.blueTint+"50"}
                        onMouseLeave={e=>e.currentTarget.style.background=baseBg}>
                        <td style={{ padding:"9px 14px",fontSize:11,color:C.inkFaint,fontFamily:FONT.mono,textAlign:"center",fontWeight:600,background:"inherit",position:"sticky",left:0,zIndex:1,borderRight:`2px solid ${C.border}`,boxShadow:"2px 0 6px rgba(15,23,42,.04)" }}>{ri+1}</td>
                        {headers.map((h,ci)=>{
                          const val=row[ci]??""; const bs=getCellStyle(h,val); const trunc=TRUNCATE.includes((h||"").toLowerCase()); const isId=["trade_id","_original_trade_id"].includes((h||"").toLowerCase()); const isConf=(h||"").toLowerCase().includes("confidence");
                          return (
                            <td key={ci} style={{ padding:"9px 14px",borderLeft:`1px solid ${C.border}`,verticalAlign:"middle" }}>
                              {isId?<span style={{ fontFamily:FONT.mono,fontSize:11,color:isFail?C.red:C.blue,fontWeight:700 }}>{val}</span>
                              :isConf?<div style={{ display:"flex",alignItems:"center",gap:7,minWidth:100 }}><div style={{ flex:1,height:5,background:C.border,borderRadius:3,overflow:"hidden" }}><div style={{ width:`${Math.max(0,Math.min(100,Math.round(parseFloat(val||0)*100)))}%`,height:"100%",background:rowStatus==="FAIL"?C.red:rowStatus==="HITL"?C.amber:C.green,borderRadius:3 }}/></div><span style={{ fontSize:10,fontWeight:700,color:C.inkMuted,minWidth:26,textAlign:"right",fontFamily:FONT.mono }}>{Math.max(0,Math.min(100,Math.round(parseFloat(val||0)*100)))}%</span></div>
                              :bs?<span style={{ display:"inline-flex",alignItems:"center",gap:4,padding:"2px 8px",borderRadius:5,fontSize:11,fontWeight:700,background:bs.bg,color:bs.color,border:`1px solid ${bs.border}`,fontFamily:FONT.mono,letterSpacing:".02em",whiteSpace:"nowrap" }}><span style={{ width:5,height:5,borderRadius:"50%",background:bs.color,display:"inline-block",flexShrink:0 }}/>{val.toUpperCase()}</span>
                              :trunc?<span title={val} style={{ display:"block",maxWidth:260,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap",fontSize:12,color:C.inkMid,lineHeight:1.4 }}>{val||<span style={{ color:C.inkFaint,fontStyle:"italic" }}>—</span>}</span>
                              :<span style={{ fontSize:12,color:val?C.ink:C.inkFaint,fontStyle:val?"normal":"italic" }}>{val||"—"}</span>}
                            </td>
                          );
                        })}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              {rows.length===0&&<div style={{ padding:"40px 24px",textAlign:"center",color:C.inkFaint,fontSize:13 }}>No data rows found in CSV.</div>}
            </div>
          )}
          {activeTab==="raw"&&<pre style={{ margin:0,padding:"14px 18px",fontSize:11,color:C.inkMuted,overflowX:"auto",maxHeight:380,fontFamily:FONT.mono,lineHeight:1.8,background:C.surfaceAlt }}>{mifid_report_csv}</pre>}
          {activeTab==="table"&&rows.length>0&&(
            <div style={{ padding:"10px 16px",borderTop:`1px solid ${C.border}`,background:C.surfaceAlt,display:"flex",gap:16,alignItems:"center" }}>
              <span style={{ fontSize:11,color:C.inkFaint }}>Showing <strong style={{ color:C.ink }}>{rows.length}</strong> records across <strong style={{ color:C.ink }}>{headers.length}</strong> fields</span>
              <div style={{ flex:1 }}/><Btn variant="ghost" size="xs" icon={Ic.Download} onClick={dl}>Download Full CSV</Btn>
            </div>
          )}
        </Card>
      )}
      {corrections.length>0&&(
        <Card noPad>
          <CardHeader title="Auto-Fix Audit Trail" sub={`${corrections.length} field correction${corrections.length!==1?"s":""} applied by agents`} right={<Badge status="APPLIED"/>}/>
          <div style={{ padding:"14px 18px",display:"flex",flexDirection:"column",gap:10 }}>
            {corrections.map((c,i)=>(
              <div key={i} style={{ display:"flex",gap:12,alignItems:"flex-start",padding:"13px 15px",background:C.violetTint,border:`1px solid ${C.violetBorder}`,borderRadius:10,borderLeft:`3px solid ${C.violet}` }}>
                <div style={{ width:30,height:30,borderRadius:8,background:C.violet+"20",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0,color:C.violet }}><Ic.Wand style={{ width:14,height:14 }}/></div>
                <div style={{ flex:1,minWidth:0 }}>
                  <div style={{ display:"flex",gap:8,alignItems:"center",marginBottom:8,flexWrap:"wrap" }}>
                    <Badge status="APPLIED" size="xs"/>
                    <span style={{ fontFamily:FONT.mono,fontSize:11,color:C.blue,fontWeight:700 }}>{c.trade_id}</span>
                    <span style={{ fontSize:11,color:C.inkMuted }}>field: <strong style={{ color:C.ink }}>{c.field}</strong></span>
                  </div>
                  <div style={{ display:"grid",gridTemplateColumns:"1fr 1fr",gap:8 }}>
                    <div style={{ padding:"6px 10px",background:C.redTint,border:`1px solid ${C.redBorder}`,borderRadius:6 }}>
                      <p style={{ margin:"0 0 3px",fontSize:9,color:C.red,fontWeight:700,textTransform:"uppercase",letterSpacing:".07em" }}>Before</p>
                      <p style={{ margin:0,fontSize:11,color:C.red,fontFamily:FONT.mono,wordBreak:"break-all" }}>{String(c.old_value||c.original_value||"—")}</p>
                    </div>
                    <div style={{ padding:"6px 10px",background:C.greenTint,border:`1px solid ${C.greenBorder}`,borderRadius:6 }}>
                      <p style={{ margin:"0 0 3px",fontSize:9,color:C.green,fontWeight:700,textTransform:"uppercase",letterSpacing:".07em" }}>After</p>
                      <p style={{ margin:0,fontSize:11,color:C.green,fontFamily:FONT.mono,wordBreak:"break-all" }}>{String(c.new_value||c.proposed_value||"—")}</p>
                    </div>
                  </div>
                  {(c.reasoning||c.reason)&&<p style={{ margin:"8px 0 0",fontSize:11,color:C.inkMuted,lineHeight:1.5 }}>{c.reasoning||c.reason}</p>}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

// ─── ROOT ─────────────────────────────────────────────────────────────────────
const NAV = [
  { id:"auditchat",  label:"Audit Chat",   Icon:Ic.Chat,   badge:null },
  { id:"input",      label:"Input",         Icon:Ic.Upload, badge:null },
  { id:"merge",      label:"Merge Sources", Icon:Ic.Layer,  badge:null },
  { id:"dashboard",  label:"Dashboard",     Icon:Ic.Home,   badge:null },
  { id:"validation", label:"Validation",    Icon:Ic.Shield, badge:null },
  { id:"risk",       label:"Risk",          Icon:Ic.Alert,  badge:null },
  { id:"hitl",       label:"HITL Queue",    Icon:Ic.Users,  badge:"hitl" },
  { id:"audit",      label:"Audit Trail",   Icon:Ic.Audit,  badge:null },
  { id:"report",     label:"Reports",       Icon:Ic.Report, badge:null },
];

export default function App() {
  const [tab,     setTab]  = useState("auditchat");
  const [data,    setData] = useState(null);
  const [hitlDec, setHD]   = useState({});
  const [sidebar, setSB]   = useState(true);

  const onComplete = useCallback(result => {
    setData({...result, hitl_queue:result.hitl_queue||[], corrections:result.corrections||result.report_json?.corrections||[], report_json:result.report_json||{}});
    setHD({});
    // Only auto-navigate if not coming from audit chat (so chat stays visible)
    if(tab !== "auditchat") setTab("dashboard");
  },[tab]);

  const onDecision = useCallback((id,dec,res)=>{ setHD(d=>({...d,[id]:{dec,res}})); },[]);

  const totalHITL   = data?.hitl_queue?.length||(data?.final_trades||[]).filter(t=>t.final_status==="HITL").length;
  const pendingHITL = Math.max(0, totalHITL - Object.keys(hitlDec).length);

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');
        *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
        html,body,#root{height:100%}
        body{font-family:${FONT.body};background:${C.bg};color:${C.ink};-webkit-font-smoothing:antialiased;font-size:14px;line-height:1.5}
        @keyframes spin{to{transform:rotate(360deg)}}
        @keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
        @keyframes pulseRing{0%,100%{opacity:1}50%{opacity:.5}}
        @keyframes typingBounce{0%,100%{transform:translateY(0);opacity:.4}50%{transform:translateY(-4px);opacity:1}}
        ::-webkit-scrollbar{width:5px;height:5px}
        ::-webkit-scrollbar-thumb{background:${C.border};border-radius:3px}
        ::-webkit-scrollbar-thumb:hover{background:${C.borderMid}}
        ::selection{background:rgba(0,86,197,.15)}
        textarea,input,button{font-family:inherit}
        textarea{resize:vertical}
        main > div{animation:fadeUp .22s ease both}
        button:focus-visible{outline:2px solid ${C.blue};outline-offset:2px}
      `}</style>

      <div style={{ display:"flex", height:"100vh", overflow:"hidden", background:C.bg }}>

        {/* ── SIDEBAR ── */}
        <aside style={{ width:sidebar?220:60, background:C.surface, borderRight:`1px solid ${C.border}`, display:"flex", flexDirection:"column", flexShrink:0, transition:"width .24s cubic-bezier(.4,0,.2,1)", overflow:"hidden" }}>
          {/* Logo */}
          <div style={{ padding:"16px", borderBottom:`1px solid ${C.border}`, display:"flex", alignItems:"center", gap:9, minHeight:58 }}>
            <div style={{ width:30, height:30, borderRadius:9, background:`linear-gradient(135deg,${C.blue},${C.blueDark})`, display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0, boxShadow:`0 4px 10px rgba(0,86,197,.3)` }}>
              <Ic.Shield style={{ width:14, height:14, color:"#fff" }}/>
            </div>
            {sidebar&&<div style={{ overflow:"hidden", flex:1 }}>
              <p style={{ margin:0, fontSize:13, fontWeight:800, color:C.ink, fontFamily:FONT.display, letterSpacing:"-.02em", whiteSpace:"nowrap" }}>MiFID II AI</p>
              <p style={{ margin:0, fontSize:10, color:C.inkFaint, whiteSpace:"nowrap" }}>Agentic Control Center</p>
            </div>}
            <button onClick={()=>setSB(s=>!s)} style={{ background:"none", border:"none", cursor:"pointer", color:C.inkFaint, padding:3, marginLeft:sidebar?"0":"auto", flexShrink:0, display:"flex" }}>
              <Ic.ChevR style={{ width:14, height:14, transform:sidebar?"rotate(180deg)":"none", transition:"transform .2s" }}/>
            </button>
          </div>

          {/* Nav */}
          <nav style={{ padding:"8px", flex:1, overflowY:"auto" }}>
            {/* Separator before Audit Chat */}
            {sidebar&&<p style={{ margin:"8px 10px 4px", fontSize:9, fontWeight:700, color:C.inkFaint, textTransform:"uppercase", letterSpacing:".1em" }}>Intelligence</p>}
            {NAV.slice(0,1).map(({id,label,Icon,badge})=>{
              const active=tab===id; const badgeVal=badge==="hitl"&&pendingHITL>0?pendingHITL:null;
              return (
                <button key={id} onClick={()=>setTab(id)}
                  style={{ width:"100%", display:"flex", alignItems:"center", gap:9, padding:sidebar?"9px 11px":"9px", borderRadius:8, border:"none", background:active?C.blueTint:"transparent", color:active?C.blue:C.inkMuted, fontSize:13, fontWeight:active?700:400, transition:"all .13s", marginBottom:2, cursor:"pointer", textAlign:"left", fontFamily:FONT.body, whiteSpace:"nowrap", overflow:"hidden", position:"relative" }}
                  onMouseEnter={e=>{ if(!active) e.currentTarget.style.background=C.bg; }}
                  onMouseLeave={e=>{ if(!active) e.currentTarget.style.background="transparent"; }}>
                  {active&&<span style={{ position:"absolute", left:0, top:"18%", bottom:"18%", width:3, background:C.blue, borderRadius:"0 2px 2px 0" }}/>}
                  <Icon style={{ width:17, height:17, flexShrink:0 }}/>
                  {sidebar&&<><span style={{ flex:1 }}>{label}</span>{badgeVal&&<span style={{ background:C.amberTint, color:C.amber, borderRadius:10, padding:"1px 7px", fontSize:10, fontWeight:700, fontFamily:FONT.mono, border:`1px solid ${C.amberBorder}` }}>{badgeVal}</span>}</>}
                </button>
              );
            })}

            {sidebar&&<p style={{ margin:"12px 10px 4px", fontSize:9, fontWeight:700, color:C.inkFaint, textTransform:"uppercase", letterSpacing:".1em" }}>Pipeline</p>}
            {NAV.slice(1).map(({id,label,Icon,badge})=>{
              const active=tab===id; const badgeVal=badge==="hitl"&&pendingHITL>0?pendingHITL:null;
              return (
                <button key={id} onClick={()=>setTab(id)}
                  style={{ width:"100%", display:"flex", alignItems:"center", gap:9, padding:sidebar?"9px 11px":"9px", borderRadius:8, border:"none", background:active?C.blueTint:"transparent", color:active?C.blue:C.inkMuted, fontSize:13, fontWeight:active?700:400, transition:"all .13s", marginBottom:2, cursor:"pointer", textAlign:"left", fontFamily:FONT.body, whiteSpace:"nowrap", overflow:"hidden", position:"relative" }}
                  onMouseEnter={e=>{ if(!active) e.currentTarget.style.background=C.bg; }}
                  onMouseLeave={e=>{ if(!active) e.currentTarget.style.background="transparent"; }}>
                  {active&&<span style={{ position:"absolute", left:0, top:"18%", bottom:"18%", width:3, background:C.blue, borderRadius:"0 2px 2px 0" }}/>}
                  <Icon style={{ width:17, height:17, flexShrink:0 }}/>
                  {sidebar&&<><span style={{ flex:1 }}>{label}</span>{badgeVal&&<span style={{ background:C.amberTint, color:C.amber, borderRadius:10, padding:"1px 7px", fontSize:10, fontWeight:700, fontFamily:FONT.mono, border:`1px solid ${C.amberBorder}` }}>{badgeVal}</span>}</>}
                </button>
              );
            })}
          </nav>

          {/* System status */}
          {sidebar&&data&&(
            <div style={{ padding:"12px 14px", borderTop:`1px solid ${C.border}` }}>
              <div style={{ padding:"9px 11px", background:C.greenTint, borderRadius:8, border:`1px solid ${C.greenBorder}` }}>
                <div style={{ display:"flex", alignItems:"center", gap:6, marginBottom:3 }}>
                  <span style={{ width:6, height:6, borderRadius:"50%", background:C.green, animation:"pulseRing 1.5s ease infinite", boxShadow:`0 0 5px ${C.green}` }}/>
                  <span style={{ fontSize:10, fontWeight:700, color:C.green, fontFamily:FONT.mono }}>SYSTEM ONLINE</span>
                </div>
                <p style={{ margin:0, fontSize:10, color:C.inkMuted, fontFamily:FONT.mono, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap" }}>{data.run_id}</p>
              </div>
            </div>
          )}
        </aside>

        {/* ── MAIN ── */}
        <div style={{ flex:1, display:"flex", flexDirection:"column", overflow:"hidden" }}>
          {/* Header */}
          <header style={{ height:54, background:C.surface, borderBottom:`1px solid ${C.border}`, display:"flex", alignItems:"center", padding:"0 20px", gap:14, flexShrink:0 }}>
            <button onClick={()=>setSB(s=>!s)} style={{ background:"none", border:"none", cursor:"pointer", color:C.inkMuted, padding:6, borderRadius:6, display:"flex", marginRight:2 }}>
              <Ic.Menu style={{ width:15,height:15 }}/>
            </button>
            <div style={{ width:1, height:18, background:C.border }}/>
            <div style={{ display:"flex", gap:5, alignItems:"center", fontSize:13 }}>
              <span style={{ color:C.inkFaint }}>MiFID AI</span>
              <Ic.ChevR style={{ width:12,height:12,color:C.border }}/>
              <span style={{ color:C.ink, fontWeight:600 }}>{NAV.find(n=>n.id===tab)?.label}</span>
            </div>
            <div style={{ flex:1 }}/>
            {data&&(
              <div style={{ display:"flex", gap:6, padding:"5px 12px", background:C.surfaceAlt, borderRadius:8, fontSize:11, color:C.inkMuted, border:`1px solid ${C.border}`, fontFamily:FONT.mono }}>
                <span>Total:<strong style={{ color:C.ink,marginLeft:4 }}>{data.stats?.total||0}</strong></span>
                <span style={{ color:C.border }}>|</span>
                <span>Pass:<strong style={{ color:C.green,marginLeft:4 }}>{data.stats?.passed||0}</strong></span>
                <span style={{ color:C.border }}>|</span>
                <span>HITL:<strong style={{ color:C.amber,marginLeft:4 }}>{pendingHITL}</strong></span>
                <span style={{ color:C.border }}>|</span>
                <span>Fail:<strong style={{ color:C.red,marginLeft:4 }}>{(data?.final_trades||[]).filter(t=>t.final_status==="FAIL").length}</strong></span>
              </div>
            )}
            <div style={{ width:30, height:30, borderRadius:"50%", background:`linear-gradient(135deg,${C.blue},${C.blueDark})`, display:"flex", alignItems:"center", justifyContent:"center", fontSize:12, fontWeight:800, color:"#fff", fontFamily:FONT.display, flexShrink:0 }}>A</div>
          </header>

          {/* Content */}
          <main style={{ flex:1, overflowY:"auto", padding:22 }}>
            <div>
              {tab==="auditchat"  && <AuditChatTab  onComplete={onComplete}/>}
              {tab==="input"      && <InputTab       onComplete={onComplete}/>}
              {tab==="merge"      && <MergeTab       onComplete={onComplete}/>}
              {tab==="dashboard"  && <DashboardTab   data={data}/>}
              {tab==="validation" && <ValidationTab  results={data?.validation_results||[]} complianceResults={data?.compliance_results||[]}/>}
              {tab==="risk"       && <RiskTab         results={data?.risk_results||[]}/>}
              {tab==="hitl"       && <HITLTab         data={data} runId={data?.run_id} onDecision={onDecision}/>}
              {tab==="audit"      && <AuditTab        runId={data?.run_id}/>}
              {tab==="report"     && <ReportTab       data={data}/>}
            </div>
          </main>
        </div>
      </div>
    </>
  );
}