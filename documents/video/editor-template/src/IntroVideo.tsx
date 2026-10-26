import React from "react";
import {
  AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, Video, getRemotionEnvironment, interpolate, spring,
  staticFile, useCurrentFrame, useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import timeline from "./timeline.json";

const { fontFamily } = loadFont("normal", { weights: ["600", "700", "800", "900"] });

// Abi's colours, as seen in Andromeda's own videos
const PINK = "#E6197F";
const LIME = "#B9E31E";
const ORANGE = "#F5821F";
const PURPLE = "#8F7BEA";
const INK = "#151515";

const fps = timeline.fps;
const f = (s: number) => Math.round(s * fps);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Layout: with B-roll up, footage fills the top half and the face sits in the bottom half.
const SEAM = 960;        // y of the line between the halves
const FACE_SHIFT = 150;  // how far the face video moves up inside the bottom half
const RAMP = 0.3;        // seconds to slide into / out of split screen

// Smooth playback in the Studio preview, frame-accurate extraction only for the final render.
const Clip: React.FC<React.ComponentProps<typeof OffthreadVideo>> = (props) =>
  getRemotionEnvironment().isRendering ? <OffthreadVideo {...props} /> : <Video {...(props as any)} />;

// ---------- split amount over time (0 = face full screen, 1 = split) ----------
const intervals = (() => {
  const raw = timeline.broll.filter((b) => !b.src.startsWith("full:")).map((b) => [b.start, b.start + b.dur]).sort((a, b) => a[0] - b[0]);
  const merged: number[][] = [];
  for (const iv of raw) {
    const last = merged[merged.length - 1];
    if (last && iv[0] <= last[1] + 0.05) last[1] = Math.max(last[1], iv[1]);
    else merged.push([...iv]);
  }
  return merged;
})();
const splitAt = (t: number) => {
  let v = 0;
  for (const [a, b] of intervals) {
    const x = Math.min(interpolate(t, [a - RAMP / 2, a + RAMP / 2], [0, 1], clamp),
                       interpolate(t, [b - RAMP / 2, b + RAMP / 2], [1, 0], clamp));
    v = Math.max(v, x);
  }
  // ease in-out
  return v * v * (3 - 2 * v);
};

// ---------- face (one continuous joined file) ----------
const FaceLayer: React.FC = () => {
  const frame = useCurrentFrame();
  const s = splitAt(frame / fps);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: SEAM * s, bottom: 0, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 0, top: -FACE_SHIFT * s, width: 1080, height: 1920 }}>
        <Clip src={staticFile("th/track.mp4")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
    </div>
  );
};

const Face: React.FC = () => (
  <Sequence from={0} durationInFrames={f(timeline.endCardStart)}>
    <FaceLayer />
  </Sequence>
);

// Rough cut only: the takes in order, nothing on top. For approving the cut.
export const RoughCut: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Sequence from={0} durationInFrames={f(timeline.endCardStart)}>
      <Clip src={staticFile("th/track.mp4")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    </Sequence>
  </AbsoluteFill>
);

// ---------- top-half B-roll ----------
type Broll = { start: number; dur: number; src: string; from: number; pos: string; zoom: number; origin: string };

const TopHalf: React.FC<{ b: Broll }> = ({ b }) => {
  const frame = useCurrentFrame();
  const s = splitAt(b.start + frame / fps);
  const drift = interpolate(frame, [0, f(b.dur)], [1.0, 1.05]);
  return (
    <div style={{
      position: "absolute", left: 0, right: 0, top: 0, height: SEAM, overflow: "hidden",
      transform: `translateY(${-(1 - s) * SEAM}px)`, backgroundColor: INK,
    }}>
      {b.src.startsWith("panel:") ? <GlobePanel dur={b.dur} /> : b.src.startsWith("image:") ? (
        <Img src={staticFile(b.src.slice(6))}
          style={{ width: "100%", height: "100%", objectFit: "cover", transformOrigin: b.origin,
                   transform: `scale(${interpolate(frame, [0, f(b.dur)], [1.0, b.zoom], clamp)})` }} />
      ) : (
        <Clip src={staticFile(b.src)} startFrom={f(b.from)} muted
          style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: b.pos,
                   transformOrigin: b.origin, transform: `scale(${b.zoom * drift})` }} />
      )}
    </div>
  );
};

