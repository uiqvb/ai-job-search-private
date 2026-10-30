// One-off gags for the Tesla video (plain, human-made style: real photo cut-outs, white judges cards,
// white monospace log, red marker circles; no Tesla colours or logo). Drawn above the video, under the
// meme text, captions and end card.
//  1. Roadster flight: in from the viewer right, arcs over his head with a full flip, lands on the viewer
//     left, timed to his eyes (his left, up, his right, then down at it).
//  2. Robot flop: the robot cut-out tries the same flip, stalls halfway, falls on its back, wheel spinning.
//     Replays tiny in the top-right corner on "No flips yet".
//  3. Judges scorecards (running gag): 10 10 10 / 2 1 0.5 / 10 10 10 with the last card dripping.
//  4. Telemetry log (top-left), reboot blink on "restart", red circles on bootId / resetCause,
//     red junk lines on "fake faulty data".
//  5. Red marker circle on the hand-on-robot B-roll ("FOUND IT" is a plan text).
//  6. Water splash on "wet" over the robot sticker.
//  7. 444-block grid in the top band (above his head): fills in, the go-live sweep turns it green column
//     by column, one block blinks red, the grid snaps in onto it.
// t = seconds in the cut; W = resolved plan anchors by name; face(t) = [x, y, width] of his face.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile } from "remotion";
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";

const { fontFamily: ANTON } = loadAnton();
const FPS = 30;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
// hard cut in with a 2-frame punch, no spring
const punch = (t: number, t0: number) => (t - t0 < 1 / FPS ? 1.18 : t - t0 < 2 / FPS ? 1.06 : 1);

const ROADSTER = "lib/project/img/roadster.png";
const ROBOT = "lib/editor-template/syncrowin-style/public/img/robot_sticker.png";
const RED = "#E8231B";
const GREEN = "#3DD65A";
const GREY = "#8E8E8E";
const WATER = "#BFE6FF";
// white sticker outline for the Roadster photo (the robot sticker already has one)
const OUTLINE =
  "drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(0 12px 18px rgba(0,0,0,0.45))";

type Props = { t: number; W: Record<string, number>; face: (t: number) => number[] };
const has = (W: Record<string, number>, ...k: string[]) => k.every((x) => typeof W[x] === "number");

// ---------- smooth path through keyframes [u, x, y, rotation] (Catmull-Rom) ----------
type Key = [number, number, number, number];
const along = (keys: Key[], u: number, easeLast = false): [number, number, number] => {
  const n = keys.length;
  if (u <= keys[0][0]) return [keys[0][1], keys[0][2], keys[0][3]];
  if (u >= keys[n - 1][0]) return [keys[n - 1][1], keys[n - 1][2], keys[n - 1][3]];
  let i = 0;
  while (u > keys[i + 1][0]) i++;
  let f = (u - keys[i][0]) / (keys[i + 1][0] - keys[i][0]);
  if (easeLast && i === n - 2) f = f * f; // falls faster and faster
  const p0 = keys[Math.max(0, i - 1)], p1 = keys[i], p2 = keys[i + 1], p3 = keys[Math.min(n - 1, i + 2)];
  const cr = (j: number) =>
    0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * f + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * f * f + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * f * f * f);
  return [cr(1), cr(2), p1[3] + (p2[3] - p1[3]) * f];
};

// ---------- red marker circle, drawn on in 0.25 s, plus a second loose pass ----------
const Scribble: React.FC<{ t: number; t0: number; cx: number; cy: number; rx: number; ry: number; rot?: number }> = ({ t, t0, cx, cy, rx, ry, rot = -6 }) => {
  if (t < t0) return null;
  const k1 = interpolate(t, [t0, t0 + 0.25], [0, 1], clamp);
  const k2 = interpolate(t, [t0 + 0.2, t0 + 0.4], [0, 1], clamp);
  const ring = (k: number, sx: number, sy: number, r: number, key: string) => (
    <g key={key} transform={`rotate(${r} ${cx} ${cy})`}>
      <ellipse cx={cx} cy={cy} rx={rx * sx} ry={ry * sy} fill="none" stroke="#000" strokeWidth={16} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} />
      <ellipse cx={cx} cy={cy} rx={rx * sx} ry={ry * sy} fill="none" stroke={RED} strokeWidth={9} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - k} />
    </g>
  );
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
      {ring(k1, 1, 1, rot, "a")}
      {k2 > 0 && ring(k2 * 0.85, 1.06, 0.9, rot + 6, "b")}
    </svg>
  );
};

