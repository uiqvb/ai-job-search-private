// One-off gags for the Affinda video. Plain, human-made style (EDITING-STYLE.md): white Anton text with a
// black outline, red marker ticks, real photo cut-outs (bin, robot), props drawn in plain colours.
// No Affinda colours or logo. Drawn above the video, under the plan's meme text, captions and name tag.
//  1. 2:00 countdown top-right: real seconds from "two minutes", freezes on "works" (blinks).
//  2. Reel: WAM 81 / 100/100 BACKEND / 100/100 DSA fly off the resume into a column (top-left).
//  3. Speed lines behind the plan text "6X FASTER".
//  4. The toss: camera whips up to a bin on the wall, the paper ball drops in, the bin explodes (0.7 s).
//  5. The bin smokes in the bottom-left corner from then on (the bin itself is a plan sticker).
//  6. Checklist top-left: GREAT IDEAS / CURIOUS / ENERGY, red marker ticks.
//  7. Fist labels: API (BACKEND DEVELOPMENT) and ROBOT (EMBEDDED SYSTEMS) typed out, smack together on "made".
//  8. Glitch on "broke": only he glitches (the blue wall is keyed out with an SVG colour matrix).
//  9. "ENERGY?" pops letter by letter, the question mark last.
// 10. Claude Code terminal: the video shrinks, the real /video cut steps run above it.
// 11. Prompt Wrappers: the "Simple English" toggle in his mock-up flicks on with his flick.
// 12. Capsule: campus map doodle on the wall, pins with padlocks, footsteps walk up, the padlock opens.
// 13. Paper stack "DONE BY HAND" gets sucked into a plain laptop that says DONE.
// 14. End: the paper ball shoots out of the bin and unfolds into the end card.
// t = seconds in the cut; W = resolved plan anchors by name; face(t) = [x, y, width] of his face.
import React from "react";
import { AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, random, staticFile } from "remotion";
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";
import { loadFont as loadMont } from "@remotion/google-fonts/Montserrat";

const { fontFamily: ANTON } = loadAnton("normal", { weights: ["400"], subsets: ["latin"] });
const { fontFamily: MONO } = loadMono("normal", { weights: ["400", "700", "800"], subsets: ["latin"] });
const { fontFamily: MONT } = loadMont("normal", { weights: ["600", "800"], subsets: ["latin"] });

const FPS = 30;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp = (t: number, a: number[], b: number[], ease?: (x: number) => number) => interpolate(t, a, b, { ...clamp, easing: ease });
// hard cut in with a 2-frame punch, no spring
const punch = (t: number, t0: number) => (t - t0 < 1 / FPS ? 1.18 : t - t0 < 2 / FPS ? 1.06 : 1);
const meme = (size: number, stroke = Math.round(size / 9)): React.CSSProperties => ({
  fontFamily: ANTON, fontSize: size, color: "#FFFFFF", lineHeight: 1.05, letterSpacing: 1,
  WebkitTextStroke: `${stroke}px #000`, paintOrder: "stroke fill", textTransform: "uppercase", whiteSpace: "nowrap",
});

type Props = { t: number; W: Record<string, number>; face: (t: number) => number[] };
const has = (W: Record<string, number>, ...k: string[]) => k.every((x) => typeof W[x] === "number");
const RED = "#E8231B";
const TRACK = "th/track.mp4";
const BIN_IMG = "lib/editor-template/syncrowin-style/public/img/bin.png"; // copied by build_plan (plan sticker)
const MOUTH: [number, number] = [116, 1715]; // mouth of the corner bin sticker (plan: x 150, y 1790, width 300)

// ---------- crumpled paper ball, drawn plain ----------
const Ball: React.FC<{ x: number; y: number; r: number; rot: number }> = ({ x, y, r, rot }) => {
  const pts = Array.from({ length: 11 }).map((_, i) => {
    const a = (i / 11) * Math.PI * 2, rr = r * (0.8 + 0.25 * random(`pb${i}`));
    return `${(Math.cos(a) * rr).toFixed(1)},${(Math.sin(a) * rr).toFixed(1)}`;
  }).join(" ");
  return (
    <svg width={r * 3} height={r * 3} style={{ position: "absolute", left: x - r * 1.5, top: y - r * 1.5, overflow: "visible" }}>
      <g transform={`translate(${r * 1.5} ${r * 1.5}) rotate(${rot})`}>
        <polygon points={pts} fill="#F4F4F2" stroke="#000" strokeWidth={Math.max(3, r / 9)} strokeLinejoin="round" />
        <path d={`M ${-r * 0.5} ${-r * 0.2} L ${-r * 0.1} ${r * 0.1} L ${r * 0.3} ${-r * 0.3} M ${-r * 0.3} ${r * 0.45} L ${r * 0.15} ${r * 0.2} L ${r * 0.5} ${r * 0.4}`}
          fill="none" stroke="#9A9A9A" strokeWidth={Math.max(2, r / 14)} strokeLinecap="round" />
      </g>
    </svg>
  );
};