// Full-screen B-roll, for sections recorded as voice only.
const FullScreen: React.FC<{ b: Broll }> = ({ b }) => {
  const frame = useCurrentFrame();
  const total = f(b.dur);
  const o = Math.min(interpolate(frame, [0, 5], [0, 1], clamp), interpolate(frame, [total - 5, total], [1, 0], clamp));
  return (
    <AbsoluteFill style={{ opacity: o, backgroundColor: INK }}>
      <Clip src={staticFile(b.src.slice(5))} startFrom={f(b.from)} muted
        style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: b.pos }} />
    </AbsoluteFill>
  );
};

// ---------- graphics ----------
const out = (frame: number, dur: number) => interpolate(frame, [f(dur) - 6, f(dur)], [1, 0], clamp);
// Graphics sit on the seam while split, otherwise on the chest (never on the face).
const inFull = (t: number) => timeline.broll.some((b) => b.src.startsWith("full:") && t >= b.start && t < b.start + b.dur);
const anchorY = (start: number) => (inFull(start + 0.3) ? 1250 : splitAt(start + 0.3) > 0.5 ? SEAM : 1150);

const Hook: React.FC<{ text: string; dur: number }> = ({ text, dur }) => {
  const frame = useCurrentFrame();
  const s = spring({ frame, fps, config: { damping: 11, stiffness: 160 } });
  return (
    <AbsoluteFill style={{ alignItems: "center", opacity: out(frame, dur) }}>
      <div style={{
        position: "absolute", top: 110, transform: `scale(${s}) rotate(-2deg)`,
        backgroundColor: LIME, color: INK, fontFamily, fontWeight: 900, fontSize: 84,
        padding: "18px 40px", borderRadius: 22, boxShadow: "0 18px 40px rgba(0,0,0,0.35)",
      }}>{text}</div>
    </AbsoluteFill>
  );
};

const Label: React.FC<{ text: string; dur: number; y: number; color: string }> = ({ text, dur, y, color }) => {
  const frame = useCurrentFrame();
  const s = spring({ frame, fps, config: { damping: 12, stiffness: 180 } });
  return (
    <AbsoluteFill style={{ alignItems: "center", opacity: out(frame, dur) }}>
      <div style={{
        position: "absolute", top: y, transform: `translateY(-50%) scale(${s})`,
        backgroundColor: color, color: "white", fontFamily, fontWeight: 900, fontSize: text.length > 22 ? 42 : 56,
        padding: "14px 30px", borderRadius: 18, boxShadow: "0 14px 34px rgba(0,0,0,0.4)",
        textAlign: "center", maxWidth: 1000, whiteSpace: "nowrap",
      }}>{text}</div>
    </AbsoluteFill>
  );
};

const Chips: React.FC<{ text: string; dur: number; y: number }> = ({ text, dur, y }) => {
  const frame = useCurrentFrame();
  const [a, b] = text.split("|");
  const s1 = spring({ frame, fps, config: { damping: 14 } });
  const s2 = spring({ frame: frame - 8, fps, config: { damping: 14 } });
  const chip = (bg: string, fg: string): React.CSSProperties => ({
    backgroundColor: bg, color: fg, fontFamily, fontWeight: 900, fontSize: 48, padding: "14px 26px", borderRadius: 18,
    boxShadow: "0 14px 34px rgba(0,0,0,0.4)", whiteSpace: "nowrap",
  });
  return (
    <AbsoluteFill style={{ alignItems: "center", opacity: out(frame, dur) }}>
      <div style={{ position: "absolute", top: y, transform: "translateY(-50%)", display: "flex", gap: 16 }}>
        <div style={{ ...chip(ORANGE, "white"), transform: `translateX(${(1 - s1) * -700}px)` }}>{a}</div>
        <div style={{ ...chip(LIME, INK), transform: `translateX(${(1 - s2) * 700}px)` }}>{b}</div>
      </div>
    </AbsoluteFill>
  );
};

