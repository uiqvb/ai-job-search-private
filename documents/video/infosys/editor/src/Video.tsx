// Infosys intro video, Draft 1: old-PewDiePie, human-made edit (see documents/video/EDITING-STYLE.md).
// Storyboard: documents/video/infosys/Storyboard.md. Every time below is a ROUGH-CUT second (words.json).
// Draft 2: no freeze; the real stare after "right" carries the B&W + echo beat. Rally photo, rising robot, robot leaves the screen.
import React from "react";
import {
  AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, random, staticFile, useCurrentFrame, Easing,
} from "remotion";
import { loadFont as loadMont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import face from "./face_track.json";
import words from "./words.json";

const { fontFamily: MONT } = loadMont("normal", { weights: ["600", "700", "800", "900"] });
const { fontFamily: ANTON } = loadAnton();

export const FPS = 30;
const TRACK_LEN = 50.6; // Draft 2: the stare after "right" is real footage (1.15 s longer), no freeze frame
export const TOTAL_FRAMES = Math.round(TRACK_LEN * FPS);
const F = (t: number) => Math.round(t * FPS);
const toTrack = (o: number) => o;

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp = (t: number, a: number[], b: number[], ease?: (x: number) => number) =>
  interpolate(t, a, b, { ...clamp, easing: ease });

// word times (rough cut)
const W: Record<string, number> = {
  okay: 0.0, robot: 2.0, mine: 3.84, deakin: 4.54, openDayEnd: 5.45,
  api: 7.66, robot2: 8.78, meet: 11.46, handsUp: 12.35, zoomRobot: 12.75, meetEnd: 13.89,
  chair: 14.04, right: 17.52, then: 18.08, hundred: 19.54, hundred2: 20.1,
  matchfeel: 23.04, courtEnd: 27.3, anyways: 27.16, same: 28.4, myRobot: 28.82, brollEnd: 30.5, built: 31.48, anywayEnd: 32.7,
  leave: 35.8, screenEnd: 36.6, yet: 38.36, yetEnd: 39.5, mlStart: 36.86, mlEnd: 41.3,
  name: 42.82, more: 44.42, watching: 47.16, endCard: 47.75,
};
const STARE = 1.15; // Draft 2: track after "right" moved later by this much
(Object.keys(W) as (keyof typeof W)[]).forEach((k) => { if (W[k] > 17.9) W[k] = +(W[k] + STARE).toFixed(3); });

// ---------- tracking ----------
type Row = number[];
const at = (rows: Row[], t: number) => {
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
// Camera
// ======================================================================
const ZOOMS: [number, number, number, number][] = [
  // [from, to, scale, tilt deg] snap zooms that follow the face
  [W.okay, 0.95, 1.25, -1.5],
  [W.right, W.then, 1.9, -4], // "he was RIGHT": black and white + echo, held on a freeze
  [W.then, 19.4, 1.3, 2],
  [W.anyways, W.same, 1.4, -3],
  [W.more, 45.9, 1.25, -2],
];
const ROBOT_AT = [540, 1180]; // where the robot photo pops (video coords)
// Draft 2: after it pops between his hands it floats UP, to where he is looking (above his head)
const RISE_A = W.handsUp + 0.08, RISE_B = W.handsUp + 0.65;
const robotPos = (t: number): [number, number] => {
  const k = lerp(t, [RISE_A, RISE_B], [0, 1], Easing.out(Easing.cubic));
  return [ROBOT_AT[0] + Math.sin(t * 3) * 8 * k, ROBOT_AT[1] + (520 - ROBOT_AT[1]) * k + Math.sin(t * 4) * 10 * k];
};

type Cam = { s: number; tx: number; ty: number; rot: number };
const camAt = (t: number): Cam => {
  let s = 1, tx = 0, ty = 0, rot = 0;
  for (const [a, b, S, R] of ZOOMS) {
    if (t >= a && t < b + 2 / FPS) {
      const k = Math.min(lerp(t, [a, a + 2 / FPS], [0, 1]), lerp(t, [b, b + 2 / FPS], [1, 0]));
      const [fx, fy] = faceAt(t);
      s = 1 + (S - 1) * k;
      const drift = Math.sin(t * 2.3) * 6;
      tx = k * (540 - s * fx + drift);
      ty = k * (800 - s * fy);
      rot = R * k;
    }
  }
  // the meet beat: the frame follows his head left and right, comes back to centre as the hands meet,
  // tilts up with him on hands-up, then snaps into the robot photo
  if (t >= 7.2 && t < W.meetEnd) {
    const k = Math.min(lerp(t, [7.2, 7.5], [0, 1], Easing.out(Easing.cubic)), lerp(t, [W.meetEnd - 0.05, W.meetEnd], [1, 0]));
    const [fx] = faceAt(t);
    const look = (fx - 540) * 0.9; // follow the head turn
    const centre = lerp(t, [10.8, W.meet], [1, 0], Easing.inOut(Easing.cubic)); // back to centre for the meet
    const up = lerp(t, [W.handsUp - 0.1, W.handsUp + 0.25], [0, 1], Easing.out(Easing.cubic));
    s = 1 + 0.18 * k;
    const cx = 540 + look * centre, cy = 960 - 140 * up;
    tx = 540 - s * cx; ty = 960 - s * cy;
    rot = (look / 540) * 3 * centre * k;
    // Draft 2: tilt up and push in, following the robot as it rises (his eyes and hands go up with it)
    const z = lerp(t, [RISE_A, RISE_B + 0.1], [0, 1], Easing.inOut(Easing.cubic));
    if (z > 0) {
      const [rx, ry] = robotPos(t);
      const S2 = s + (1.6 - s) * z;
      const cx2 = cx + (rx - cx) * z, cy2 = cy + (ry + 260 - cy) * z; // keep the robot high, his face below it
      s = S2; tx = 540 - S2 * cx2; ty = 960 - S2 * cy2; rot = rot * (1 - z) - 1.5 * z;
    }
  }
  tx = Math.min(0, Math.max(1080 - s * 1080, tx));
  ty = Math.min(0, Math.max(1920 - s * 1920, ty));
  const d = t - W.meet; // little shake when the labels smack together
  if (d >= 0 && d < 0.35) {
    const e = Math.exp(-d * 9) * 14;
    tx = Math.min(0, Math.max(1080 - s * 1080, tx + Math.sin(d * 120) * e));
    ty = Math.min(0, Math.max(1920 - s * 1920, ty + Math.cos(d * 97) * e));
  }
  return { s, tx, ty, rot };
};

// split screen for B-roll: demo on top, his face pushed down into the bottom half
const SPLITS: [number, number, string, number][] = [
  [W.mine, W.openDayEnd, "broll/openday.mp4", 162.5], // the robot on the Open Day table
  [W.myRobot, W.brollEnd, "stills/robot.png", 0], // the robot photo
];
const splitK = (t: number) => {
  for (const [a, b] of SPLITS) if (t >= a - 0.01 && t < b + 0.15)
    return Math.min(lerp(t, [a, a + 0.12], [0, 1], Easing.out(Easing.cubic)), lerp(t, [b, b + 0.12], [1, 0], Easing.in(Easing.cubic)));
  return 0;
};

const cameraStyle = (t: number): React.CSSProperties => {
  const c = camAt(t);
  const sk = splitK(t);
  const bw = t >= W.right && t < W.then;
  const extra = c.rot !== 0 ? 1.05 : 1;
  return {
    transformOrigin: "0px 0px",
    transform: `translate(0px, ${sk * 520}px) translate(${c.tx}px, ${c.ty}px) scale(${c.s}) translate(540px, 960px) rotate(${c.rot}deg) scale(${extra}) translate(-540px, -960px)`,
    filter: bw ? "grayscale(1) contrast(1.15)" : "none",
    overflow: "hidden",
  };
};

const SplitBroll: React.FC<{ t: number }> = ({ t }) => {
  const k = splitK(t);
  const [a1] = SPLITS[1];
  const still = 1 + 0.25 * lerp(t, [a1, SPLITS[1][1] + 0.15], [0, 1]); // slow push-in on the robot photo
  return (
    <AbsoluteFill style={{ height: 960 * k, overflow: "hidden", borderBottom: k > 0 ? "6px solid #fff" : "none", opacity: k > 0 ? 1 : 0 }}>
      {/* Open Day: the robot on the table at 2:42, zoomed in 2.2x on it */}
      <Sequence from={F(SPLITS[0][0])} durationInFrames={F(SPLITS[0][1] + 0.2) - F(SPLITS[0][0])}>
        <AbsoluteFill style={{ transformOrigin: "0 0", transform: `translate(${540 - 2.2 * 558}px, ${480 - 2.2 * 311}px) scale(2.2)` }}>
          <OffthreadVideo muted src={staticFile("broll/openday.mp4")} startFrom={Math.round(162.5 * FPS)} style={{ width: 1080, height: 960, objectFit: "cover" }} />
        </AbsoluteFill>
      </Sequence>
      {/* "Same with my robot": the clean 4K photo of the robot */}
      {t >= a1 - 0.01 && (
        <Img src={staticFile("stills/robot.png")} style={{ width: 1080, height: 960, transformOrigin: "540px 600px", transform: `scale(${still})` }} />
      )}
    </AbsoluteFill>
  );
};

// ======================================================================
// The meet: API and ROBOT ride his fists, smack together, then pop into the robot photo
// ======================================================================
const LABELS = [
  // [text, appear, start pos (on the fist, edge of frame), meet pos, tilt]
  { txt: "API", at: W.api, p0: [770, 1620], p1: [660, 1530], rot: 6 },
  { txt: "ROBOT", at: W.robot2, p0: [300, 1620], p1: [420, 1530], rot: -6 },
];
const Meet: React.FC<{ t: number }> = ({ t }) => {
  if (t < W.api || t >= W.meetEnd) return null;
  const pop = lerp(t, [W.handsUp, W.handsUp + 0.12], [0, 1], Easing.out(Easing.back(2.5)));
  return (
    <AbsoluteFill>
      {t < W.handsUp + 0.08 && LABELS.map((L) => {
        if (t < L.at) return null;
        const k = lerp(t, [10.75, W.meet], [0, 1], Easing.in(Easing.quad));
        const bob = Math.sin(t * 7 + L.at) * 6 * (1 - k);
        const x = L.p0[0] + (L.p1[0] - L.p0[0]) * k, y = L.p0[1] + (L.p1[1] - L.p0[1]) * k + bob;
        const squash = t >= W.meet && t < W.meet + 0.1 ? 0.85 : 1;
        const gone = 1 - lerp(t, [W.handsUp, W.handsUp + 0.08], [0, 1]);
        return (
          <div key={L.txt} style={{ position: "absolute", left: x, top: y, transform: `translate(-50%,-50%) rotate(${L.rot * (1 - k)}deg) scale(${punch(t, L.at) * squash * gone}, ${punch(t, L.at) * gone})` }}>
            <div style={meme(110)}>{L.txt}</div>
          </div>
        );
      })}
      {t >= W.meet && t < W.meet + 0.18 && (
        <svg width={1080} height={1920} style={{ position: "absolute" }}>
          {Array.from({ length: 10 }).map((_, i) => {
            const a = (i / 10) * Math.PI * 2, d = lerp(t, [W.meet, W.meet + 0.18], [40, 150]);
            return <line key={i} x1={530 + Math.cos(a) * d} y1={1530 + Math.sin(a) * d} x2={530 + Math.cos(a) * (d + 50)} y2={1530 + Math.sin(a) * (d + 50)}
              stroke="#fff" strokeWidth={12} strokeLinecap="round" />;
          })}
        </svg>
      )}
      {pop > 0 && (
        <div style={{ position: "absolute", left: robotPos(t)[0], top: robotPos(t)[1], transform: `translate(-50%,-50%) scale(${pop}) rotate(${Math.sin(t * 5) * 4}deg)` }}>
          <Img src={staticFile("img/robot_sticker.png")} style={{ width: 420, filter: "drop-shadow(0 10px 18px rgba(0,0,0,0.45))" }} />
        </div>
      )}
      {pop > 0 && t < W.handsUp + 0.8 && (
        <svg width={1080} height={1920} style={{ position: "absolute" }}>
          {Array.from({ length: 16 }).map((_, i) => {
            const [rx, ry] = robotPos(t);
            const a = random(`sa${i}`) * Math.PI * 2, d = lerp(t, [W.handsUp, W.handsUp + 0.8], [120, 360]) * (0.7 + random(`sd${i}`) * 0.5);
            const r = 10 * (1 - lerp(t, [W.handsUp + 0.4, W.handsUp + 0.8], [0, 1]));
            return <circle key={i} cx={rx + Math.cos(a) * d} cy={ry + Math.sin(a) * d} r={Math.max(0, r)} fill="#fff" stroke="#000" strokeWidth={3} />;
          })}
        </svg>
      )}
    </AbsoluteFill>
  );
};

// ======================================================================
// Tennis: scoreboard in the corner, MatchFeel court
// ======================================================================
const SCORES: [number, string][] = [
  [W.okay + 0.1, "0-0"], [W.deakin, "15-0"], [W.meet, "30-0"], [W.right, "30-40"], [W.hundred2, "GAME"],
];
const Ball: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 100 100">
    <circle cx={50} cy={50} r={45} fill="#D7F23A" stroke="#000" strokeWidth={7} />
    <path d="M12 30 C 40 40, 40 60, 12 72" stroke="#fff" strokeWidth={6} fill="none" />
    <path d="M88 30 C 60 40, 60 60, 88 72" stroke="#fff" strokeWidth={6} fill="none" />
  </svg>
);
const Score: React.FC<{ t: number }> = ({ t }) => {
  if (t < SCORES[0][0] || t >= W.endCard) return null;
  const cur = [...SCORES].reverse().find(([a]) => t >= a)!;
  return (
    <div style={{ position: "absolute", right: 40, top: 46, display: "flex", alignItems: "center", gap: 14, transform: `scale(${punch(t, cur[0])})`, transformOrigin: "100% 0" }}>
      <Ball size={62} />
      <div style={meme(80)}>{cur[1]}</div>
    </div>
  );
};

const Court: React.FC<{ t: number }> = ({ t }) => {
  if (t < W.matchfeel || t >= W.courtEnd) return null;
  // court seen from above, top of the frame; a dot (the ring) traces the ball's path across the lines
  const X0 = 190, Y0 = 250, CW = 700, CH = 330;
  const path: [number, number][] = [[0.1, 0.85], [0.85, 0.2], [0.2, 0.25], [0.75, 0.8], [0.3, 0.6], [0.9, 0.5]];
  const p = ((t - W.matchfeel) / 0.75) % (path.length - 1);
  const i = Math.floor(p), f = p - i;
  const [ax, ay] = path[i], [bx, by] = path[i + 1];
  const bx2 = X0 + (ax + (bx - ax) * f) * CW, by2 = Y0 + (ay + (by - ay) * f) * CH;
  const trail = [];
  for (let k = 1; k <= 6; k++) {
    const q = Math.max(0, p - k * 0.05), j = Math.floor(q), g = q - j;
    const [cx, cy] = path[j], [dx, dy] = path[Math.min(j + 1, path.length - 1)];
    trail.push(<circle key={k} cx={X0 + (cx + (dx - cx) * g) * CW} cy={Y0 + (cy + (dy - cy) * g) * CH} r={22 - k * 2.5} fill="#D7F23A" opacity={0.6 - k * 0.09} />);
  }
  const line = { stroke: "#fff", strokeWidth: 8, fill: "none" } as const;
  return (
    <AbsoluteFill style={{ transform: `scale(${punch(t, W.matchfeel)})`, transformOrigin: "540px 400px" }}>
      <div style={{ position: "absolute", top: 110, width: 1080, textAlign: "center" }}><div style={meme(110)}>MATCHFEEL</div></div>
      <svg width={1080} height={1920} style={{ position: "absolute", filter: "drop-shadow(0 0 3px #000) drop-shadow(0 0 3px #000)" }}>
        <rect x={X0} y={Y0} width={CW} height={CH} {...line} />
        <line x1={X0} y1={Y0 + CH * 0.12} x2={X0 + CW} y2={Y0 + CH * 0.12} {...line} />
        <line x1={X0} y1={Y0 + CH * 0.88} x2={X0 + CW} y2={Y0 + CH * 0.88} {...line} />
        <line x1={X0 + CW / 2} y1={Y0 - 14} x2={X0 + CW / 2} y2={Y0 + CH + 14} stroke="#fff" strokeWidth={12} />
        <line x1={X0 + CW * 0.23} y1={Y0 + CH * 0.12} x2={X0 + CW * 0.23} y2={Y0 + CH * 0.88} {...line} />
        <line x1={X0 + CW * 0.77} y1={Y0 + CH * 0.12} x2={X0 + CW * 0.77} y2={Y0 + CH * 0.88} {...line} />
        <line x1={X0 + CW * 0.23} y1={Y0 + CH / 2} x2={X0 + CW * 0.77} y2={Y0 + CH / 2} {...line} />
        {trail}
        <circle cx={bx2} cy={by2} r={24} fill="#D7F23A" stroke="#000" strokeWidth={5} />
      </svg>
    </AbsoluteFill>
  );
};

// ======================================================================
// Meme text, name tag, end card
// ======================================================================
const TEXTS: { from: number; to: number; txt: string; size: number; top: number; rot: number }[] = [
  { from: W.hundred2, to: 22.5, txt: "100/100", size: 150, top: 230, rot: 3 },
  { from: W.built, to: W.anywayEnd, txt: "BUILT IT ANYWAY", size: 112, top: 250, rot: -3 },
  { from: W.yet, to: W.yetEnd, txt: "NOT YET", size: 100, top: 270, rot: 4 },
];
// Rally, Infosys's AO 2026 robot: photo cut-out with a white sticker outline, slides in and waves
const Rally: React.FC<{ t: number }> = ({ t }) => {
  if (t < W.robot || t >= W.mine) return null;
  const k = lerp(t, [W.robot, W.robot + 0.14], [0, 1], Easing.out(Easing.back(1.6)));
  return (
    <div style={{ position: "absolute", left: -320 + 620 * k, top: 1180, transform: `translate(-50%,-50%) rotate(${-6 + Math.sin(t * 6) * 3}deg)` }}>
      <div style={{ position: "absolute", top: -95, width: 520, textAlign: "center", transform: `rotate(-4deg) scale(${punch(t, W.robot)})` }}><div style={{ ...meme(120), display: "inline-block" }}>RALLY</div></div>
      <Img src={staticFile("img/rally_sticker.png")} style={{ width: 520, filter: "drop-shadow(0 12px 20px rgba(0,0,0,0.5))" }} />
    </div>
  );
};

// "AI and robots that leave the screen": the shot shrinks into a phone, and his robot drives out of it at you
const SCR_A = W.leave - 0.12, SCR_B = W.screenEnd + 0.25;
const screenK = (t: number) => (t < SCR_A || t > SCR_B + 0.12 ? 0 :
  Math.min(lerp(t, [SCR_A, SCR_A + 0.14], [0, 1], Easing.out(Easing.cubic)), lerp(t, [SCR_B, SCR_B + 0.12], [1, 0], Easing.in(Easing.cubic))));
const PH = { s: 0.6, cx: 540, cy: 900 }; // phone scale and centre
const PhoneBack: React.FC<{ t: number }> = ({ t }) => {
  const k = screenK(t);
  if (k <= 0) return null;
  const s = 1 - (1 - PH.s) * k, w = 1080 * s, h = 1920 * s;
  return (
    <AbsoluteFill style={{ background: "#0E1A26" }}>
      <div style={{ position: "absolute", left: PH.cx - w / 2 - 26, top: PH.cy - h / 2 - 26, width: w + 52, height: h + 52, borderRadius: 70 * k, background: "#111", boxShadow: "0 30px 60px rgba(0,0,0,0.6)" }} />
    </AbsoluteFill>
  );
};
const phoneStyle = (t: number): React.CSSProperties => {
  const k = screenK(t);
  if (k <= 0) return {};
  const s = 1 - (1 - PH.s) * k;
  return { transformOrigin: "0 0", transform: `translate(${PH.cx - 540 * s}px, ${PH.cy - 960 * s}px) scale(${s})`, borderRadius: 50 * k / s, overflow: "hidden" };
};
const RobotOut: React.FC<{ t: number }> = ({ t }) => {
  const a = W.leave + 0.05, b = SCR_B + 0.1;
  if (t < a || t > b) return null;
  const k = lerp(t, [a, b], [0, 1], Easing.in(Easing.cubic));
  const sc = 0.3 + 5.2 * lerp(t, [a, b], [0, 1], Easing.in(Easing.quad));
  return (
    <div style={{ position: "absolute", left: 540 + 60 * k, top: 900 + 420 * k, transform: `translate(-50%,-50%) scale(${sc}) rotate(${-8 * k}deg)`, filter: k > 0.6 ? `blur(${(k - 0.6) * 12}px)` : "none" }}>
      <Img src={staticFile("img/robot_sticker.png")} style={{ width: 380, filter: "drop-shadow(0 16px 24px rgba(0,0,0,0.55))" }} />
    </div>
  );
};

const MemeText: React.FC<{ t: number }> = ({ t }) => (
  <AbsoluteFill>
    {TEXTS.map((x) => t >= x.from && t < x.to && (
      <div key={x.txt} style={{ position: "absolute", top: x.top, width: 1080, textAlign: "center" }}>
        <div style={{ ...meme(x.size), display: "inline-block", transform: `rotate(${x.rot}deg) scale(${punch(t, x.from)})` }}>{x.txt}</div>
      </div>
    ))}
  </AbsoluteFill>
);

const NameTag: React.FC<{ t: number }> = ({ t }) => {
  if (t < W.name || t >= W.endCard) return null;
  return (
    <div style={{ position: "absolute", left: 56, top: 190, transform: `rotate(-2deg) scale(${punch(t, W.name)})`, transformOrigin: "0 0" }}>
      <div style={meme(110)}>MANIT KHERA</div>
      <div style={{ fontFamily: MONT, fontWeight: 800, fontSize: 38, color: "#fff", WebkitTextStroke: "6px #000", paintOrder: "stroke fill" }}>Software Engineering student, Deakin</div>
    </div>
  );
};

const EndCard: React.FC<{ t: number }> = ({ t }) => {
  if (t < W.endCard) return null;
  return (
    <AbsoluteFill style={{ background: "#000", justifyContent: "center", alignItems: "center", textAlign: "center", color: "#fff", fontFamily: MONT }}>
      <div style={{ display: "flex", alignItems: "center", gap: 18, transform: `scale(${punch(t, W.endCard)})` }}><Ball size={70} /><div style={meme(84)}>GAME, SET, MATCH</div></div>
      <div style={{ ...meme(130), marginTop: 70 }}>MANIT KHERA</div>
      <div style={{ fontSize: 40, fontWeight: 600, marginTop: 20 }}>Software Engineering student · Deakin University</div>
      <div style={{ fontSize: 46, fontWeight: 800, marginTop: 70 }}>manitkhera26@gmail.com</div>
      <div style={{ fontSize: 36, fontWeight: 600, marginTop: 20 }}>linkedin.com/in/manit-khera-603957252</div>
    </AbsoluteFill>
  );
};

// ---------- captions (white, current word yellow) ----------
type Wd = { w: string; s: number; e: number };
const FIX: Record<string, string> = {};
const CHUNKS = (() => {
  const src = (words as Wd[]).map((x) => ({ ...x, w: FIX[x.w] ?? x.w }));
  const res: { words: Wd[]; s: number; e: number }[] = [];
  let cur: Wd[] = [];
  const flush = () => { if (cur.length) res.push({ words: cur.map((c) => ({ ...c, w: c.w.replace(/[.,]+$/, "") })), s: cur[0].s, e: cur[cur.length - 1].e }); cur = []; };
  src.forEach((x, i) => {
    const next = src[i + 1];
    cur.push(x);
    const len = cur.map((c) => c.w).join(" ").length;
    if (cur.length >= 4 || len > 15 || /[.,?]$/.test(x.w) || !next || next.s - x.e > 0.35) flush();
  });
  for (let i = 0; i < res.length; i++) res[i].e = Math.min(res[i].e + 0.25, res[i + 1] ? res[i + 1].s : Infinity);
  return res;
})();
const Captions: React.FC<{ t: number }> = ({ t }) => {
  if (t >= W.endCard) return null;
  const c = CHUNKS.find((x) => t >= x.s && t < x.e);
  if (!c) return null;
  const top = t >= 7.2 && t < W.meetEnd ? 1220 : 1600; // lift above the fists during the meet
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
// Sound
// ======================================================================
const SFX: [string, number, number, number?][] = [
  ["thock", W.okay + 0.1, 0.55], ["slam", W.robot, 0.3],
  ["thock", W.deakin, 0.45], ["whip", W.mine, 0.35], ["whip", W.openDayEnd, 0.25],
  ["pop", W.api, 0.4], ["pop", W.robot2, 0.4], ["clap", W.meet, 0.5], ["thock", W.meet + 0.05, 0.4],
  ["tada", W.handsUp, 0.55],
  ["echo_right", W.right, 0.75], ["thock", W.right + 0.02, 0.35],
  ["whip", W.then, 0.4], ["ding", W.hundred2, 0.45], ["thock", W.hundred2 + 0.05, 0.4],
  ["thock", W.matchfeel, 0.4], ["thock", W.matchfeel + 0.75, 0.25], ["thock", W.matchfeel + 1.5, 0.25], ["thock", W.matchfeel + 2.25, 0.25],
  ["whip", W.anyways, 0.4], ["whip", W.myRobot, 0.3], ["whip", W.brollEnd, 0.25], ["slam", W.built, 0.35],
  ["whip", W.leave - 0.12, 0.35], ["whoosh", W.leave + 0.25, 0.6], ["sparkle", W.handsUp + 0.1, 0.3], ["whoosh", W.robot, 0.3], ["pop", W.yet, 0.3], ["slam", W.name, 0.3], ["whip", W.more, 0.3], ["ding2", W.watching, 0.5],
];
const MUSIC = "music/pixel_peeker_polka_faster.mp3";
const MUSIC_VOL = 0.085;

// ======================================================================
export const Infosys: React.FC = () => {
  const frame = useCurrentFrame();
  const t = toTrack(frame / FPS);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <PhoneBack t={t} />
      <AbsoluteFill style={phoneStyle(t)}>
      <AbsoluteFill style={cameraStyle(t)}>
        <OffthreadVideo muted src={staticFile("th/track.mp4")} />
        <Meet t={t} />
      </AbsoluteFill>
      </AbsoluteFill>
      <Rally t={t} />
      <RobotOut t={t} />
      <SplitBroll t={t} />
      <Court t={t} />
      <MemeText t={t} />
      <NameTag t={t} />
      <Score t={t} />
      <Captions t={t} />
      <EndCard t={t} />

      {/* voice; the echo of "right" rings over the real stare that follows it */}
      <Audio src={staticFile("th/track.mp4")} />

      {/* Music: Pixel Peeker Polka (faster), Kevin MacLeod, CC BY 4.0. Stops dead on "right",
          back on "Then it worked", dips under the ML line, up on the end card, fades out. */}
      <Sequence from={F(0.3)} durationInFrames={F(W.right) - F(0.3)}>
        <Audio src={staticFile(MUSIC)} volume={MUSIC_VOL} />
      </Sequence>
      <Sequence from={F(W.then)}>
        <Audio src={staticFile(MUSIC)} startFrom={F(W.right) - F(0.3)}
          volume={(f) => {
            const tt = toTrack((F(W.then) + f) / FPS);
            const dip = tt >= W.mlStart && tt < W.mlEnd ? 0.45 : 1;
            const end = tt >= W.endCard ? 1.8 : 1;
            const fade = interpolate(F(W.then) + f, [TOTAL_FRAMES - 30, TOTAL_FRAMES - 1], [1, 0], clamp);
            return MUSIC_VOL * dip * end * fade;
          }} />
      </Sequence>
      {SFX.map(([name, at0, vol, max], i) => (
        <Sequence key={i} from={F(at0)} durationInFrames={max ? Math.round(max * FPS) : undefined}>
          <Audio src={staticFile(`sfx/${name}.wav`)} volume={vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