// ======================================================================
// 1. Countdown (real seconds; he finishes with time to spare)
// ======================================================================
const Timer: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "two", "minutes_e", "works_e", "card", "term_in", "term_out")) return null;
  if (t < W.two || t >= W.card || (t >= W.term_in && t < W.term_out)) return null;
  const tt = Math.min(t, W.works_e);
  const secs = Math.ceil(120 - Math.max(0, tt - W.minutes_e) - 1e-6);
  const frozen = t >= W.works_e;
  const blink = frozen && t < W.works_e + 0.6 && Math.floor((t - W.works_e) * 10) % 2 === 1;
  return (
    <div style={{ position: "absolute", right: 46, top: 40, fontFamily: MONO, fontWeight: 800, fontSize: 84, color: "#fff",
      WebkitTextStroke: "14px #000", paintOrder: "stroke fill", opacity: blink ? 0 : 1, transformOrigin: "100% 0",
      transform: `scale(${punch(t, frozen ? W.works_e : W.two)})` }}>
      {`${Math.floor(secs / 60)}:${String(secs % 60).padStart(2, "0")}`}
    </div>
  );
};

// ======================================================================
// 2. Reel: achievements fly off the resume (held at the viewer left) into a column
// ======================================================================
type ReelItem = { k: string; from: [number, number]; to: [number, number]; big: string; sub?: string; size: number; rot: number };
const REEL: ReelItem[] = [
  { k: "wam", from: [90, 1160], to: [290, 230], big: "WAM 81", size: 120, rot: -6 }, // camera zoomed in here: resume at the left edge
  { k: "hundred1", from: [300, 1180], to: [290, 420], big: "100/100", sub: "BACKEND", size: 110, rot: 4 },
  { k: "dsa", from: [300, 1180], to: [290, 615], big: "100/100", sub: "DSA", size: 110, rot: -3 },
];
const FLY = 0.16;
const Reel: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "wam", "hundred1", "dsa", "openday1_e") || t < W.wam || t >= W.openday1_e) return null;
  const draw = (it: ReelItem, tt: number, op: number, key: string) => {
    const t0 = W[it.k];
    const k = lerp(tt, [t0, t0 + FLY], [0, 1], Easing.out(Easing.cubic));
    const x = it.from[0] + (it.to[0] - it.from[0]) * k;
    const y = it.from[1] + (it.to[1] - it.from[1]) * k - Math.sin(Math.PI * k) * 120;
    const sc = (0.35 + 0.65 * k) * (tt >= t0 + FLY ? punch(tt, t0 + FLY) : 1);
    const rot = it.rot * k - 25 * (1 - k);
    return (
      <div key={key} style={{ position: "absolute", left: x, top: y, opacity: op, textAlign: "center", transform: `translate(-50%,-50%) scale(${sc}) rotate(${rot}deg)` }}>
        <div style={meme(it.size)}>{it.big}</div>
        {it.sub && <div style={{ ...meme(54), marginTop: -6 }}>{it.sub}</div>}
      </div>
    );
  };
  return (
    <AbsoluteFill>
      {REEL.map((it, i) => {
        const t0 = W[it.k];
        if (t < t0) return null;
        const flying = t < t0 + FLY;
        return (
          <React.Fragment key={i}>
            {flying && draw(it, t - 2 / FPS, 0.18, "g2")}
            {flying && draw(it, t - 1 / FPS, 0.35, "g1")}
            {draw(it, t, 1, "m")}
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};

// ======================================================================
// 3. Speed lines behind "6X FASTER" (plan text, top 200)
// ======================================================================
const Speed: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "six") || t < W.six || t >= W.six + 0.55) return null;
  const d = t - W.six;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
      {Array.from({ length: 9 }).map((_, i) => {
        const y = 190 + i * 24 + random(`sy${i}`) * 10;
        const len = 260 + random(`sl${i}`) * 300;
        const x = -len + ((d * (3200 + random(`sv${i}`) * 1600) + random(`so${i}`) * 400) % (1080 + len * 2));
        return (
          <g key={i} opacity={lerp(d, [0.35, 0.55], [1, 0])}>
            <line x1={x} y1={y} x2={x + len} y2={y} stroke="#000" strokeWidth={14} strokeLinecap="round" />
            <line x1={x} y1={y} x2={x + len} y2={y} stroke="#fff" strokeWidth={7} strokeLinecap="round" />
          </g>
        );
      })}
    </svg>
  );
};