const Quote: React.FC<{ text: string; dur: number; y: number }> = ({ text, dur, y }) => {
  const frame = useCurrentFrame();
  const s = spring({ frame, fps, config: { damping: 13, stiffness: 170 } });
  return (
    <AbsoluteFill style={{ alignItems: "center", opacity: out(frame, dur) }}>
      <div style={{
        position: "absolute", top: y, transform: `translateY(-50%) scale(${s}) rotate(-1.5deg)`,
        backgroundColor: "white", color: INK, fontFamily, borderRadius: 22, padding: "18px 38px 16px",
        boxShadow: "0 16px 40px rgba(0,0,0,0.4)", textAlign: "center",
      }}>
        <div style={{ fontSize: 60, fontWeight: 900 }}>
          <span style={{ color: PINK }}>“</span>{text}<span style={{ color: PINK }}>”</span>
        </div>
        <div style={{ fontSize: 30, fontWeight: 700, color: PURPLE, marginTop: 4 }}>my unit chair</div>
      </div>
    </AbsoluteFill>
  );
};

const Wifi: React.FC<{ dur: number; y: number }> = ({ dur, y }) => {
  const frame = useCurrentFrame();
  const s = spring({ frame, fps, config: { damping: 12, stiffness: 180 } });
  const cross = interpolate(frame, [12, 24], [0, 1], clamp);
  const len = 260;
  return (
    <AbsoluteFill style={{ alignItems: "center", opacity: out(frame, dur) }}>
      <div style={{
        position: "absolute", top: y, transform: `translateY(-50%) scale(${s})`,
        width: 230, height: 230, borderRadius: 40, backgroundColor: PURPLE,
        boxShadow: "0 16px 40px rgba(0,0,0,0.4)", display: "flex", alignItems: "center", justifyContent: "center",
      }}>
        <svg width="170" height="170" viewBox="0 0 100 100">
          <g fill="none" stroke="white" strokeWidth="8" strokeLinecap="round">
            <path d="M14 42 A50 50 0 0 1 86 42" />
            <path d="M27 56 A32 32 0 0 1 73 56" />
            <path d="M40 70 A14 14 0 0 1 60 70" />
          </g>
          <circle cx="50" cy="82" r="6" fill="white" />
          <line x1="12" y1="12" x2="88" y2="88" stroke={PINK} strokeWidth="11" strokeLinecap="round"
            strokeDasharray={len} strokeDashoffset={len * (1 - cross)} />
        </svg>
      </div>
    </AbsoluteFill>
  );
};

const Batteries: React.FC<{ text: string; dur: number }> = ({ text, dur }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ alignItems: "center", opacity: out(frame, dur) }}>
      <div style={{ position: "absolute", top: 1080, display: "flex", gap: 34, alignItems: "flex-end", transform: "scale(0.8)" }}>
        {[0, 1, 2, 3].map((i) => {
          const s = spring({ frame: frame - i * 4, fps, config: { damping: 9, stiffness: 220 } });
          const bob = Math.sin((frame + i * 9) / 7) * 6;
          return (
            <div key={i} style={{ transform: `translateY(${bob}px) scale(${s}) rotate(${(i - 1.5) * 6}deg)`, textAlign: "center" }}>
              <div style={{ width: 44, height: 18, margin: "0 auto", backgroundColor: "#222", borderRadius: "8px 8px 0 0" }} />
              <div style={{ width: 130, height: 230, border: "10px solid #222", borderRadius: 22, backgroundColor: "white", position: "relative", overflow: "hidden" }}>
                <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: "90%", backgroundColor: LIME }} />
                <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily, fontWeight: 900, fontSize: 40, color: INK }}>{text}</div>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const NameTag: React.FC<{ text: string; dur: number }> = ({ text, dur }) => {
  const frame = useCurrentFrame();
  const [name, role] = text.split("|");
  const s = spring({ frame, fps, config: { damping: 18 }, durationInFrames: 16 });
  return (
    <div style={{ position: "absolute", left: 60, top: 1130, opacity: out(frame, dur), transform: `translateX(${(1 - s) * -800}px)` }}>
      <div style={{ display: "inline-block", backgroundColor: "white", color: INK, fontFamily, fontWeight: 900, fontSize: 64, padding: "10px 26px", borderRadius: "16px 16px 16px 0" }}>{name}</div>
      <br />
      <div style={{ display: "inline-block", backgroundColor: PURPLE, color: "white", fontFamily, fontWeight: 700, fontSize: 34, padding: "10px 24px", borderRadius: "0 0 16px 16px" }}>{role}</div>
    </div>
  );
};

