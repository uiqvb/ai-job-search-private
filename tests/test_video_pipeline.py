"""Unit tests for the intro-video pipeline helpers (tools/video/).

They need numpy (the pipeline's own dependency); CI images without it skip them.
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools" / "video"))

try:
    import numpy as np
    import vlib
    import prep
    import render_cut
    HAVE_NUMPY = True
except ImportError:  # pragma: no cover
    HAVE_NUMPY = False


def W(text, start=0.0, step=0.3):
    return [{"w": w, "s": round(start + i * step, 3), "e": round(start + i * step + 0.25, 3)} for i, w in enumerate(text.split())]


@unittest.skipUnless(HAVE_NUMPY, "numpy not installed")
class TokenTests(unittest.TestCase):
    def test_tokens_drop_stage_directions_and_normalise(self):
        self.assertEqual(vlib.tokens("Then it WORKED, 100 out of 100 [grin] (beat)"),
                         ["then", "it", "worked", "hundred", "out", "of", "hundred"])

    def test_resolve_word_phrase_nth_and_edges(self):
        words = W("so I made them meet and they did meet")
        self.assertEqual(vlib.resolve({"word": "meet"}, words), words[4]["s"])
        self.assertEqual(vlib.resolve({"word": "meet", "n": 2}, words), words[8]["s"])
        self.assertEqual(vlib.resolve({"word": "made them meet", "edge": "e"}, words), words[4]["e"])
        self.assertAlmostEqual(vlib.resolve({"word": "made", "offset": 0.1}, words), words[2]["s"] + 0.1)
        self.assertEqual(vlib.resolve(3.5, words), 3.5)
        with self.assertRaises(ValueError):
            vlib.resolve({"word": "robot"}, words)


@unittest.skipUnless(HAVE_NUMPY, "numpy not installed")
class AttemptTests(unittest.TestCase):
    def test_finds_every_attempt_of_a_repeated_line(self):
        take = ("okay infosys at the australian open you brought a robot um sorry "
                "okay infosys at the australian open you brought a robot to the fan zone "
                "i brought mine to deakin open day")
        words = W(take)
        line = vlib.tokens("Okay, Infosys. At the Australian Open, you brought a robot to the Fan Zone.")
        found = prep.find_attempts(line, words)
        starts = sorted(words[i]["w"] + str(i) for _, i, _ in found)
        self.assertEqual(len(found), 2, found)
        self.assertIn("okay0", starts)
        self.assertIn("okay12", starts)

    def test_attempt_never_spans_a_long_silence(self):
        words = W("i brought mine to") + W("deakin open day", start=40.0)
        found = prep.find_attempts(vlib.tokens("I brought mine to Deakin Open Day"), words)
        for _, i, n in found:
            self.assertLess(words[i + n - 1]["s"] - words[i]["s"], 10)


@unittest.skipUnless(HAVE_NUMPY, "numpy not installed")
class SnapTests(unittest.TestCase):
    def setUp(self):
        # 3 s envelope: silence, speech from 1.00 to 2.00 s, silence (10 ms frames)
        self.env = np.full(300, -70.0)
        self.env[100:200] = -20.0
        self.thr = -45.0

    def test_onset_inside_silence_moves_forward_to_the_first_sound(self):
        self.assertAlmostEqual(render_cut.snap_edge(self.env, self.thr, 0.80, True), 1.00, places=2)

    def test_onset_inside_speech_moves_back_to_the_silence(self):
        self.assertAlmostEqual(render_cut.snap_edge(self.env, self.thr, 1.20, True), 1.00, places=1)

    def test_offset_inside_speech_moves_forward_to_the_end(self):
        self.assertAlmostEqual(render_cut.snap_edge(self.env, self.thr, 1.80, False), 2.00, places=1)

    def test_offset_in_silence_moves_back_to_the_last_sound(self):
        self.assertAlmostEqual(render_cut.snap_edge(self.env, self.thr, 2.30, False), 2.00, places=2)


@unittest.skipUnless(HAVE_NUMPY, "numpy not installed")
class EditorGuardTests(unittest.TestCase):
    def test_setup_refuses_to_overwrite_a_hand_made_editor(self):
        import setup_editor
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        (root / "Raw Takes").mkdir()
        (root / "editor" / "src").mkdir(parents=True)
        (root / "editor" / "src" / "Video.tsx").write_text("// hand-made Infosys editor", encoding="utf-8")
        (root / "project.json").write_text(json.dumps({"company": "T", "lines": []}), encoding="utf-8")
        with self.assertRaises(SystemExit) as cm:
            setup_editor.main(root)
        self.assertIn("refusing to overwrite", str(cm.exception))
        self.assertEqual((root / "editor" / "src" / "Video.tsx").read_text(encoding="utf-8"), "// hand-made Infosys editor")


@unittest.skipUnless(HAVE_NUMPY, "numpy not installed")
class PlanResolverTests(unittest.TestCase):
    def test_named_anchors_with_offsets(self):
        try:
            import build_plan
        except ImportError:
            self.skipTest("opencv/scipy not installed")
        words = W("and for a month he was right then it worked")
        r = build_plan.Resolver(words, {"right": {"word": "right"}})
        self.assertEqual(r("@right"), words[6]["s"])
        self.assertAlmostEqual(r("@right+0.7"), words[6]["s"] + 0.7)
        self.assertAlmostEqual(r("@right - 0.2"), words[6]["s"] - 0.2)
        with self.assertRaises(ValueError):
            r("@nope")


if __name__ == "__main__":
    unittest.main()