// ======================================================================
// 4. The toss: whip pan up to a bin on the wall, ball drops in, bin explodes (held 0.7 s, then hard cut)
// ======================================================================
const BIN: [number, number] = [440, 1000]; // behind his left shoulder, where the real paper lands // where the bin hangs on the wall (video coords, above his raised hand)
const Explosion: React.FC<{ d: number; cx: number; cy: number }> = ({ d, cx, cy }) => {
  const grow = lerp(d, [0, 0.38], [0.25, 1], Easing.out(Easing.cubic));
  const fade = 1 - lerp(d, [0.32, 0.7], [0, 1]);
  const balls = [];
  for (let i = 0; i < 34; i++) {
    const a = random(`ba${i}`) * Math.PI * 2, dist = random(`bd${i}`) * 230 * grow;
    const r = (50 + random(`br${i}`) * 120) * grow;
    const hot = random(`bh${i}`) < 0.55;
    balls.push(<circle key={i} cx={cx + Math.cos(a) * dist} cy={cy + Math.sin(a) * dist * 0.8 - d * 220 * random(`bu${i}`)} r={r}
      fill={hot ? "url(#affHot)" : "url(#affSmoke)"} opacity={hot ? fade : Math.min(1, fade * 1.6) * 0.8} />);
  }
  const debris = [];
  for (let i = 0; i < 16; i++) {
    const a = random(`da${i}`) * Math.PI * 2, v = 700 + random(`dv${i}`) * 700;
    const x = cx + Math.cos(a) * v * d, y = cy + Math.sin(a) * v * d + 700 * d * d;
    debris.push(<rect key={i} x={x} y={y} width={14 + random(`dw${i}`) * 22} height={10 + random(`dh${i}`) * 14}
      transform={`rotate(${d * 900 * (random(`dr${i}`) - 0.5)} ${x} ${y})`} fill={i % 2 ? "#F4F4F2" : "#55555A"} stroke="#000" strokeWidth={2} />);
  }
  return (
    <>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0, filter: "blur(9px)" }}>
        <defs>
          <radialGradient id="affHot"><stop offset="0" stopColor="#FFF4C2" /><stop offset="0.35" stopColor="#FFB02E" /><stop offset="0.7" stopColor="#E8480F" stopOpacity="0.85" /><stop offset="1" stopColor="#5A1A08" stopOpacity="0" /></radialGradient>
          <radialGradient id="affSmoke"><stop offset="0" stopColor="#4A4440" /><stop offset="0.7" stopColor="#2E2A28" stopOpacity="0.8" /><stop offset="1" stopColor="#222" stopOpacity="0" /></radialGradient>
        </defs>
        {balls}
      </svg>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>{debris}</svg>
    </>
  );
};
// Camera keys while the paper flies: [seconds after "stuff" starts, focus x, focus y, scale]
const CAM: [number, number, number, number][] = [
  [0, 540, 960, 1.0], [0.35, 330, 930, 1.25], [1.1, 260, 880, 1.32], [1.35, 400, 900, 1.36], [1.6, 450, 990, 1.4],
];
const camAt = (u: number) => {
  for (let i = 1; i < CAM.length; i++) {
    if (u <= CAM[i][0]) {
      const a = CAM[i - 1], b = CAM[i], f = Easing.inOut(Easing.quad)((u - a[0]) / (b[0] - a[0]));
      return [a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f, a[3] + (b[3] - a[3]) * f];
    }
  }
  const z = CAM[CAM.length - 1];
  return [z[1], z[2], z[3]];
};
// "stuff": B&W, the camera follows his hand and the real paper to a bin behind his shoulder, the bin explodes.
const Whip: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "stuff_s", "land", "boom") || t < W.stuff_s || t >= W.boom + 0.55) return null;
  const [fx, fy, s] = camAt(t - W.stuff_s);
  let tx = 540 - s * fx, ty = 960 - s * fy;
  const d = t - W.boom;
  if (d >= 0) {
    const e = Math.exp(-d * 5) * 18;
    tx += Math.sin(d * 120) * e;
    ty += Math.cos(d * 97) * e;
  }
  tx = Math.min(0, Math.max(1080 - s * 1080, tx));
  ty = Math.min(0, Math.max(1920 - s * 1920, ty));
  const binIn = W.stuff_s + 0.9;
  const dl = t - W.land;
  const wob = dl > 0 && dl < 0.3 ? Math.sin(dl * 60) * 9 * Math.exp(-dl * 10) : 0;
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <AbsoluteFill style={{ transformOrigin: "0 0", transform: `translate(${tx}px, ${ty}px) scale(${s})` }}>
        <AbsoluteFill style={{ filter: "grayscale(1) contrast(1.15)" }}>
          <OffthreadVideo muted src={staticFile(TRACK)} />
        </AbsoluteFill>
        {t >= binIn && t < W.boom + 0.04 && (
          <Img src={staticFile(BIN_IMG)} style={{ position: "absolute", left: BIN[0], top: BIN[1], width: 210,
            transform: `translate(-50%,-50%) scale(${punch(t, binIn)}) rotate(${4 + wob}deg)` }} />
        )}
        {d >= 0 && <Explosion d={d} cx={BIN[0]} cy={BIN[1] - 20} />}
      </AbsoluteFill>
      {d >= 0 && d < 2 / FPS && <AbsoluteFill style={{ background: "#fff", opacity: 0.85 }} />}
    </AbsoluteFill>
  );
};

// 6000 robots: a counter runs up while little robots pop in across the top of the frame
const ROBOT_IMG = "lib/editor-template/syncrowin-style/public/img/robot_sticker.png";
const Army: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "n6000", "six") || t < W.n6000 || t >= W.six) return null;
  const n = Math.round(lerp(t, [W.n6000, W.n6000 + 0.7], [0, 6000], Easing.out(Easing.cubic)));
  const bots = [];
  for (let i = 0; i < 28; i++) {
    const t0 = W.n6000 + i * 0.035;
    if (t < t0) continue;
    const side = i % 2, x = side ? 830 + random(`ax${i}`) * 200 : 50 + random(`ax${i}`) * 200, y = 420 + random(`ay${i}`) * 820; // two side columns, clear of his face
    bots.push(<Img key={i} src={staticFile(ROBOT_IMG)} style={{ position: "absolute", left: x, top: y, width: 90 + random(`aw${i}`) * 50,
      transform: `translate(-50%,-50%) scale(${punch(t, t0)}) rotate(${(random(`ar${i}`) - 0.5) * 30}deg)` }} />);
  }
  return (
    <AbsoluteFill>
      {bots}
      <div style={{ position: "absolute", top: 210, left: 0, width: 1080, textAlign: "center", transform: `rotate(-4deg) scale(${punch(t, W.n6000)})` }}>
        <div style={meme(150)}>{n.toLocaleString("en-AU")} ROBOTS</div>
      </div>
    </AbsoluteFill>
  );
};