// Family on a laptop, a dotted line across the world, to Abi.
const GlobePanel: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const draw = interpolate(frame, [10, 55], [0, 1], clamp);
  const heart = interpolate(frame, [30, 80], [0, 1], clamp);
  const pop = (d: number) => spring({ frame: frame - d, fps, config: { damping: 12, stiffness: 170 } });
  const path = "M 230 560 C 380 220, 700 220, 850 560";
  // point on the cubic curve for the travelling heart
  const P = (t: number) => {
    const x = (1 - t) ** 3 * 230 + 3 * (1 - t) ** 2 * t * 380 + 3 * (1 - t) * t ** 2 * 700 + t ** 3 * 850;
    const y = (1 - t) ** 3 * 560 + 3 * (1 - t) ** 2 * t * 220 + 3 * (1 - t) * t ** 2 * 220 + t ** 3 * 560;
    return [x, y];
  };
  const [hx, hy] = P(heart);
  return (
    <AbsoluteFill style={{ background: `linear-gradient(160deg, ${PURPLE} 0%, ${PINK} 100%)` }}>
      <svg width="1080" height="960" viewBox="0 0 1080 960">
        {/* globe */}
        <g opacity={pop(0)} transform={`translate(540 600) scale(${pop(0)})`}>
          <circle r="150" fill="none" stroke="rgba(255,255,255,0.35)" strokeWidth="6" />
          <ellipse rx="60" ry="150" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="5" />
          <line x1="-150" y1="0" x2="150" y2="0" stroke="rgba(255,255,255,0.3)" strokeWidth="5" />
          <path d="M -130 -75 Q 0 -60 130 -75 M -130 75 Q 0 60 130 75" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="5" />
        </g>
        {/* dotted line */}
        <path d={path} fill="none" stroke="white" strokeWidth="8" strokeLinecap="round" strokeDasharray="2 22"
          pathLength={1000} style={{ clipPath: `inset(0 ${(1 - draw) * 100}% 0 0)` }} />
        {/* laptop: family */}
        <g transform={`translate(230 600) scale(${pop(4)})`}>
          <rect x="-95" y="-80" width="190" height="125" rx="14" fill="white" />
          <rect x="-80" y="-66" width="160" height="97" rx="6" fill={LIME} />
          <circle cx="0" cy="-30" r="20" fill={INK} />
          <path d="M -32 22 Q 0 -14 32 22 Z" fill={INK} />
          <rect x="-120" y="45" width="240" height="18" rx="9" fill="white" />
        </g>
        {/* Abi-style robot */}
        <g transform={`translate(850 590) scale(${pop(10)})`}>
          <rect x="-60" y="-110" width="120" height="90" rx="28" fill={ORANGE} />
          <rect x="-44" y="-94" width="88" height="56" rx="16" fill={INK} />
          <circle cx="-18" cy="-66" r="9" fill="white" />
          <circle cx="18" cy="-66" r="9" fill="white" />
          <rect x="-46" y="-12" width="92" height="100" rx="20" fill={LIME} />
          <rect x="-76" y="0" width="22" height="70" rx="11" fill={PURPLE} />
          <rect x="54" y="0" width="22" height="70" rx="11" fill={PURPLE} />
        </g>
        {/* travelling heart */}
        {heart > 0 && heart < 1 && (
          <path transform={`translate(${hx} ${hy}) scale(1.6)`} d="M0 8 C -14 -2, -10 -16, 0 -8 C 10 -16, 14 -2, 0 8 Z" fill="white" />
        )}
        {/* labels */}
        <text x="230" y="740" textAnchor="middle" fontFamily={fontFamily} fontWeight={900} fontSize="44" fill="white" opacity={pop(14)}>FAMILY</text>
        <text x="230" y="790" textAnchor="middle" fontFamily={fontFamily} fontWeight={700} fontSize="30" fill="white" opacity={pop(16)}>anywhere in the world</text>
        <text x="850" y="740" textAnchor="middle" fontFamily={fontFamily} fontWeight={900} fontSize="44" fill="white" opacity={pop(18)}>ABI</text>
        <text x="850" y="790" textAnchor="middle" fontFamily={fontFamily} fontWeight={700} fontSize="30" fill="white" opacity={pop(20)}>with their grandparent</text>
        <text x="540" y="170" textAnchor="middle" fontFamily={fontFamily} fontWeight={900} fontSize="58" fill="white" opacity={pop(6)}>WHAT IF…</text>
      </svg>
    </AbsoluteFill>
  );
};