// ======================================================================
// 1. Roadster flight (u = seconds after W.flight = end of "Roadster" + 0.14 s; matched to his eyes)
// ======================================================================
const CAR_W = 440;
const CAR_LAND = 1.72; // plan: slam + burst + shake at "@flight+2.15"
const CAR_KEYS: Key[] = [
  [0.0, 1320, 900, -8],   // off the viewer right
  [0.36, 930, 760, 20],   // he looks to his left (viewer right)
  [0.68, 760, 430, 110],  // he looks up and right
  [0.96, 480, 250, 200],   // apex over his head, he looks straight up ("ooh")
  [1.2, 250, 420, 280],   // he looks up to his right (viewer left)
  [1.48, 200, 900, 340],  // coming down on the viewer left
  [1.72, 230, 1440, 360], // lands upright; he stares down at it
];
const Roadster: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "flight", "too_in") || t < W.flight || t >= W.too_in) return null;
  const u = t - W.flight;
  const car = (uu: number, op: number, solid: boolean, key: string) => {
    const [x, y, r] = along(CAR_KEYS, uu);
    return (
      <Img key={key} src={staticFile(ROADSTER)} style={{ position: "absolute", left: x, top: y, width: CAR_W, opacity: op,
        transform: `translate(-50%, -50%) rotate(${r}deg)`, filter: solid ? OUTLINE : "none" }} />
    );
  };
  // two faint ghost frames behind it while it flies (hand-made motion blur)
  return (
    <AbsoluteFill>
      {u < CAR_LAND && car(u - 2 / FPS, 0.18, false, "g2")}
      {u < CAR_LAND && car(u - 1 / FPS, 0.35, false, "g1")}
      {car(u, 1, true, "car")}
    </AbsoluteFill>
  );
};

// ======================================================================
// 2. Robot flop (u = seconds after W.flop = end of "smaller" + 0.08 s); offsets from the landing point
// ======================================================================
const ROBOT_W = 300;
const IMG_W = 980; // robot_sticker.png is 980x740; the yellow wheel is centred at (515, 592), r ~104
const WHEEL = { x: 515, y: 592, r: 104 };
const FLOP_LAND = 0.69; // plan: puff + shake at "@flop+0.92"
const FLOP_KEYS: Key[] = [
  [0.0, 560, -60, 0],     // off the viewer right
  [0.225, 260, -320, 70],   // tries the same flip...
  [0.413, 120, -440, 150], // ...gets halfway (record scratch at "@flop+0.55")
  [0.54, 100, -450, 165], // hangs there
  [0.69, 0, 0, 180],      // drops on its back
];
const FlopRobot: React.FC<{ u: number; lx: number; ly: number; sc: number }> = ({ u, lx, ly, sc }) => {
  const [dx, dy, r0] = along(FLOP_KEYS, u, true);
  const after = Math.max(0, u - FLOP_LAND);
  const rot = u >= FLOP_LAND ? 180 + 3 * Math.sin(after * 14) * Math.exp(-after * 2) : r0; // rocks a little on its back
  const w = ROBOT_W * sc, k = w / IMG_W;
  const cx = WHEEL.x * k, cy = WHEEL.y * k, r = WHEEL.r * k;
  const spin = u * 900; // the wheel keeps spinning
  return (
    <div style={{ position: "absolute", left: lx + dx * sc, top: ly + dy * sc, width: w, transform: `translate(-50%, -50%) rotate(${rot}deg)` }}>
      <Img src={staticFile(ROBOT)} style={{ width: w, display: "block", filter: "drop-shadow(0 10px 14px rgba(0,0,0,0.45))" }} />
      <div style={{ position: "absolute", left: cx - r, top: cy - r, width: 2 * r, height: 2 * r, borderRadius: "50%", overflow: "hidden", transform: `rotate(${spin}deg)` }}>
        <Img src={staticFile(ROBOT)} style={{ position: "absolute", left: -(cx - r), top: -(cy - r), width: w, maxWidth: "none" }} />
      </div>
    </div>
  );
};
const Flop: React.FC<Props> = ({ t, W }) => (
  <>
    {has(W, "flop", "flips") && t >= W.flop && t < W.flips && <FlopRobot u={t - W.flop} lx={740} ly={1450} sc={1} />}
    {has(W, "mini") && t >= W.mini && <FlopRobot u={t - W.mini} lx={880} ly={560} sc={0.42} />}
  </>
);