// Yellow shiny rays burst out of the robot when the labels meet
const Rays: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "made", "started") || t < W.made || t >= W.started) return null;
  const d = t - W.made, cx = 560, cy = 1440;
  const grow = lerp(d, [0, 0.25], [0.2, 1], Easing.out(Easing.cubic));
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
      <g transform={`rotate(${d * 40} ${cx} ${cy})`}>
        {Array.from({ length: 16 }).map((_, i) => {
          const a = (i / 16) * Math.PI * 2, r0 = 170 * grow, r1 = (330 + (i % 2) * 120) * grow * (1 + 0.06 * Math.sin(t * 20 + i));
          return <line key={i} x1={cx + Math.cos(a) * r0} y1={cy + Math.sin(a) * r0} x2={cx + Math.cos(a) * r1} y2={cy + Math.sin(a) * r1}
            stroke="#FFD43B" strokeWidth={i % 2 ? 10 : 18} strokeLinecap="round" opacity={0.9} style={{ filter: "drop-shadow(0 0 10px #FFE98A)" }} />;
        })}
      </g>
    </svg>
  );
};

// ======================================================================
// 5. Corner bin smokes (heavier right after the explosion, then a thin wisp)
// ======================================================================
const Smoke: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "i_had", "card") || t < W.i_had || t >= W.card + 0.3) return null;
  const age = t - W.i_had;
  const strength = (0.35 + 0.65 * Math.exp(-age / 5)) * Math.min(1, age * 3);
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0, filter: "blur(8px)" }}>
      {Array.from({ length: 7 }).map((_, i) => {
        const ph = (t * 0.45 + i / 7) % 1;
        return <circle key={i} cx={MOUTH[0] + Math.sin(ph * 5 + i) * 18 + ph * 40} cy={MOUTH[1] - ph * 330} r={16 + ph * 46}
          fill={i % 2 ? "#8A8A8A" : "#6E6E6E"} opacity={(1 - ph) * 0.55 * strength} />;
      })}
    </svg>
  );
};

// ======================================================================
// 6. Checklist top-left (on screen only; he never says the ad's words). Red marker ticks.
// ======================================================================
const ROWS = ["GREAT IDEAS", "CURIOUS", "ENERGY"];
const CX = 40, CY = [56, 124, 192], BOX = 48;
const MarkerTick: React.FC<{ t: number; t0: number; x: number; y: number }> = ({ t, t0, x, y }) => {
  const k = lerp(t, [t0, t0 + 0.2], [0, 1]);
  const d = `M ${x + 4} ${y + 22} L ${x + 20} ${y + 44} L ${x + 60} ${y - 16}`;
  const s = punch(t, t0 + 0.2);
  return (
    <g transform={`translate(${x + 24} ${y + 24}) scale(${s}) translate(${-(x + 24)} ${-(y + 24)})`}>
      <path d={d} fill="none" stroke="#000" strokeWidth={17} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} />
      <path d={d} fill="none" stroke={RED} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} />
    </g>
  );
};
const Checklist: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "i_had", "check_out", "meet_e", "worked", "tick3", "term_in", "term_out")) return null;
  if (t < W.i_had || t >= W.check_out || (t >= W.term_in && t < W.term_out)) return null;
  const ticks = [W.meet_e, W.worked, W.tick3];
  return (
    <AbsoluteFill>
      {ROWS.map((r, i) => {
        const t0 = W.i_had + i * 0.16;
        if (t < t0) return null;
        return (
          <div key={i} style={{ position: "absolute", left: CX, top: CY[i], display: "flex", alignItems: "center", transformOrigin: "0 50%",
            transform: `scale(${punch(t, t0)}) rotate(${i % 2 ? 1 : -1}deg)` }}>
            <div style={{ width: BOX, height: BOX, boxSizing: "border-box", border: "7px solid #fff", outline: "5px solid #000", boxShadow: "inset 0 0 0 4px #000" }} />
            <div style={{ ...meme(50, 7), marginLeft: 22 }}>{r}</div>
          </div>
        );
      })}
      <svg width={1080} height={400} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        {ticks.map((t0, i) => t >= t0 && <MarkerTick key={i} t={t} t0={t0} x={CX} y={CY[i]} />)}
      </svg>
    </AbsoluteFill>
  );
};

