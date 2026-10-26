import React from "react";
import { Composition } from "remotion";
import { Intro, TOTAL_FRAMES, FPS } from "./Video";

export const Root: React.FC = () => (
  <Composition id="Intro" component={Intro} durationInFrames={TOTAL_FRAMES} fps={FPS} width={1080} height={1920} />
);