// ======================================================================
// 3. Judges scorecards along the bottom (captions sit just above them at 1600)
// ======================================================================
const CARD_TOP = 1690, CW = 150, CH = 180;
const CARD_X = [330, 540, 750], CARD_ROT = [-4, 2, -2];
const CARDS1 = 1.8; // after W.flight (plan pops at "@flight+2.7", +2.85, +3.0)
const CARDS2 = 0.75; // after W.flop (plan pops at "@flop+1.2", +1.35, +1.5)
const Card: React.FC<{ t: number; t0: number; i: number; val: string; wet?: number }> = ({ t, t0, i, val, wet }) => {
  if (t < t0) return null;
  return (
    <div style={{ position: "absolute", left: CARD_X[i] - CW / 2, top: CARD_TOP, width: CW, height: CH + 80,
      transformOrigin: "50% 100%", transform: `rotate(${CARD_ROT[i]}deg) scale(${punch(t, t0)})` }}>
      <div style={{ position: "absolute", left: CW / 2 - 9, top: CH - 6, width: 18, height: 90, background: "#3a3a3a", border: "4px solid #000", boxSizing: "border-box" }} />
      <div style={{ position: "absolute", left: 0, top: 0, width: CW, height: CH, background: "#fff", border: "6px solid #000", borderRadius: 8, boxSizing: "border-box",
        display: "flex", alignItems: "center", justifyContent: "center", fontFamily: ANTON, fontSize: val.length > 2 ? 86 : 124, color: "#000", lineHeight: 1 }}>{val}</div>
      {wet !== undefined && t >= wet && [30, 78, 118].map((x, j) => {
        const ph = ((t - wet) * 1.1 + j * 0.33) % 1;
        return (
          <div key={j} style={{ position: "absolute", left: x - 7, top: 8 + ph * (CH - 24), width: 14, height: 20, background: WATER, border: "3px solid #000",
            borderRadius: "50% 50% 50% 50% / 60% 60% 40% 40%", opacity: interpolate(ph, [0.8, 1], [1, 0], clamp) }} />
        );
      })}
    </div>
  );
};
type CardSet = { t0s: number[]; end: number; vals: string[]; wet?: number };
const Cards: React.FC<Props> = ({ t, W }) => {
  const sets: CardSet[] = [];
  if (has(W, "flight", "too_in")) sets.push({ t0s: [0, 0.15, 0.3].map((d) => W.flight + CARDS1 + d), end: W.too_in, vals: ["10", "10", "10"] });
  if (has(W, "flop", "and_in")) sets.push({ t0s: [0, 0.15, 0.3].map((d) => W.flop + CARDS2 + d), end: W.and_in, vals: ["2", "1", "0.5"] });
  if (has(W, "rain", "is_wet", "wet", "much")) sets.push({ t0s: [W.rain, W.is_wet, W.wet], end: W.much, vals: ["10", "10", "10"], wet: W.wet });
  const s = sets.find((x) => t >= x.t0s[0] && t < x.end);
  if (!s) return null;
  return (
    <AbsoluteFill>
      {s.vals.map((v, i) => <Card key={i} t={t} t0={s.t0s[i]} i={i} val={v} wet={i === 2 ? s.wet : undefined} />)}
    </AbsoluteFill>
  );
};