// ======================================================================
// 7. Fist labels (positions keyed to his fists in the wide frame; no camera move here)
// ======================================================================
type LKey = [number, number, number]; // [seconds relative to W.made, x, y]
const API_KEYS: LKey[] = [[-0.75, 860, 1390], [-0.36, 840, 1160], [0, 600, 1330]];
const ROBOT_KEYS: LKey[] = [[-0.75, 220, 1390], [-0.36, 250, 1160], [0, 500, 1330]];
const keyAt = (keys: LKey[], u: number): [number, number] => {
  if (u <= keys[0][0]) return [keys[0][1], keys[0][2]];
  for (let i = 1; i < keys.length; i++) {
    if (u <= keys[i][0]) {
      const a = keys[i - 1], b = keys[i], f = (u - a[0]) / (b[0] - a[0]);
      return [a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f];
    }
  }
  const z = keys[keys.length - 1];
  return [z[1], z[2]];
};
const FistLabel: React.FC<{ t: number; t0: number; made: number; keys: LKey[]; word: string; sub: string }> = ({ t, t0, made, keys, word, sub }) => {
  if (t < t0 || t >= made) return null;
  const [x, y] = keyAt(keys, t - made);
  const n = Math.floor(lerp(t, [t0 + 0.15, t0 + 0.15 + sub.length * 0.04], [0, sub.length]));
  const conv = lerp(t, [made - 0.36, made], [1, 0.6]);
  return (
    <div style={{ position: "absolute", left: x, top: y, textAlign: "center", transform: `translate(-50%,-50%) scale(${punch(t, t0) * conv}) rotate(${Math.sin(t * 5) * 3}deg)` }}>
      <div style={meme(96)}>{word}</div>
      <div style={{ ...meme(40, 6), marginTop: 2 }}><span>{sub.slice(0, n)}</span><span style={{ opacity: 0 }}>{sub.slice(n)}</span></div>
    </div>
  );
};
const FistLabels: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "api", "robot_fist", "made")) return null;
  return (
    <AbsoluteFill>
      <FistLabel t={t} t0={W.api} made={W.made} keys={API_KEYS} word="API" sub="(BACKEND DEVELOPMENT)" />
      <FistLabel t={t} t0={W.robot_fist} made={W.made} keys={ROBOT_KEYS} word="ROBOT" sub="(EMBEDDED SYSTEMS)" />
    </AbsoluteFill>
  );
};

// ======================================================================
// 8. Glitch on "broke": only he glitches. The plain blue wall is keyed out (alpha = 3R - 3B + 1), so the
//    red/cyan split and the slice jitter sit on him, not the wall. The camera is still here (no zoom/follow).
// ======================================================================
const KEY_A = "3 0 -3 0 1";
const GlitchDefs: React.FC = () => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <defs>
      <filter id="affKey" colorInterpolationFilters="sRGB"><feColorMatrix type="matrix" values={`1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  ${KEY_A}`} /></filter>
      <filter id="affKeyR" colorInterpolationFilters="sRGB"><feColorMatrix type="matrix" values={`1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  ${KEY_A}`} /></filter>
      <filter id="affKeyC" colorInterpolationFilters="sRGB"><feColorMatrix type="matrix" values={`0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  ${KEY_A}`} /></filter>
    </defs>
  </svg>
);
const Glitch: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "broke", "broke_e") || t < W.broke || t >= W.broke_e) return null;
  const fr = Math.round(t * FPS);
  if (fr % 4 === 3) return null; // stutter: some frames clean
  const r = (k: string) => random(`${k}${fr}`) - 0.5;
  const dx = 24 + Math.abs(r("dx")) * 50;
  const copy = (key: string, style: React.CSSProperties) => (
    <AbsoluteFill key={key} style={style}><OffthreadVideo muted src={staticFile(TRACK)} /></AbsoluteFill>
  );
  const bands = [];
  for (let i = 0; i < 5; i++) {
    const top = Math.floor(random(`gt${fr}${i}`) * 1500) + 200, h = 40 + Math.floor(random(`gh${fr}${i}`) * 160);
    bands.push(copy(`b${i}`, { filter: "url(#affKey)", clipPath: `inset(${top}px 0 ${Math.max(0, 1920 - top - h)}px 0)`, transform: `translateX(${r(`gx${i}`) * 160}px)` }));
  }
  return (
    <AbsoluteFill>
      <GlitchDefs />
      {copy("red", { filter: "url(#affKeyR)", mixBlendMode: "screen", opacity: 0.85, transform: `translateX(${-dx}px)` })}
      {copy("cyan", { filter: "url(#affKeyC)", mixBlendMode: "screen", opacity: 0.85, transform: `translateX(${dx}px)` })}
      {bands}
    </AbsoluteFill>
  );
};

// ======================================================================
// 9. "ENERGY?" pops letter by letter (one per frame), the question mark lands last, tilted
// ======================================================================
const EnergyPop: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "energy", "energy_out") || t < W.energy || t >= W.energy_out) return null;
  const q0 = W.energy + 0.27;
  return (
    <div style={{ position: "absolute", top: 220, left: 0, width: 1080, display: "flex", justifyContent: "center", alignItems: "flex-end" }}>
      {"ENERGY".split("").map((c, i) => {
        const t0 = W.energy + i / FPS;
        return (
          <span key={i} style={{ ...meme(150), display: "inline-block", visibility: t < t0 ? "hidden" : "visible",
            transform: `scale(${t < t0 ? 1 : punch(t, t0)}) translateY(${Math.sin(t * 7 + i) * 3}px)` }}>{c}</span>
        );
      })}
      <span style={{ ...meme(190), display: "inline-block", marginLeft: 8, visibility: t < q0 ? "hidden" : "visible", transformOrigin: "50% 90%",
        transform: `rotate(${12 + Math.sin((t - q0) * 9) * 6 * Math.exp(-Math.max(0, t - q0) * 1.5)}deg) scale(${t < q0 ? 1 : punch(t, q0)})` }}>?</span>
    </div>
  );
};

