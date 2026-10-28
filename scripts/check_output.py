"""Check explicit, literal constraints in a short-video prompt result."""

import json
import sys
import unicodedata
from pathlib import Path


def normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def string_list(value: object, field: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        errors.append(f"{field} must be an array of non-empty strings")
        return []
    return value


def validate(brief: object, result: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(brief, dict) or not isinstance(result, dict):
        return ["brief and result must both be JSON objects"]

    mode = brief.get("mode")
    if mode not in ("text_to_video", "image_to_video"):
        errors.append("mode must be text_to_video or image_to_video")

    expected_duration = brief.get("duration_seconds")
    if (
        isinstance(expected_duration, bool)
        or not isinstance(expected_duration, int)
        or expected_duration <= 0
    ):
        errors.append("duration_seconds must be a positive integer")
    actual_duration = result.get("duration_seconds")
    if isinstance(actual_duration, bool) or not isinstance(actual_duration, int):
        errors.append("result.duration_seconds must be an integer")
    elif actual_duration != expected_duration:
        errors.append("result.duration_seconds differs from brief.duration_seconds")

    expected_ratio = brief.get("aspect_ratio")
    if not isinstance(expected_ratio, str) or not expected_ratio.strip():
        errors.append("brief.aspect_ratio must be a non-empty string")
    actual_ratio = result.get("aspect_ratio")
    if not isinstance(actual_ratio, str):
        errors.append("result.aspect_ratio must be a string")
    elif actual_ratio != expected_ratio:
        errors.append("result.aspect_ratio differs from brief.aspect_ratio")

    prompt = result.get("video_prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        errors.append("video_prompt must be a non-empty string")
        prompt = ""
    negative = result.get("negative_constraints")
    if not isinstance(negative, str):
        errors.append("negative_constraints must be a string")
        negative = ""

    audio = brief.get("audio")
    if audio not in ("none", "ambient", "requested"):
        errors.append("audio must be none, ambient, or requested")
    audio_plan = result.get("audio_plan")
    if not isinstance(audio_plan, str) or not audio_plan.strip():
        errors.append("audio_plan must be a non-empty string")
    elif audio == "none" and audio_plan != "none":
        errors.append("audio_plan must be none when brief.audio is none")

    reference_plan = result.get("reference_plan")
    if not isinstance(reference_plan, str):
        errors.append("reference_plan must be a string")
    elif mode == "image_to_video" and not reference_plan.strip():
        errors.append("image_to_video requires reference_plan")
    reference_image = brief.get("reference_image")
    if mode == "image_to_video" and (
        not isinstance(reference_image, str) or not reference_image.strip()
    ):
        errors.append("image_to_video requires non-empty brief.reference_image")

    continuity = result.get("continuity_notes")
    if not isinstance(continuity, str) or not continuity.strip():
        errors.append("continuity_notes must be a non-empty string")
    string_list(result.get("assumptions"), "assumptions", errors)
    string_list(result.get("capability_warnings"), "capability_warnings", errors)

    required = string_list(brief.get("required_details", []), "required_details", errors)
    excluded = string_list(
        brief.get("exclude_from_video_prompt", []), "exclude_from_video_prompt", errors
    )
    prompt_key = normalized(prompt)
    negative_key = normalized(negative)
    for phrase in required:
        if normalized(phrase) not in prompt_key:
            errors.append(f"required detail missing from video_prompt: {phrase}")
    for phrase in excluded:
        key = normalized(phrase)
        if key in prompt_key:
            errors.append(f"excluded detail appears in video_prompt: {phrase}")
        if key not in negative_key:
            errors.append(f"excluded detail missing from negative_constraints: {phrase}")
    return errors


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: python3 scripts/check_output.py <brief.json> <result.json>", file=sys.stderr)
        return 2
    try:
        brief = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"cannot read input: {exc}", file=sys.stderr)
        return 2
    errors = validate(brief, result)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: explicit short-video prompt constraints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
