// One-off gags for the Infosys video (plain white-line / meme style, same as the kit):
//  1. Tennis scoreboard in the top-right corner (0-0, 15-0, 30-0, 30-40, GAME). GAME, SET, MATCH is the end card title.
//  2. "API" / "ROBOT" labels riding his fists, smacking together on "made them meet".
//  3. MatchFeel: a drawn court (white lines, black outline) with a ball and ring tracing a rally.
// t = seconds in the cut; W = resolved plan anchors by name; face(t) = [x, y, width] of his face (1080x1920).
import React from "react";
import { AbsoluteFill, Easing, interpolate } from "remotion";
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";

const { fontFamily: ANTON } = loadAnton();
const FPS = 30;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const meme = (size: number, stroke = Math.round(size / 9)): React.CSSProperties => ({
  fontFamily: ANTON, fontSize: size, color: "#FFFFFF", lineHeight: 1.05, letterSpacing: 1,
  WebkitTextStroke: `${stroke}px #000`, paintOrder: "stroke fill", textTransform: "uppercase", whiteSpace: "nowrap",
});
// hard cut in with a 2-frame punch, no spring
const punch = (t: number, t0: number) => (t - t0 < 1 / FPS ? 1.18 : t - t0 < 2 / FPS ? 1.06 : 1);

type Props = { t: number; W: Record<string, number>; face: (t: number) => number[] };

// ---------- 1. scoreboard ----------
const Score: React.FC<Props> = ({ t, W }) => {
  const steps: [number, string][] = (
    [[W.okay ?? 0, "0-0"], [W.score15, "15-0"], [W.smack, "30-0"], [W.right, "30-40"], [W.game, "GAME"]] as [number, string][]
  ).filter((s) => typeof s[0] === "number");
  const end = W.court ?? Infinity;
  if (!steps.length || t < steps[0][0] || t >= end) return null;
  let cur = steps[0];
  for (const s of steps) if (t >= s[0]) cur = s;
  return (
    <div style={{ position: "absolute", top: 70, right: 50, transformOrigin: "100% 0",
      transform: `rotate(3deg) scale(${punch(t, cur[0])})` }}>
      <div style={meme(cur[1] === "GAME" ? 96 : 84)}>{cur[1]}</div>
    </div>
  );
};

// ---------- 2. API / ROBOT labels on his fists ----------
const Tag: React.FC<{ x: number; y: number; txt: string; rot: number; sc: number }> = ({ x, y, txt, rot, sc }) => (
  <div style={{ position: "absolute", left: x, top: y, transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${sc})` }}>
    <div style={meme(120)}>{txt}</div>
  </div>
);

const Labels: React.FC<Props> = ({ t, W, face }) => {
  if (W.api === undefined || W.handsup === undefined || t < W.api || t >= W.handsup) return null;
  const slide = W.slide ?? W.smack - 0.15;
  const k = interpolate(t, [slide, W.smack], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const sway = (face(t)[0] - 540) * 0.5 * (1 - k); // fists move with his body until they meet
  const hit = t >= W.smack;
  const y = 1430;
  const apiX = 880 + (690 - 880) * k + sway;   // his fist on the frame's right ("API", he looks right)
  const robX = Math.max(175, 290 + (395 - 290) * k + sway);  // his fist on the frame's left ("ROBOT", he looks left)
  return (
    <>
      <Tag x={apiX} y={y} txt="API" rot={hit ? -7 : 4} sc={hit ? punch(t, W.smack) : punch(t, W.api)} />
      {t >= W.robot && <Tag x={robX} y={y} txt="ROBOT" rot={hit ? 6 : -4} sc={hit ? punch(t, W.smack) : punch(t, W.robot)} />}
    </>
  );
};

// ---------- 3. MatchFeel court + ball tracing a rally ----------
const CX = 540, CY = 355, CW = 600, CH = 277;           // top-down court, doubles ratio ~2.17:1
const L = CX - CW / 2, R = CX + CW / 2, T = CY - CH / 2, B = CY + CH / 2;
const IN = (CH * 1.37) / 10.97;                          // singles sideline inset
const SV = ((CW / 2) * 6.4) / 11.885;                    // service line distance from the net
const LINES: number[][] = [
  [L, T, R, T], [L, B, R, B], [L, T, L, B], [R, T, R, B],
  [L, T + IN, R, T + IN], [L, B - IN, R, B - IN],
  [CX - SV, T + IN, CX - SV, B - IN], [CX + SV, T + IN, CX + SV, B - IN],
  [CX - SV, CY, CX + SV, CY],
];
const PATH: number[][] = [
  [L + 60, T + 60], [R - 70, B - 60], [L + 80, B - 50], [R - 60, T + 70], [L + 70, CY], [R - 80, CY + 40], [L + 90, T + 50],
];
const LEG = 0.85; // seconds per shot; plan has a thock at each landing (court + 0.85 k)

const Court: React.FC<Props> = ({ t, W }) => {
  if (W.court === undefined || W.court_end === undefined || t < W.court || t >= W.court_end) return null;
  const u = t - W.court;
  const i = Math.min(Math.floor(u / LEG), PATH.length - 2);
  const f = Math.min(1, (u - i * LEG) / LEG);
  const [ax, ay] = PATH[i], [bx, by] = PATH[i + 1];
  const x = ax + (bx - ax) * f, y = ay + (by - ay) * f;
  const r = 13 + 5 * Math.sin(Math.PI * f); // a touch bigger mid-air
  return (
    <AbsoluteFill>
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        {LINES.map((l, k) => <line key={`b${k}`} x1={l[0]} y1={l[1]} x2={l[2]} y2={l[3]} stroke="#000" strokeWidth={16} strokeLinecap="round" />)}
        <line x1={CX} y1={T - 18} x2={CX} y2={B + 18} stroke="#000" strokeWidth={20} strokeLinecap="round" />
        {LINES.map((l, k) => <line key={`w${k}`} x1={l[0]} y1={l[1]} x2={l[2]} y2={l[3]} stroke="#fff" strokeWidth={8} strokeLinecap="round" />)}
        <line x1={CX} y1={T - 18} x2={CX} y2={B + 18} stroke="#fff" strokeWidth={10} strokeLinecap="round" strokeDasharray="4 10" />
        {/* trail of this shot */}
        <line x1={ax} y1={ay} x2={x} y2={y} stroke="#000" strokeWidth={10} strokeLinecap="round" opacity={0.6} />
        <line x1={ax} y1={ay} x2={x} y2={y} stroke="#fff" strokeWidth={5} strokeLinecap="round" strokeDasharray="10 12" opacity={0.85} />
        {/* the ring that traces the ball */}
        <circle cx={x} cy={y} r={32} fill="none" stroke="#000" strokeWidth={12} />
        <circle cx={x} cy={y} r={32} fill="none" stroke="#fff" strokeWidth={6} />
        {/* ball */}
        <circle cx={x} cy={y} r={r} fill="#FFE11A" stroke="#000" strokeWidth={5} />
      </svg>
    </AbsoluteFill>
  );
};

export const Custom: React.FC<Props> = (p) => (
  <AbsoluteFill>
    <Score {...p} />
    <Labels {...p} />
    <Court {...p} />
  </AbsoluteFill>
);