// ======================================================================
// 4. Telemetry log, top-left. Field names are the real ones (bootId, resetCause); values are generic (Manit, 27 Oct: no made-up readings).
// ======================================================================
const MONO = "Courier New, Courier, monospace";
const LOG_X = 40, LOG_Y = 140, LH = 46, FS = 30, CHW = FS * 0.6; // Courier advance = 0.6 em
const OK41 = "rain=... light=... state=...";
const BOOT = "bootId=...  resetCause=...";
const OK42 = "rain=... light=... state=...";
const OKT = "rain=DRY state=DRYING";
const JUNK = ["rain=%%#@! state=??????", "rain=NaN light=NaN", "{\"rain\":tru", "state=@#!&*% rain=WET?DRY", "bootId=??? resetCause=???",
  "rain=#######", "light=-?? state=NULL", "rain=WETWETWETWETWET", "{{{{\"state\":", "rain=DRY?WET?DRY?WET"];
type Line = { txt: string; red?: boolean; boot?: boolean };
const LogLines: React.FC<{ lines: Line[] }> = ({ lines }) => (
  <>
    {lines.map((l, i) => (
      <div key={i} style={{ position: "absolute", left: LOG_X, top: LOG_Y + i * LH, fontFamily: MONO, fontWeight: 700, fontSize: FS, lineHeight: 1,
        whiteSpace: "pre", color: l.red ? "#FF3B30" : "#FFFFFF", WebkitTextStroke: "6px #000", paintOrder: "stroke fill" }}>{l.txt}</div>
    ))}
  </>
);
const Log: React.FC<Props> = ({ t, W }) => {
  // part 1: "It sends its data..." until the B-roll on "that led me"; stops scrolling after "random"
  if (has(W, "log_in", "restart", "random_e", "split2") && t >= W.log_in && t < W.split2) {
    const tt = Math.min(t, W.random_e);
    const all: Line[] = [];
    for (let s = W.log_in; s <= tt && s < W.restart; s += 0.55) all.push({ txt: OK41 });
    if (tt >= W.restart + 0.2) {
      all.push({ txt: BOOT, boot: true });
      for (let s = W.restart + 0.75; s <= tt; s += 0.55) all.push({ txt: OK42 });
    }
    const lines = all.slice(-6);
    const bi = lines.findIndex((l) => l.boot);
    const cy = LOG_Y + bi * LH + FS * 0.5;
    const ring = (a: number, b: number) => ({ cx: LOG_X + ((a + b) / 2) * CHW, rx: ((b - a) * CHW) / 2 + 22 });
    const id = ring(0, 10), rc = ring(12, 26);
    return (
      <AbsoluteFill>
        <LogLines lines={lines} />
        {bi >= 0 && has(W, "boot") && <Scribble t={t} t0={W.boot} cx={id.cx} cy={cy} rx={id.rx} ry={34} rot={-4} />}
        {bi >= 0 && has(W, "reset") && <Scribble t={t} t0={W.reset} cx={rc.cx} cy={cy} rx={rc.rx} ry={34} rot={3} />}
      </AbsoluteFill>
    );
  }
  // part 2: stress test, "Before I trusted it..." until "Megapacks"; red junk floods in on "fake faulty data"
  if (has(W, "log_back", "fake", "megapacks") && t >= W.log_back && t < W.megapacks) {
    const all: Line[] = [];
    for (let s = W.log_back; s <= t && s < W.fake; s += 0.5) all.push({ txt: OKT });
    let j = 0;
    for (let s = W.fake; s <= t; s += 0.14) all.push({ txt: JUNK[j++ % JUNK.length], red: true });
    return <AbsoluteFill><LogLines lines={all.slice(-6)} /></AbsoluteFill>;
  }
  return null;
};
// reboot: the whole frame blinks off for 0.2 s on "restart"
const Blink: React.FC<Props> = ({ t, W }) =>
  has(W, "restart") && t >= W.restart && t < W.restart + 0.2 ? <AbsoluteFill style={{ background: "#000" }} /> : null;

