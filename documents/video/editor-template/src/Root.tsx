import React from "react";
import { Composition } from "remotion";
import { IntroVideo, RoughCut } from "./IntroVideo";
import timeline from "./timeline.json";

export const Root: React.FC = () => (
  <>
  <Composition
    id="RoughCut"
    component={RoughCut}
    durationInFrames={Math.round(timeline.endCardStart * timeline.fps)}
    fps={timeline.fps}
    width={1080}
    height={1920}
  />
  <Composition
    id="IntroVideo"
    component={IntroVideo}
    durationInFrames={Math.round(timeline.total * timeline.fps)}
    fps={timeline.fps}
    width={1080}
    height={1920}
  />
  </>
);
