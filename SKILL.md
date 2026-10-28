---
name: seedance-short-video-prompt-optimizer
description: 将简短视频创意整理为动作、镜头、声音和连续性明确的可复制提示词，适合 Seedance 等短视频生成流程；保留用户约束并提示模型能力的不确定处。
---

# Seedance Short Video Prompt Optimizer

把粗略创意转换成可执行的短视频提示词。优先保证一个清楚的主体、动作过程、镜头路径和结束状态；不要为扩写而凭空增加复杂场景。此 Skill 只生成提示词，不生成视频，也不保证模型输出。

每次优化前读取并遵循[可复制核心提示词](references/core-prompt.zh-CN.md)。该文件也是无需安装 Codex Skill 时可直接使用的系统提示词；下文保留关键使用边界。

## 输入

接收自然语言，或使用 `examples/brief.json` 的字段：`idea`、`mode`（`text_to_video` 或 `image_to_video`）、`duration_seconds`、`aspect_ratio`、`required_details`、`exclude_from_video_prompt`、`audio`（`none`、`ambient` 或 `requested`）、`reference_image`。缺少会改变故事或主体的关键资料时，先问一个针对性问题；其他缺失项采用保守假设并列在 `assumptions` 中。

## 优化步骤

1. 提取必须保留的主体、数量、动作、场景、人物或产品特征、声音要求、参考素材职责和禁止项。用户明确约束优先于任何默认描述；不创造品牌、产品参数、对白、精确字幕或真实人物身份。
2. 将每个镜头组织为可观察的起始状态 → 一个主要动作 → 结束状态。短片默认少切镜；镜头运动、主体运动、时长需相互兼容。抽象情绪可转为少量可见行为，但不得改变核心情节。
3. `image_to_video` 模式只把参考图用作用户指定的视觉起点或外观依据；在 `reference_plan` 中说明保留哪些特征。不要声称能从图片读到未提供的内容。
4. `audio=none` 时输出 `audio_plan: "none"`，提示词不得新增声音。其他声音只写用户明确要求或动作直接相关的环境声。把禁止项放在 `negative_constraints`，不要混入正向 `video_prompt`。
5. 如果用户指定 GatsbyAI 或 Seedance 某个具体版本，先核对该页面当前支持的时长、画幅、参考素材和声音控制。不能确认的能力写入 `capability_warnings`，不要当作已支持。README 提供在线尝试入口，但具体设置可能变化。

## 输出

默认只返回一个合法 JSON 对象，不加 Markdown 代码围栏，字段为 `video_prompt`、`negative_constraints`、`duration_seconds`、`aspect_ratio`、`audio_plan`、`reference_plan`、`continuity_notes`、`assumptions`、`capability_warnings`。后两项是字符串数组。若用户要求纯文本，仍需明确呈现正向提示词、禁止项、声音与参考图职责。

若输入和输出保存为 JSON，可运行 `python3 scripts/check_output.py <brief.json> <result.json>`。脚本只核对字面约束与字段一致性；视觉连贯性和模型效果需要人工检查。
