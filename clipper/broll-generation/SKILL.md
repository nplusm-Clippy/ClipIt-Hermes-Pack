---
name: clipper-broll-generation
description: Plan and generate AI B-Roll video overlays using Flux 2 Max + Veo 3.1
version: 1.0.0
author: nplusm-Clippy
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [Video, ClipIt, B-Roll, AI Video, Flux, Veo, Visual Effects, Overlay]
  hermes:
    tags: [Video, ClipIt, B-Roll, AI Video, Flux, Veo, Visual Effects, Overlay]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: CLIPPER_API_KEY
    prompt: "Enter your ClipIt API key"
    help: "Get one at https://clipit.dev -> Settings -> API Keys -> Quick Connect"
    required_for: "ClipIt API access"
---

# ClipIt B-Roll Generation

## When to Use

Use this skill when the user wants to:
- Add visual B-Roll overlays to a clip (stock-footage-style AI-generated video)
- Plan multiple B-Roll concepts for a clip before committing to generation
- Create transition effects between scenes using start/end frame interpolation

B-Roll is generated in two stages:
1. **Image generation** (Flux 2 Max) — creates the visual frame(s)
2. **Video generation** (Veo 3.1) — animates the frame into a 4-8 second video clip

This is the most expensive operation. Use account-insights for a balance/cost preflight, plan first, and generate only what the user approves.

## Quick Reference

| Operation | Script | Cost |
|-----------|--------|------|
| Plan concepts | `plan_broll.py --clip-id <id> [--count 3]` | ~5 $CLIP |
| Generate B-Roll | `generate_broll.py --clip-id <id> --start <s> --end <s> [--wait]` | ~220-420 $CLIP |

## Procedure

### Planning B-Roll Concepts

**When to use:** The user wants B-Roll ideas before spending credits on generation. Always recommend this step first, after checking credits with `get_credits_balance.py`.

**Steps:**
1. Run `python scripts/plan_broll.py --clip-id <id> --count 3 --wait`
2. The AI generates concept descriptions with image and video prompts for each
3. Present the concepts to the user and let them choose which to generate
4. Use the chosen concept's index with `generate_broll.py --concept-index N`

**Example:**
```bash
python scripts/plan_broll.py --clip-id clip_xyz --count 3 --theme "technology" --wait
```

### Generating B-Roll (Single Image Mode)

**When to use:** Standard B-Roll — one starting image animated into video. Best for atmosphere shots, slow reveals, ambient motion.

**Steps:**
1. Run `python scripts/generate_broll.py --clip-id <id> --start 10 --end 16 --prompt "city skyline at sunset, golden light, cinematic" --wait`
2. `--start` and `--end` define WHERE in the clip the B-Roll overlay appears (in seconds)
3. Generation takes 2-4 minutes (Flux image ~15s + Veo 3.1 video ~2-3 min)
4. The result includes both `imageUrl` (the generated frame) and `videoUrl` (the animated B-Roll)

### Generating B-Roll (Start/End Frame Mode)

**When to use:** When the B-Roll needs a clear visual transformation — sunrise to sunset, empty room to filled room, cause and effect. Creates more intentional, controlled motion.

**Steps:**
1. Run with `--mode start_end_frame` and REQUIRED `--end-frame-description`:
   ```bash
   python scripts/generate_broll.py --clip-id clip_xyz --start 10 --end 18 \
     --prompt "empty conference room, morning light, clean modern design" \
     --mode start_end_frame \
     --end-frame-description "same conference room now filled with people, active meeting, warm afternoon light" \
     --transition-description "smooth time-lapse transition from empty to full" \
     --duration 8 --wait
   ```
2. This generates TWO Flux images (start and end frame), then Veo 3.1 interpolates between them
3. Costs approximately 2x the image generation (two Flux calls) but the same video cost
4. `--transition-description` is optional but recommended — it tells Veo how to animate between frames

### Generation Options

- `--mode` — `single_image` (default) or `start_end_frame`
- `--duration` — `4` (quick cutaway), `6` (standard), or `8` (establishing shot) seconds
- `--with-audio` — include AI-generated audio (doubles the video generation cost)
- `--concept-index` — use a concept from `plan_broll.py` output (skips `--prompt`)
- `--prompt` — custom visual description (overrides planned concepts)

### Cost Breakdown

| Component | Cost |
|-----------|------|
| Flux 2 Max image (single_image) | ~9.1 $CLIP |
| Flux 2 Max images (start_end_frame) | ~18.2 $CLIP |
| Veo 3.1 video, 8s, no audio | ~208 $CLIP |
| Veo 3.1 video, 8s, with audio | ~416 $CLIP |
| **Total (typical, single_image, 8s, no audio)** | **~217 $CLIP** |
| **Total (start_end_frame, 8s, with audio)** | **~434 $CLIP** |

Always plan first, check account-insights, and confirm with the user before generating.

## Pitfalls

- **This is expensive.** A single B-Roll generation costs 200-400+ $CLIP. Always use account-insights and `plan_broll.py` first, then get user approval before generating.
- **Generation takes 2-4 minutes.** Use `--wait` to block, or poll the jobId. Don't timeout prematurely.
- **`start_end_frame` mode requires `--end-frame-description`.** Without it, the script will fail.
- **Keep motion prompts concise.** Veo 3.1 responds best to under 200 characters of motion description.
- **Duration affects cost.** 4-second clips are cheaper than 8-second clips. Use shorter durations for quick cutaways.
- **Re-render after adding B-Roll.** The B-Roll overlay is applied during the next clip render. Use `render_clip.py` after generating B-Roll.

## Verification

- **Plan succeeded:** Response contains a non-empty `concepts` array with `description`, `imagePrompt`, `videoPrompt` for each
- **Generation succeeded:** Job status is `completed` and result has both `imageUrl` and `videoUrl`
- **B-Roll visible in render:** After re-rendering the clip, the B-Roll appears at the specified start/end times
- **Start/end frame mode:** The video shows a clear visual transformation from start to end state