// ======================================================================
// 5. Red circle on the hand-on-robot B-roll (split box = top 1080x960)
// ======================================================================
const FoundIt: React.FC<Props> = ({ t, W }) =>
  has(W, "failing", "split2_out") && t >= W.failing && t < W.split2_out
    ? <Scribble t={t} t0={W.failing} cx={590} cy={330} rx={210} ry={150} rot={-8} /> : null;

// ======================================================================
// 6. Splash on "wet", over the robot sticker at (840, 1330)
// ======================================================================
const Splash: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "wet")) return null;
  const d = t - W.wet;
  if (d < 0 || d >= 0.8) return null;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
      {Array.from({ length: 12 }).map((_, j) => {
        const a = -Math.PI / 2 + (j / 11 - 0.5) * 2.2;
        const v = 520 + (j % 3) * 140;
        const x = 840 + Math.cos(a) * v * d;
        const y = 1225 + Math.sin(a) * v * d + 0.5 * 2600 * d * d;
        return <circle key={j} cx={x} cy={y} r={9 + (j % 4) * 3} fill={WATER} stroke="#000" strokeWidth={4} opacity={interpolate(d, [0.6, 0.8], [1, 0], clamp)} />;
      })}
    </svg>
  );
};

// ======================================================================
// 7. 444 Megapacks grid in the top band (above his head): 26 per row, 17 rows + 2
// ======================================================================
const COLS = 26, PITCH = 40, BLK = 32, N = 444;
const GX = (1080 - COLS * PITCH) / 2, GY = 40;
const RED_C = 18, RED_R = 12, RED_I = RED_R * COLS + RED_C;
const Grid: React.FC<Props> = ({ t, W }) => {
  if (!has(W, "grid_in", "grid_out") || t < W.grid_in || t >= W.grid_out) return null;
  const k = has(W, "grid_zoom") ? interpolate(t, [W.grid_zoom, W.grid_zoom + 0.2], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) }) : 0;
  const s = 1 + 1.6 * k;
  const bx = GX + RED_C * PITCH + PITCH / 2, by = GY + RED_R * PITCH + PITCH / 2;
  const tx = bx + (540 - bx) * k, ty = by + (400 - by) * k;
  const golive = has(W, "tests", "live_e");
  return (
    <AbsoluteFill>
      <svg width={1080} height={800} style={{ position: "absolute", left: 0, top: 0 }}>
        <g transform={`translate(${tx} ${ty}) scale(${s}) translate(${-bx} ${-by})`}>
          {Array.from({ length: N }).map((_, i) => {
            const r = Math.floor(i / COLS), c = i % COLS;
            if (t < W.grid_in + r * 0.025) return null; // fills in row by row
            let fill = GREY;
            if (golive && t >= W.tests + (c / (COLS - 1)) * (W.live_e - W.tests)) fill = GREEN;
            if (i === RED_I && has(W, "red") && t >= W.red) {
              const d = t - W.red;
              fill = d > 1.0 || Math.floor(d * 10) % 2 === 0 ? RED : fill;
            }
            return <rect key={i} x={GX + c * PITCH + (PITCH - BLK) / 2} y={GY + r * PITCH + (PITCH - BLK) / 2} width={BLK} height={BLK} fill={fill} stroke="#000" strokeWidth={3} />;
          })}
        </g>
      </svg>
      {has(W, "grid_zoom") && <Scribble t={t} t0={W.grid_zoom + 0.22} cx={540} cy={400} rx={80} ry={74} rot={-10} />}
    </AbsoluteFill>
  );
};

export const Custom: React.FC<Props> = (p) => (
  <AbsoluteFill>
    <Grid {...p} />
    <Log {...p} />
    <FoundIt {...p} />
    <Roadster {...p} />
    <Flop {...p} />
    <Splash {...p} />
    <Cards {...p} />
    <Blink {...p} />
  </AbsoluteFill>
);