// ======================================================================
// 10. Claude Code terminal above the shrunk video. Every step shown really happened making this video
//     (/video cut: prep.py transcribed the long take, the video-cutter agent wrote cuts.json, render_cut.py
//     made the 80.7 s rough cut, add_music.py laid in Run Amok).
// ======================================================================
const CC = "#D77757"; // Claude Code orange (the terminal UI, not a company palette)
const PROMPT = "/video cut affinda";
const CC_LINES: [number, "text" | "tool" | "out", string][] = [
  [0.15, "text", "Starting phase 1: the cut."],
  [0.4, "tool", "Bash(python tools/video/prep.py documents/video/affinda)"],
  [0.6, "out", "long take transcribed, word timings saved"],
  [0.85, "tool", "Task(video-cutter)"],
  [1.05, "out", "cuts.json: 15 pieces"],
  [1.3, "tool", "Bash(python tools/video/render_cut.py documents/video/affinda)"],
  [1.5, "out", "rough cut: 80.7 s"],
  [1.75, "tool", "Bash(python tools/video/add_music.py documents/video/affinda)"],
  [1.95, "out", "Run Amok, ending lands on the wave"],
];
const Terminal: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "term_in", "term_out") || t < W.term_in || t >= W.term_out) return null;
  const a = W.term_in, b = W.term_out;
  const k = Math.min(lerp(t, [a, a + 0.25], [0, 1], Easing.out(Easing.cubic)), lerp(t, [b - 0.15, b], [1, 0], Easing.in(Easing.cubic)));
  const s2 = 1 - 0.44 * k, cy = 960 + 415 * k;
  const typeA = a + 0.15, typeB = a + 0.75, enter = a + 0.85;
  const typed = PROMPT.slice(0, Math.floor(lerp(t, [typeA, typeB], [0, PROMPT.length])));
  const sent = t >= enter;
  const mono: React.CSSProperties = { fontFamily: MONO, fontSize: 24, lineHeight: 1.5, whiteSpace: "pre", color: "#E8E8E8" };
  return (
    <AbsoluteFill style={{ background: "#141414" }}>
      <div style={{ position: "absolute", left: 36, top: 96, width: 1008, height: 640, borderRadius: 22, background: "#1E1E1E", border: "2px solid #333",
        overflow: "hidden", opacity: k, boxShadow: "0 18px 40px rgba(0,0,0,0.6)" }}>
        <div style={{ height: 48, background: "#2B2B2B", display: "flex", alignItems: "center", padding: "0 20px", gap: 10 }}>
          {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => <div key={c} style={{ width: 16, height: 16, borderRadius: 8, background: c }} />)}
          <div style={{ ...mono, fontSize: 21, color: "#9A9A9A", marginLeft: 14 }}>Terminal: claude</div>
        </div>
        <div style={{ padding: "16px 22px" }}>
          <div style={{ border: `2px solid ${CC}`, borderRadius: 12, padding: "6px 16px", marginBottom: 12 }}>
            <div style={mono}><span style={{ color: CC }}>✻</span> Welcome to <b>Claude Code</b>!</div>
            <div style={{ ...mono, fontSize: 21, color: "#8A8A8A" }}>  cwd: ~/Documents/ai-job-search</div>
          </div>
          {sent && <div style={{ ...mono, color: "#A8A8A8", background: "#2A2A2A", padding: "0 6px" }}>{"> " + PROMPT}</div>}
          {CC_LINES.map(([dt, kind, txt], i) => t >= enter + dt && (
            <div key={i} style={{ ...mono, marginTop: kind === "out" ? 0 : 6 }}>
              {kind === "text" && <><span>● </span>{txt}</>}
              {kind === "tool" && <><span style={{ color: "#4EBA65" }}>● </span><b>{txt.split("(")[0]}</b>({txt.split("(").slice(1).join("(")}</>}
              {kind === "out" && <span style={{ color: "#9A9A9A" }}>{"  ⎿  " + txt}</span>}
            </div>
          ))}
          {!sent && (
            <div style={{ border: "2px solid #5A5A5A", borderRadius: 10, padding: "4px 14px", marginTop: 6 }}>
              <div style={mono}>{"> " + typed}<span style={{ background: Math.floor(t * 2.5) % 2 === 0 ? "#E8E8E8" : "transparent" }}> </span></div>
            </div>
          )}
        </div>
      </div>
      <AbsoluteFill style={{ transformOrigin: "0 0", transform: `translate(${540 - 540 * s2}px, ${cy - 960 * s2}px) scale(${s2})`,
        borderRadius: k > 0 ? 40 : 0, overflow: "hidden", boxShadow: k > 0 ? `0 0 0 ${(6 / s2).toFixed(1)}px #FFFFFF` : "none" }}>
        <OffthreadVideo muted src={staticFile(TRACK)} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ======================================================================
// 11. Prompt Wrappers mock-up (plan split B-roll: zoom 1.0, focus [600, 440], push 0.12). The "Simple English"
//     toggle (1208, 676 in the 1380x1920 image) flicks on with his flick on "one click".
// ======================================================================
const IMG_K = 1080 / 1380, IMG_DY = (960 - 1920 * IMG_K) / 2; // objectFit cover into the 1080x960 split box
const TOG = { x: 1208 * IMG_K, y: 676 * IMG_K + IMG_DY, w: 108 * IMG_K, h: 66 * IMG_K };
const Toggle: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "one_is", "pw_out", "click") || t < W.click || t >= W.pw_out) return null;
  const S = 1 + 0.12 * lerp(t, [W.one_is, W.pw_out + 0.15], [0, 1]);
  const cx = 540 + S * (TOG.x - 600), cy = 480 + S * (TOG.y - 440);
  const w = TOG.w * S, h = TOG.h * S;
  const k = lerp(t, [W.click, W.click + 0.1], [0, 1], Easing.out(Easing.cubic));
  return (
    <svg width={1080} height={960} style={{ position: "absolute", left: 0, top: 0 }}>
      <rect x={cx - w / 2} y={cy - h / 2} width={w} height={h} rx={h / 2} fill="#111" />
      <circle cx={cx - w / 2 + h / 2 + (w - h) * k} cy={cy} r={h / 2 - 4 * S} fill="#fff" />
    </svg>
  );
};

