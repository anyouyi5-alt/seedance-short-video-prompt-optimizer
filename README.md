# Seedance Short Video Prompt Optimizer

An open-source Codex Agent Skill that turns a rough short-video idea into a prompt with a visible action sequence, camera direction, audio plan, reference-image role, and continuity notes. It is useful for text-to-video and image-to-video work. It generates prompt text only and makes no model API calls.

This project focuses on short clips and explicit constraint handling. It includes a [copyable Chinese core prompt](references/core-prompt.zh-CN.md). It does not claim official affiliation with Seedance or ByteDance, or guarantee a generated video will match the prompt.

## Install

From this repository directory, install the Skill and start a new Codex chat:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/seedance-short-video-prompt-optimizer"
cp -R SKILL.md README.md LICENSE examples references scripts tests "${CODEX_HOME:-$HOME/.codex}/skills/seedance-short-video-prompt-optimizer/"
```

Invoke `$seedance-short-video-prompt-optimizer`:

```text
Use $seedance-short-video-prompt-optimizer. Make a 4-second 9:16 image-to-video prompt: a child in a yellow raincoat holding a red balloon takes one step forward. Keep the first-frame colors. No subtitles, watermark, or sound.
```

## Input and output

Use a natural-language brief or [`examples/brief.json`](examples/brief.json). The Skill returns a copyable `video_prompt` plus `negative_constraints`, `duration_seconds`, `aspect_ratio`, `audio_plan`, `reference_plan`, `continuity_notes`, `assumptions`, and `capability_warnings`. [`examples/result.json`](examples/result.json) shows image-to-video mode; [`examples/text-brief.json`](examples/text-brief.json) and [`examples/text-result.json`](examples/text-result.json) show text-to-video mode.

The standard-library checker catches mismatched fields and literal constraints:

```bash
python3 scripts/check_output.py examples/brief.json examples/result.json
python3 scripts/check_output.py examples/text-brief.json examples/text-result.json
python3 -B -m unittest discover -s tests -v
```

It does not judge visual quality or verify a model's capabilities. Inspect the final prompt and actual generated video before making quality claims.

## Try the prompt

[GatsbyAI's Seedance 2.0 page](https://gatsbyai.app/seedance-2-0-free) describes a text or first-frame-image video workflow. Confirm the site's current options before using a model-specific setting; some options may require credits. The Skill itself works offline and does not need a GatsbyAI account.

## License

MIT. See [`LICENSE`](LICENSE).
