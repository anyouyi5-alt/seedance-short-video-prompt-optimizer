"""Meaningful checks for the video prompt constraint validator."""

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_output import validate  # noqa: E402


class VideoPromptChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.brief = json.loads((ROOT / "examples/brief.json").read_text(encoding="utf-8"))
        cls.result = json.loads((ROOT / "examples/result.json").read_text(encoding="utf-8"))

    def test_example_satisfies_explicit_constraints(self) -> None:
        self.assertEqual(validate(self.brief, self.result), [])

    def test_text_to_video_example_satisfies_explicit_constraints(self) -> None:
        brief = json.loads((ROOT / "examples/text-brief.json").read_text(encoding="utf-8"))
        result = json.loads((ROOT / "examples/text-result.json").read_text(encoding="utf-8"))
        self.assertEqual(validate(brief, result), [])

    def test_missing_action_is_reported(self) -> None:
        result = copy.deepcopy(self.result)
        result["video_prompt"] = result["video_prompt"].replace("向前迈出一步", "向前移动")
        self.assertTrue(any("向前迈出一步" in error for error in validate(self.brief, result)))

    def test_forbidden_phrase_in_video_prompt_is_reported(self) -> None:
        result = copy.deepcopy(self.result)
        result["video_prompt"] += " 叠加字幕。"
        self.assertTrue(any("字幕" in error for error in validate(self.brief, result)))

    def test_no_audio_request_cannot_add_audio(self) -> None:
        result = copy.deepcopy(self.result)
        result["audio_plan"] = "rain ambience"
        self.assertTrue(any("audio_plan" in error for error in validate(self.brief, result)))

    def test_duration_must_match(self) -> None:
        result = copy.deepcopy(self.result)
        result["duration_seconds"] = 10
        self.assertTrue(any("duration_seconds" in error for error in validate(self.brief, result)))

    def test_image_mode_requires_reference_plan(self) -> None:
        result = copy.deepcopy(self.result)
        result["reference_plan"] = ""
        self.assertTrue(any("reference_plan" in error for error in validate(self.brief, result)))

    def test_image_mode_requires_reference_description(self) -> None:
        brief = copy.deepcopy(self.brief)
        brief["reference_image"] = " "
        self.assertTrue(any("reference_image" in error for error in validate(brief, self.result)))


if __name__ == "__main__":
    unittest.main()