// ======================================================================
// 12. Capsule: a map doodled on the wall above his head (white marker, black outline)
// ======================================================================
const PATHS = [
  "M 30 560 C 150 540, 260 500, 390 450 S 600 330, 690 270 S 900 210, 1050 250",
  "M 390 450 C 470 540, 640 590, 780 545 S 940 470, 1050 520",
  "M 170 330 C 200 400, 230 470, 270 520",
];
const TARGET = { x: 390, y: 450 };
const Pin: React.FC<{ x: number; y: number; t: number; t0: number; open: number }> = ({ x, y, t, t0, open }) => {
  if (t < t0) return null;
  const s = punch(t, t0);
  const hy = y - 56; // centre of the pin head
  return (
    <g transform={`translate(${x} ${y}) scale(${s}) translate(${-x} ${-y})`}>
      <path d={`M ${x} ${y} C ${x - 14} ${y - 22}, ${x - 34} ${hy + 18}, ${x - 34} ${hy} A 34 34 0 1 1 ${x + 34} ${hy} C ${x + 34} ${hy + 18}, ${x + 14} ${y - 22}, ${x} ${y} Z`}
        fill="#fff" stroke="#000" strokeWidth={6} strokeLinejoin="round" />
      <rect x={x - 13} y={hy - 4} width={26} height={20} rx={3} fill="#111" />
      <g transform={`rotate(${-35 * open} ${x + 8} ${hy - 4}) translate(0 ${-8 * open})`}>
        <path d={`M ${x - 8} ${hy - 4} L ${x - 8} ${hy - 12} A 8 8 0 0 1 ${x + 8} ${hy - 12} L ${x + 8} ${hy - 4}`} fill="none" stroke="#111" strokeWidth={5} />
      </g>
    </g>
  );
};
const CapsuleMap: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "leave", "messages", "campus", "walk", "map_out") || t < W.leave || t >= W.map_out) return null;
  const draw = lerp(t, [W.leave, W.leave + 0.35], [0, 1]);
  const pins = [
    { x: 170, y: 330, t0: W.leave + 0.12 },
    { x: 690, y: 270, t0: W.messages },
    { x: 900, y: 480, t0: W.messages + 0.22 },
    { x: TARGET.x, y: TARGET.y, t0: W.campus },
  ];
  const unlock = W.walk + 0.42, bubble = W.walk + 0.5;
  const open = lerp(t, [unlock, unlock + 0.08], [0, 1]);
  const steps = [];
  for (let i = 0; i < 6; i++) {
    const ts = W.walk + i * 0.07;
    if (t < ts) continue;
    const f = i / 5;
    const x = 405 + (i % 2 ? 14 : -14), y = 790 + (TARGET.y + 40 - 790) * f;
    steps.push(<ellipse key={i} cx={x} cy={y} rx={9} ry={14} fill="#fff" stroke="#000" strokeWidth={4} />);
  }
  return (
    <svg width={1080} height={1000} style={{ position: "absolute", left: 0, top: 0 }}>
      {PATHS.map((d, i) => <path key={`o${i}`} d={d} fill="none" stroke="#000" strokeWidth={20} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />)}
      {PATHS.map((d, i) => <path key={`w${i}`} d={d} fill="none" stroke="#fff" strokeWidth={10} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />)}
      {steps}
      {pins.map((p, i) => <Pin key={i} x={p.x} y={p.y} t={t} t0={p.t0} open={i === 3 ? open : 0} />)}
      {t >= bubble && (
        <g transform={`translate(500 310) scale(${punch(t, bubble)}) translate(-500 -310)`}>
          <path d="M 440 260 H 560 A 20 20 0 0 1 580 280 V 340 A 20 20 0 0 1 560 360 H 470 L 430 395 L 445 360 H 440 A 20 20 0 0 1 420 340 V 280 A 20 20 0 0 1 440 260 Z"
            fill="#fff" stroke="#000" strokeWidth={6} strokeLinejoin="round" />
          <text x={500} y={337} textAnchor="middle" fontFamily={ANTON} fontSize={70} fill="#111">?</text>
        </g>
      )}
    </svg>
  );
};

