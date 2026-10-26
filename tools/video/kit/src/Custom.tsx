// One-off gags for this video only (e.g. Infosys's tennis court or the phone shrink).
// The plan turns this on with "custom": true. t = seconds in the rough cut; W = resolved word anchors
// from the plan's "anchors" block; face(t) = [x, y, width] of his face in the 1080x1920 frame.
import React from "react";

export const Custom: React.FC<{ t: number; W: Record<string, number>; face: (t: number) => number[] }> = () => null;
