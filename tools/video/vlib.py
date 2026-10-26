"""Shared helpers for the intro-video pipeline (tools/video/).

A video project is a folder, e.g. documents/video/<company>/, holding:
  project.json     script lines, raw folder, grade, music, end card (see README.md)
  Raw Takes/       one long take, or one file per line, or a mix
  pipeline/        everything the pipeline writes (transcripts, cuts, rough cut, reviews, plan)
  editor/          the Remotion editor for Phase 2 (made by setup_editor.py)
"""

import json
import os
import re
import subprocess
from pathlib import Path

import numpy as np

SR = 16000          # analysis sample rate
HOP = 0.01          # RMS frame step (s)
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm"}
REPO = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------- project
class Project:
    def __init__(self, folder):
        self.dir = Path(folder).resolve()
        cfg = self.dir / "project.json"
        if not cfg.exists():
            raise SystemExit(f"no project.json in {self.dir} (see tools/video/README.md)")
        self.cfg = json.loads(cfg.read_text(encoding="utf-8"))
        self.pipe = self.dir / "pipeline"
        self.pipe.mkdir(exist_ok=True)
        (self.pipe / "transcripts").mkdir(exist_ok=True)

    @property
    def name(self):
        return self.cfg.get("company", self.dir.name)

    @property
    def lines(self):
        return self.cfg["lines"]

    def raw_files(self):
        raw = self.dir / self.cfg.get("raw", "Raw Takes")
        files = sorted(p for p in raw.iterdir() if p.suffix.lower() in VIDEO_EXT)
        if not files:
            raise SystemExit(f"no video files in {raw}")
        return files

    @property
    def editor(self):
        """Remotion editor folder (project.json "editor", default editor/)."""
        return self.dir / self.cfg.get("editor", "editor")

    def raw(self, name):
        return self.dir / self.cfg.get("raw", "Raw Takes") / name

    def path(self, *parts):
        return self.pipe.joinpath(*parts)

    def read_json(self, *parts, default=None):
        p = self.path(*parts)
        if not p.exists():
            if default is not None:
                return default
            raise SystemExit(f"missing {p}")
        return json.loads(p.read_text(encoding="utf-8"))

    def write_json(self, data, *parts):
        p = self.path(*parts)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
        return p


# ---------------------------------------------------------------- ffmpeg
def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
               "-of", "json", str(path)]).stdout
    d = json.loads(out or "{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    return {"duration": float(d.get("format", {}).get("duration", 0)), "width": v.get("width"), "height": v.get("height")}


def audio(path, start=None, dur=None, sr=SR):
    """Mono float32 audio of a file (or a window of it)."""
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{max(0, start):.3f}"]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-i", str(path), "-vn", "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def rms_db(x, sr=SR, hop=HOP, win=0.03):
    """RMS envelope in dBFS, one value per hop."""
    h, w = int(sr * hop), int(sr * win)
    if len(x) < w:
        return np.array([-100.0])
    n = 1 + (len(x) - w) // h
    idx = np.arange(w)[None, :] + h * np.arange(n)[:, None]
    r = np.sqrt((x[idx] ** 2).mean(axis=1) + 1e-12)
    return 20 * np.log10(r + 1e-9)


def speech_threshold(env):
    """dB level that separates speech from room noise for this recording."""
    floor = np.percentile(env, 10)
    speech = np.percentile(env, 90)
    return max(floor + 10, speech - 28, -55)


def frame_at(path, t, w=270, h=480):
    """One frame (BGR uint8) at time t, scaled to w x h."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", str(path), "-frames:v", "1",
                          "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    if len(raw) < w * h * 3:
        return np.zeros((h, w, 3), np.uint8)
    return np.frombuffer(raw[: w * h * 3], np.uint8).reshape(h, w, 3).copy()


# ---------------------------------------------------------------- transcription
_MODEL = None


def transcribe(media, out_json, prompt="", model="medium", force=False):
    """Word-level transcript, cached next to out_json (re-run only when the media changes)."""
    media, out_json = Path(media), Path(out_json)
    stamp = f"{media.stat().st_size}-{int(media.stat().st_mtime)}"
    if out_json.exists() and not force:
        d = json.loads(out_json.read_text(encoding="utf-8"))
        if d.get("stamp") == stamp:
            return d["words"]
    global _MODEL
    if _MODEL is None:
        from faster_whisper import WhisperModel
        _MODEL = WhisperModel(model, device="cpu", compute_type="int8")
    wav = out_json.with_suffix(".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(media), "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    segs, _ = _MODEL.transcribe(str(wav), language="en", word_timestamps=True, vad_filter=False,
                                initial_prompt=prompt or None)
    words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 2)}
             for s in segs for w in s.words if w.word.strip()]
    out_json.write_text(json.dumps({"media": media.name, "stamp": stamp, "words": words}, indent=0), encoding="utf-8")
    wav.unlink(missing_ok=True)
    return words


NUM = {"100": "hundred", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "10": "ten"}


def norm(word):
    w = re.sub(r"[^a-z0-9']", "", word.lower().replace("’", "'"))
    return NUM.get(w, w)


def tokens(text):
    text = re.sub(r"\[.*?\]|\(.*?\)", " ", text)   # drop stage directions
    return [t for t in (norm(x) for x in text.split()) if t]


FILLERS = {"um", "uh", "erm", "ah", "hmm", "like"}


# ---------------------------------------------------------------- word anchors
def resolve(spec, words):
    """Time in the rough cut for an anchor.

    spec: a number (seconds) | {"t": 3.2} | {"word": "right", "n": 1, "edge": "s"|"e", "offset": 0.1}
    n counts matching words from the start (1 = first). "word" may be several words ("made them meet").
    """
    if isinstance(spec, (int, float)):
        return float(spec)
    if "t" in spec:
        return float(spec["t"]) + spec.get("offset", 0)
    want = tokens(spec["word"])
    toks = [norm(w["w"]) for w in words]
    n, hits = spec.get("n", 1), 0
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            hits += 1
            if hits == n:
                w = words[i] if spec.get("edge", "s") == "s" else words[i + len(want) - 1]
                return round(w[spec.get("edge", "s")] + spec.get("offset", 0), 3)
    raise ValueError(f"anchor not found in rough cut words: {spec}")