// ======================================================================
// 13. Paper stack beside him (viewer right, where he points on "the thing"), sucked into a plain laptop
// ======================================================================
const STK = { x: 975, base: 1560, n: 20, w: 190, h: 20, gap: 22 };
const LAP = { x: 940, y: 800 };
const Stack: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "slow", "build_thing", "thing", "so_in") || t < W.slow || t >= W.so_in) return null;
  const sway = (Math.sin(t * 2.6) * 2.2 * Math.PI) / 180;
  const sheets = [];
  for (let i = 0; i < STK.n; i++) {
    const tSuck = W.thing + (STK.n - 1 - i) * 0.025; // top sheets go first
    const k = lerp(t, [tSuck, tSuck + 0.18], [0, 1], Easing.in(Easing.quad));
    if (k >= 1) continue;
    const y0 = STK.base - i * STK.gap;
    const x0 = STK.x + (random(`sx${i}`) - 0.5) * 24 + (STK.base - y0) * Math.sin(sway);
    const x = x0 + (LAP.x - x0) * k, y = y0 + (LAP.y - 10 - y0) * k;
    const rot = (random(`sr${i}`) - 0.5) * 6 + k * 200;
    sheets.push(<rect key={i} x={-STK.w / 2} y={-STK.h / 2} width={STK.w} height={STK.h} fill="#F7F7F5" stroke="#000" strokeWidth={4}
      transform={`translate(${x} ${y}) rotate(${rot}) scale(${1 - 0.85 * k})`} />);
  }
  const lapOn = t >= W.build_thing, done = W.thing + 0.6;
  const ls = lapOn ? punch(t, W.build_thing) : 1;
  return (
    <AbsoluteFill>
      {t < W.build_thing && (
        <div style={{ position: "absolute", left: STK.x, top: 1040, transform: `translate(-50%,-50%) scale(${punch(t, W.slow)}) rotate(-4deg)`, textAlign: "center" }}>
          <div style={meme(62)}>DONE</div>
          <div style={meme(62)}>BY HAND</div>
        </div>
      )}
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {lapOn && (
          <g transform={`translate(${LAP.x} ${LAP.y}) scale(${ls}) translate(${-LAP.x} ${-LAP.y})`}>
            <rect x={LAP.x - 130} y={LAP.y - 95} width={260} height={170} rx={10} fill="#2B2B2B" stroke="#000" strokeWidth={7} />
            <rect x={LAP.x - 114} y={LAP.y - 80} width={228} height={140} fill={t >= done ? "#1E1E1E" : "#3A3F45"} />
            <path d={`M ${LAP.x - 160} ${LAP.y + 75} H ${LAP.x + 160} L ${LAP.x + 140} ${LAP.y + 100} H ${LAP.x - 140} Z`} fill="#C8C8C8" stroke="#000" strokeWidth={6} strokeLinejoin="round" />
          </g>
        )}
        {sheets}
        {t >= done && (
          <g transform={`translate(${LAP.x} ${LAP.y - 10}) scale(${punch(t, done)}) translate(${-LAP.x} ${-(LAP.y - 10)})`}>
            <text x={LAP.x - 22} y={LAP.y + 12} textAnchor="middle" fontFamily={ANTON} fontSize={64} fill="#fff" stroke="#000" strokeWidth={8} paintOrder="stroke">DONE</text>
            <path d={`M ${LAP.x + 52} ${LAP.y - 8} L ${LAP.x + 66} ${LAP.y + 10} L ${LAP.x + 98} ${LAP.y - 34}`} fill="none" stroke={RED} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" />
          </g>
        )}
      </svg>
    </AbsoluteFill>
  );
};

// ======================================================================
// 14. The resume comes back: the ball shoots out of the corner bin and unfolds into the end card
// ======================================================================
const EndPaper: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "thanks", "card") || t < W.thanks) return null;
  if (t < W.card) {
    const u = lerp(t, [W.thanks, W.card], [0, 1], Easing.out(Easing.quad));
    const x = 540, y = 1980 + (900 - 1980) * u - Math.sin(Math.PI * u) * 300;
    return <AbsoluteFill><Ball x={x} y={y} r={30 + 40 * u} rot={u * 900} /></AbsoluteFill>;
  }
  const sx = lerp(t, [W.card, W.card + 0.14], [0.12, 1], Easing.out(Easing.cubic));
  const sy = lerp(t, [W.card + 0.1, W.card + 0.28], [0.07, 1], Easing.out(Easing.cubic));
  const rot = lerp(t, [W.card, W.card + 0.28], [10, 0]);
  const open = t >= W.card + 0.28;
  const txt = (size: number, weight: number, top: number): React.CSSProperties => ({ fontFamily: MONT, fontWeight: weight, fontSize: size, color: "#222", marginTop: top });
  return (
    <AbsoluteFill style={{ transformOrigin: "540px 960px", transform: `rotate(${rot}deg) scale(${sx}, ${sy})`, background: "#F6F5F1",
      justifyContent: "center", alignItems: "center", textAlign: "center" }}>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        {[[0, 300, 1080, 560], [0, 1380, 1080, 1180], [380, 0, 520, 1920], [760, 0, 650, 1920], [0, 900, 1080, 980]].map(([x1, y1, x2, y2], i) => (
          <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#000" strokeOpacity={0.09} strokeWidth={3} />
        ))}
      </svg>
      {open && (
        <div style={{ transform: `scale(${punch(t, W.card + 0.28)})` }}>
          <div style={{ fontFamily: ANTON, fontSize: 130, color: "#111", letterSpacing: 1 }}>MANIT KHERA</div>
          <div style={txt(40, 600, 20)}>Software Engineering student · Deakin University</div>
          <div style={txt(46, 800, 70)}>manitkhera26@gmail.com</div>
          <div style={txt(36, 600, 20)}>linkedin.com/in/manit-khera-603957252</div>
        </div>
      )}
    </AbsoluteFill>
  );
};

export const Custom: React.FC<Props> = (p) => (
  <AbsoluteFill>
    <Rays {...p} />
    <Army {...p} />
    <Reel {...p} />
    <Speed {...p} />
    <FistLabels {...p} />
    <CapsuleMap {...p} />
    <Stack {...p} />
    <Toggle {...p} />
    <Glitch {...p} />
    <Checklist {...p} />
    <EnergyPop {...p} />
    <Whip {...p} />
    <Terminal {...p} />
    <Timer {...p} />
    <EndPaper {...p} />
  </AbsoluteFill>
);