type G = { type: string; start: number; dur: number; text: string };
const Graphic: React.FC<{ g: G; i: number }> = ({ g, i }) => {
  const y = anchorY(g.start);
  if (g.type === "hook") return <Hook text={g.text} dur={g.dur} />;
  if (g.type === "label") return <Label text={g.text} dur={g.dur} y={y} color={[ORANGE, PURPLE, PINK][i % 3]} />;
  if (g.type === "chips") return <Chips text={g.text} dur={g.dur} y={y} />;
  if (g.type === "quote") return <Quote text={g.text} dur={g.dur} y={y} />;
  if (g.type === "wifi") return <Wifi dur={g.dur} y={y} />;
  if (g.type === "batteries") return <Batteries text={g.text} dur={g.dur} />;
  if (g.type === "nametag") return <NameTag text={g.text} dur={g.dur} />;
  return null;
};

// ---------- section tag (top left) ----------
const SectionTag: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const x = spring({ frame, fps, config: { damping: 18 }, durationInFrames: 14 });
  const o = interpolate(frame, [f(2.0), f(2.4)], [1, 0], clamp);
  return (
    <div style={{
      position: "absolute", top: 120, left: 60, opacity: o, transform: `translateX(${(1 - x) * -500}px)`,
      backgroundColor: LIME, color: INK, fontFamily, fontWeight: 900, fontSize: 44,
      padding: "12px 26px", borderRadius: 999, letterSpacing: 2,
    }}>{text}</div>
  );
};

// ---------- captions (switched on in the captions stage) ----------
type Word = { text: string; start: number; end: number; section: string };
type Chunk = { words: Word[]; start: number; end: number };
const chunks: Chunk[] = (() => {
  const res: Chunk[] = [];
  let cur: Word[] = [];
  const words = timeline.words as Word[];
  words.forEach((w, i) => {
    cur.push(w);
    const next = words[i + 1];
    const punct = /[.,?!]$/.test(w.text);
    const gap = next ? next.start - w.end > 0.25 || next.section !== w.section : true;
    if (cur.length >= 3 || punct || gap) {
      res.push({ words: cur, start: cur[0].start, end: next && next.section === w.section ? Math.min(next.start, w.end + 0.4) : w.end + 0.2 });
      cur = [];
    }
  });
  return res;
})();

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / fps;
  if (t >= timeline.endCardStart) return null;
  const c = chunks.find((k) => t >= k.start - 0.05 && t < k.end);
  if (!c) return null;
  const pop = spring({ frame: frame - f(c.start - 0.05), fps, config: { damping: 12, stiffness: 220 }, durationInFrames: 10 });
  // Face full screen: on the chest. Split screen: face is lower, so captions drop to the bottom.
  const y = inFull(t) ? 1560 : interpolate(splitAt(t), [0, 1], [1420, 1690]);
  return (
    <AbsoluteFill style={{ alignItems: "center" }}>
      <div style={{ position: "absolute", top: y, maxWidth: 940, textAlign: "center", transform: `scale(${0.8 + 0.2 * pop})` }}>
        <span style={{
          backgroundColor: PINK, color: "white", fontFamily, fontWeight: 800, fontSize: 62, lineHeight: 1.35,
          padding: "6px 22px", borderRadius: 14, boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone",
          textTransform: "uppercase",
        }}>
          {c.words.map((w, i) => (
            <span key={i} style={{ color: t >= w.start - 0.03 && t < w.end + 0.05 ? LIME : "white" }}>
              {w.text}{i < c.words.length - 1 ? " " : ""}
            </span>
          ))}
        </span>
      </div>
    </AbsoluteFill>
  );
};

