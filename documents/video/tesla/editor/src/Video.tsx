// Plan-driven intro-video editor (tools/video/kit). Old-PewDiePie, human-made style:
// see documents/video/EDITING-STYLE.md. Everything on screen comes from src/plan.json, which
// tools/video/build_plan.py resolves from the planner's pipeline/plan.json (word anchors -> seconds).
// Generalised from the Infosys Draft 2 editor (Manit: "love it").
import React from "react";
import {
  AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, random, staticFile, useCurrentFrame, Easing,
} from "remotion";
import { loadFont as loadMont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import planJson from "./plan.json";
import face from "./face_track.json";
import words from "./words.json";
import { Custom } from "./Custom";

const { fontFamily: MONT } = loadMont("normal", { weights: ["600", "700", "800", "900"] });
const { fontFamily: ANTON } = loadAnton();

type Span = { from: number; to: number };
type Plan = {
  length: number;
  anchors?: Record<string, number>;
  captions?: { on: boolean; top?: number; lift?: (Span & { top: number })[]; fix?: Record<string, string> };
  zooms?: (Span & { scale: number; tilt?: number })[];
  follow?: (Span & { scale?: number; amount?: number })[];
  bw?: Span[];
  shakes?: { at: number; strength?: number }[];
  broll?: (Span & { src: string; start?: number; layout?: "split" | "full"; zoom?: number; focus?: [number, number]; push?: number })[];
  texts?: (Span & { txt: string; size?: number; top?: number; x?: number; rot?: number })[];
  stickers?: (Span & { src: string; x: number; y: number; width?: number; anim?: "pop" | "slide" | "rise"; rise_to?: [number, number]; label?: string })[];
  bursts?: { at: number; x: number; y: number }[];
  nametag?: Span & { name: string; subtitle?: string };
  endcard?: { from: number; title?: string; name: string; subtitle?: string; lines?: string[] };
  sfx?: { name: string; at: number; vol?: number; max?: number }[];
  music?: { src: string; startAt: number; musicFrom: number; volume: number; stops?: Span[]; dips?: (Span & { factor: number })[]; endBoost?: number };
  custom?: boolean;
};
const P = planJson as unknown as Plan;

export const FPS = 30;
export const TOTAL_FRAMES = Math.round(P.length * FPS);
const F = (t: number) => Math.round(t * FPS);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp = (t: number, a: number[], b: number[], ease?: (x: number) => number) => interpolate(t, a, b, { ...clamp, easing: ease });
const inSpan = (t: number, s: Span, pad = 0) => t >= s.from - pad && t < s.to + pad;

// ---------- face track ----------
type Row = number[];
const at = (rows: Row[], t: number) => {
  if (!rows.length) return [540, 860, 380];
  if (t <= rows[0][0]) return rows[0].slice(1);
  for (let i = 1; i < rows.length; i++) {
    if (t <= rows[i][0]) {
      const a = rows[i - 1], b = rows[i], k = (t - a[0]) / (b[0] - a[0]);
      return a.slice(1).map((v, j) => v + (b[j + 1] - v) * k);
    }
  }
  return rows[rows.length - 1].slice(1);
};
const faceAt = (t: number) => at(face as Row[], t) as [number, number, number];

// ---------- meme text ----------
const meme = (size: number, stroke = Math.round(size / 9)): React.CSSProperties => ({
  fontFamily: ANTON, fontSize: size, color: "#FFFFFF", lineHeight: 1.05, letterSpacing: 1,
  WebkitTextStroke: `${stroke}px #000`, paintOrder: "stroke fill", textTransform: "uppercase", whiteSpace: "nowrap",
});
const punch = (t: number, t0: number) => (t - t0 < 1 / FPS ? 1.18 : t - t0 < 2 / FPS ? 1.06 : 1);

// ======================================================================
// Camera: snap zooms that follow his face, slow follows, shakes
// ======================================================================
type Cam = { s: number; tx: number; ty: number; rot: number };
const camAt = (t: number): Cam => {
  let s = 1, tx = 0, ty = 0, rot = 0;
  for (const f of P.follow ?? []) {
    if (!inSpan(t, f, 0.3)) continue;
    const k = Math.min(lerp(t, [f.from - 0.3, f.from], [0, 1], Easing.out(Easing.cubic)), lerp(t, [f.to, f.to + 0.3], [1, 0]));
    const [fx, fy] = faceAt(t);
    s = 1 + ((f.scale ?? 1.15) - 1) * k;
    const look = (fx - 540) * (f.amount ?? 0.9);
    const cx = 540 + look, cy = fy + 90;
    tx = k * (540 - s * cx); ty = k * (960 - s * cy);
    rot = (look / 540) * 3 * k;
  }
  for (const z of P.zooms ?? []) {
    if (t >= z.from && t < z.to + 2 / FPS) {
      const k = Math.min(lerp(t, [z.from, z.from + 2 / FPS], [0, 1]), lerp(t, [z.to, z.to + 2 / FPS], [1, 0]));
      const [fx, fy] = faceAt(t);
      s = 1 + (z.scale - 1) * k;
      const drift = Math.sin(t * 2.3) * 6;
      tx = k * (540 - s * fx + drift);
      ty = k * (800 - s * fy);
      rot = (z.tilt ?? 0) * k;
    }
  }
  tx = Math.min(0, Math.max(1080 - s * 1080, tx));
  ty = Math.min(0, Math.max(1920 - s * 1920, ty));
  for (const sh of P.shakes ?? []) {
    const d = t - sh.at;
    if (d >= 0 && d < 0.35) {
      const e = Math.exp(-d * 9) * (sh.strength ?? 14);
      tx = Math.min(0, Math.max(1080 - s * 1080, tx + Math.sin(d * 120) * e));
      ty = Math.min(0, Math.max(1920 - s * 1920, ty + Math.cos(d * 97) * e));
    }
  }
  return { s, tx, ty, rot };
};

const SPLITS = (P.broll ?? []).filter((b) => (b.layout ?? "split") === "split");
const FULLS = (P.broll ?? []).filter((b) => b.layout === "full");
const splitK = (t: number) => {
  for (const b of SPLITS) if (t >= b.from - 0.01 && t < b.to + 0.15)
    return Math.min(lerp(t, [b.from, b.from + 0.12], [0, 1], Easing.out(Easing.cubic)), lerp(t, [b.to, b.to + 0.12], [1, 0], Easing.in(Easing.cubic)));
  return 0;
};

const cameraStyle = (t: number): React.CSSProperties => {
  const c = camAt(t);
  const sk = splitK(t);
  const bw = (P.bw ?? []).some((b) => inSpan(t, b));
  const extra = c.rot !== 0 ? 1.05 : 1; // hides corners when tilted
  return {
    transformOrigin: "0px 0px",
    transform: `translate(0px, ${sk * 520}px) translate(${c.tx}px, ${c.ty}px) scale(${c.s}) translate(540px, 960px) rotate(${c.rot}deg) scale(${extra}) translate(-540px, -960px)`,
    filter: bw ? "grayscale(1) contrast(1.15)" : "none",
    overflow: "hidden",
  };
};

const isImg = (src: string) => /\.(png|jpe?g|webp)$/i.test(src);
const BrollMedia: React.FC<{ b: NonNullable<Plan["broll"]>[number]; t: number; w: number; h: number }> = ({ b, t, w, h }) => {
  const z = b.zoom ?? 1, [fx, fy] = b.focus ?? [w / 2, h / 2];
  const push = 1 + (b.push ?? (isImg(b.src) ? 0.25 : 0)) * lerp(t, [b.from, b.to + 0.15], [0, 1]);
  const S = z * push;
  return (
    <AbsoluteFill style={{ transformOrigin: "0 0", transform: `translate(${w / 2 - S * fx}px, ${h / 2 - S * fy}px) scale(${S})` }}>
      {isImg(b.src)
        ? <Img src={staticFile(b.src)} style={{ width: w, height: h, objectFit: "cover" }} />
        : <OffthreadVideo muted src={staticFile(b.src)} startFrom={Math.round((b.start ?? 0) * FPS)} style={{ width: w, height: h, objectFit: "cover" }} />}
    </AbsoluteFill>
  );
};

const SplitBroll: React.FC<{ t: number }> = ({ t }) => {
  const k = splitK(t);
  if (k <= 0) return null;
  return (
    <AbsoluteFill style={{ height: 960 * k, overflow: "hidden", borderBottom: "6px solid #fff" }}>
      {SPLITS.map((b, i) => (
        <Sequence key={i} from={F(b.from)} durationInFrames={Math.max(1, F(b.to + 0.2) - F(b.from))}>
          <BrollMedia b={b} t={t} w={1080} h={960} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const FullBroll: React.FC<{ t: number }> = ({ t }) => (
  <>
    {FULLS.map((b, i) => (
      <Sequence key={i} from={F(b.from)} durationInFrames={Math.max(1, F(b.to) - F(b.from))}>
        <AbsoluteFill style={{ overflow: "hidden" }}><BrollMedia b={b} t={t} w={1080} h={1920} /></AbsoluteFill>
      </Sequence>
    ))}
  </>
);

// ======================================================================
// Overlays
// ======================================================================
const Stickers: React.FC<{ t: number }> = ({ t }) => (
  <AbsoluteFill>
    {(P.stickers ?? []).map((s, i) => {
      if (!inSpan(t, s)) return null;
      const anim = s.anim ?? "pop";
      let x = s.x, y = s.y, sc = 1;
      if (anim === "pop") sc = lerp(t, [s.from, s.from + 0.12], [0, 1], Easing.out(Easing.back(2.5)));
      if (anim === "slide") x = -400 + (s.x + 400) * lerp(t, [s.from, s.from + 0.14], [0, 1], Easing.out(Easing.back(1.6)));
      if (anim === "rise" && s.rise_to) {
        sc = lerp(t, [s.from, s.from + 0.12], [0, 1], Easing.out(Easing.back(2.5)));
        const k = lerp(t, [s.from + 0.08, s.from + 0.65], [0, 1], Easing.out(Easing.cubic));
        x = s.x + (s.rise_to[0] - s.x) * k + Math.sin(t * 3) * 8 * k;
        y = s.y + (s.rise_to[1] - s.y) * k + Math.sin(t * 4) * 10 * k;
      }
      const wob = Math.sin(t * 5 + i) * 4;
      return (
        <div key={i} style={{ position: "absolute", left: x, top: y, transform: `translate(-50%,-50%) scale(${sc}) rotate(${wob}deg)` }}>
          {s.label && <div style={{ position: "absolute", top: -95, width: s.width ?? 420, textAlign: "center", transform: `rotate(-4deg) scale(${punch(t, s.from)})` }}><div style={{ ...meme(110), display: "inline-block" }}>{s.label}</div></div>}
          <Img src={staticFile(s.src)} style={{ width: s.width ?? 420, filter: "drop-shadow(0 12px 20px rgba(0,0,0,0.5))" }} />
        </div>
      );
    })}
  </AbsoluteFill>
);

const Bursts: React.FC<{ t: number }> = ({ t }) => (
  <>
    {(P.bursts ?? []).map((b, k) => t >= b.at && t < b.at + 0.18 && (
      <svg key={k} width={1080} height={1920} style={{ position: "absolute" }}>
        {Array.from({ length: 10 }).map((_, i) => {
          const a = (i / 10) * Math.PI * 2 + random(`b${k}`), d = lerp(t, [b.at, b.at + 0.18], [40, 150]);
          return <line key={i} x1={b.x + Math.cos(a) * d} y1={b.y + Math.sin(a) * d} x2={b.x + Math.cos(a) * (d + 50)} y2={b.y + Math.sin(a) * (d + 50)}
            stroke="#fff" strokeWidth={12} strokeLinecap="round" />;
        })}
      </svg>
    ))}
  </>
);

const MemeText: React.FC<{ t: number }> = ({ t }) => (
  <AbsoluteFill>
    {(P.texts ?? []).map((x, i) => inSpan(t, x) && (
      <div key={i} style={{ position: "absolute", top: x.top ?? 250, left: x.x !== undefined ? x.x - 540 : 0, width: 1080, textAlign: "center" }}>
        <div style={{ ...meme(x.size ?? 120), display: "inline-block", transform: `rotate(${x.rot ?? 0}deg) scale(${punch(t, x.from)})` }}>{x.txt}</div>
      </div>
    ))}
  </AbsoluteFill>
);

const NameTag: React.FC<{ t: number }> = ({ t }) => {
  const n = P.nametag;
  if (!n || !inSpan(t, n)) return null;
  return (
    <div style={{ position: "absolute", left: 56, top: 190, transform: `rotate(-2deg) scale(${punch(t, n.from)})`, transformOrigin: "0 0" }}>
      <div style={meme(110)}>{n.name}</div>
      {n.subtitle && <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 38, color: "#fff", WebkitTextStroke: "6px #000", paintOrder: "stroke fill" }}>{n.subtitle}</div>}
    </div>
  );
};

const EndCard: React.FC<{ t: number }> = ({ t }) => {
  const e = P.endcard;
  if (!e || t < e.from) return null;
  return (
    <AbsoluteFill style={{ background: "#000", justifyContent: "center", alignItems: "center", textAlign: "center", color: "#fff", fontFamily: MONT }}>
      {e.title && <div style={{ ...meme(84), transform: `scale(${punch(t, e.from)})` }}>{e.title}</div>}
      <div style={{ ...meme(130), marginTop: e.title ? 70 : 0 }}>{e.name}</div>
      {e.subtitle && <div style={{ fontSize: 40, fontWeight: 600, marginTop: 20 }}>{e.subtitle}</div>}
      {(e.lines ?? []).map((l, i) => <div key={i} style={{ fontSize: i === 0 ? 46 : 36, fontWeight: i === 0 ? 800 : 600, marginTop: i === 0 ? 70 : 20 }}>{l}</div>)}
    </AbsoluteFill>
  );
};

// ---------- captions: white, black outline, 2-4 words, current word yellow ----------
type Wd = { w: string; s: number; e: number };
const CHUNKS = (() => {
  const fix = P.captions?.fix ?? {};
  const src = (words as Wd[]).map((x) => ({ ...x, w: fix[x.w.trim()] ?? x.w.trim() }));
  const res: { words: Wd[]; s: number; e: number }[] = [];
  let cur: Wd[] = [];
  const flush = () => { if (cur.length) res.push({ words: cur.map((c) => ({ ...c, w: c.w.replace(/[.,]+$/, "") })), s: cur[0].s, e: cur[cur.length - 1].e }); cur = []; };
  src.forEach((x, i) => {
    const next = src[i + 1];
    cur.push(x);
    const len = cur.map((c) => c.w).join(" ").length;
    if (cur.length >= 4 || len > 15 || /[.,?!]$/.test(x.w) || !next || next.s - x.e > 0.35) flush();
  });
  for (let i = 0; i < res.length; i++) res[i].e = Math.min(res[i].e + 0.25, res[i + 1] ? res[i + 1].s : Infinity);
  return res;
})();
const Captions: React.FC<{ t: number }> = ({ t }) => {
  const c0 = P.captions;
  if (!c0?.on || (P.endcard && t >= P.endcard.from)) return null;
  const c = CHUNKS.find((x) => t >= x.s && t < x.e);
  if (!c) return null;
  const lift = (c0.lift ?? []).find((l) => inSpan(t, l));
  const top = lift ? lift.top : c0.top ?? 1600;
  return (
    <div style={{ position: "absolute", top, left: 140, width: 800, textAlign: "center" }}>
      {c.words.map((w, i) => {
        const next = c.words[i + 1];
        const on = t >= w.s && (!next || t < next.s);
        return (
          <span key={i} style={{ fontFamily: MONT, fontWeight: 900, fontSize: 64, color: on ? "#FFE11A" : "#FFFFFF", WebkitTextStroke: "10px #000",
            paintOrder: "stroke fill", lineHeight: 1.15, display: "inline-block", margin: "0 15px", transform: on ? "scale(1.08)" : "none" }}>{w.w}</span>
        );
      })}
    </div>
  );
};

// ======================================================================
// Sound: voice, music (with stops that pause it, dips, end boost), sound effects
// ======================================================================
const Music: React.FC = () => {
  const m = P.music;
  if (!m) return null;
  // play segments between stops; each segment resumes the music where it paused
  const stops = [...(m.stops ?? [])].sort((a, b) => a.from - b.from);
  const segs: { a: number; b: number; from: number }[] = [];
  let a = Math.max(0, m.startAt), mt = m.musicFrom + Math.max(0, -m.startAt);
  for (const s of stops) {
    if (s.from > a) { segs.push({ a, b: s.from, from: mt }); mt += s.from - a; }
    a = Math.max(a, s.to);
  }
  if (a < P.length) segs.push({ a, b: P.length, from: mt });
  const endFrom = P.endcard?.from ?? Infinity;
  return (
    <>
      {segs.map((g, i) => (
        <Sequence key={i} from={F(g.a)} durationInFrames={Math.max(1, F(g.b) - F(g.a))}>
          <Audio src={staticFile(m.src)} startFrom={F(g.from)} volume={(f) => {
            const tt = g.a + f / FPS;
            const dip = (m.dips ?? []).filter((d) => inSpan(tt, d)).reduce((x, d) => x * d.factor, 1);
            const end = tt >= endFrom ? m.endBoost ?? 1 : 1;
            const fade = interpolate(tt, [P.length - 1.0, P.length], [1, 0], clamp);
            return m.volume * dip * end * fade;
          }} />
        </Sequence>
      ))}
    </>
  );
};

// ======================================================================
export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={cameraStyle(t)}>
        <OffthreadVideo muted src={staticFile("th/track.mp4")} />
      </AbsoluteFill>
      <FullBroll t={t} />
      <SplitBroll t={t} />
      <Stickers t={t} />
      <Bursts t={t} />
      {P.custom && <Custom t={t} W={P.anchors ?? {}} face={faceAt} />}
      <MemeText t={t} />
      <NameTag t={t} />
      <Captions t={t} />
      <EndCard t={t} />
      <Audio src={staticFile("th/track.mp4")} />
      <Music />
      {(P.sfx ?? []).map((s, i) => (
        <Sequence key={i} from={F(s.at)} durationInFrames={s.max ? Math.round(s.max * FPS) : undefined}>
          <Audio src={staticFile(`sfx/${s.name}.wav`)} volume={s.vol ?? 0.4} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