// ---------- end card ----------
const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const fade = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: "clamp" });
  const line = (d: number) => spring({ frame: frame - d, fps, config: { damping: 16 } });
  const row = (d: number): React.CSSProperties => ({ opacity: line(d), transform: `translateY(${(1 - line(d)) * 40}px)` });
  return (
    <AbsoluteFill style={{
      opacity: fade, background: `linear-gradient(160deg, ${PURPLE} 0%, ${PINK} 100%)`,
      justifyContent: "center", alignItems: "center", fontFamily, color: "white", textAlign: "center",
    }}>
      <div style={{ ...row(4), fontSize: 110, fontWeight: 900, lineHeight: 1 }}>Manit Khera</div>
      <div style={{ ...row(10), fontSize: 40, fontWeight: 600, marginTop: 24 }}>Software Engineering student · Deakin University</div>
      <div style={{ ...row(18), marginTop: 70, display: "inline-block", backgroundColor: LIME, color: INK, fontSize: 44, fontWeight: 800, padding: "14px 30px", borderRadius: 16 }}>manitkhera26@gmail.com</div>
      <div style={{ ...row(24), marginTop: 26, fontSize: 38, fontWeight: 700 }}>linkedin.com/in/manit-khera-603957252</div>
      <div style={{ ...row(34), marginTop: 110, fontSize: 52, fontWeight: 800 }}>Thanks for watching</div>
    </AbsoluteFill>
  );
};

export const IntroVideo: React.FC = () => {
  const { durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: INK }}>
      <Face />
      {(timeline.broll as Broll[]).map((b, i) => (
        <Sequence key={`b${i}`} from={f(b.start)} durationInFrames={Math.max(1, f(b.dur))} premountFor={30}>
          {b.src.startsWith("full:") ? <FullScreen b={b} /> : <TopHalf b={b} />}
        </Sequence>
      ))}
      {timeline.sections.filter((s) => s.tag).map((s) => (
        <Sequence key={`t${s.id}`} from={f(s.start)} durationInFrames={f(2.4)}>
          <SectionTag text={s.tag as string} />
        </Sequence>
      ))}
      {(timeline.graphics as G[]).map((g, i) => (
        <Sequence key={`g${i}`} from={f(g.start)} durationInFrames={Math.max(1, f(g.dur))}>
          <Graphic g={g} i={i} />
        </Sequence>
      ))}
      {timeline.captions && <Captions />}
      <Sequence from={f(timeline.endCardStart)}>
        <EndCard />
      </Sequence>
      {timeline.music && (() => {
        const m = timeline.music as { src: string; offset: number; base: number; duck: number; duckStart: number; duckEnd: number; endLift: number };
        const E = timeline.endCardStart;
        return (
          <Audio src={staticFile(m.src)} startFrom={f(m.offset)}
            volume={(fr) => {
              const t = fr / fps;
              const total = durationInFrames / fps;
              let v = m.base;
              // duck under the grandfather section, then come back with the track's own re-entry
              v *= interpolate(t, [m.duckStart - 0.8, m.duckStart, m.duckEnd - 0.4, m.duckEnd + 0.3], [1, m.duck / m.base, m.duck / m.base, 1], clamp);
              // lift a little on the end card, fade in at the start and out at the very end
              v = interpolate(t, [E - 0.5, E + 0.5], [v, m.endLift], clamp);
              v *= interpolate(t, [0, 1.0], [0, 1], clamp) * interpolate(t, [total - 1.8, total], [1, 0], clamp);
              return v;
            }} />
        );
      })()}
    </AbsoluteFill>
  );
};
