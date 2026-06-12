---
name: clipper-thumbnail-generation
description: Generate AI thumbnails for clips using Google Nano Banana Pro
version: 1.0.0
author: nplusm-Clippy
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [Video, ClipIt, Thumbnail, AI, Image Generation, Nano Banana Pro]
  hermes:
    tags: [Video, ClipIt, Thumbnail, AI, Image Generation, Nano Banana Pro]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: CLIPPER_API_KEY
    prompt: "Enter your ClipIt API key"
    help: "Get one at https://clipit.dev -> Settings -> API Keys -> Quick Connect"
    required_for: "ClipIt API access"
---

# ClipIt Thumbnail Generation

## When to Use

Use this skill when the user wants to:
- Generate an AI thumbnail for a clip (enhances a frame from the clip)
- Generate a standalone thumbnail from a text prompt
- Get a specific style, mood, or text overlay on their thumbnail

Powered by Google Nano Banana Pro — supports 4K resolution, accurate text rendering, and reference image composition.

Use the account-insights skill before generation when the user is cost-sensitive: check balance with `get_credits_balance.py` and estimate with `estimate_cost.py` when provider/model metrics are known.

## Quick Reference

| Operation | Script | Cost |
|-----------|--------|------|
| Generate for clip | `generate_thumbnail.py --clip-id <id> --prompt "..." [--wait]` | ~19.5 $CLIP |
| Generate standalone | `generate_thumbnail.py --prompt "..." [--wait]` | ~19.5 $CLIP |

## Procedure

### Generating a Thumbnail for a Clip

**When to use:** The user has a clip and wants a scroll-stopping thumbnail.

**Steps:**
1. Run `python scripts/generate_thumbnail.py --clip-id <id> --prompt "description" --wait`
2. When `clipId` is provided, the system extracts a frame from the clip and uses it as the image-to-image edit base
3. The result includes the generated thumbnail URL
4. The thumbnail is automatically linked to the clip

**Prompt engineering tips:**
- Be specific about lighting: "golden hour side-lighting", "dramatic rim light"
- Include composition: "rule of thirds", "centered subject", "negative space on left for text overlay"
- For text in thumbnails: include the exact text in quotes, e.g., `--prompt 'shocked face reacting, text: "YOU WON'T BELIEVE THIS"'`
- For YouTube: emphasize facial expressions, high contrast, bold text overlays
- Quality keywords: "cinematic lighting, professional photograph, sharp focus, vibrant colors"
- Keep prompts under 500 characters

**Example:**
```bash
python scripts/generate_thumbnail.py \
  --clip-id clip_xyz \
  --prompt 'excited person reacting with wide eyes, dramatic rim lighting, text: "INSANE PLAY", bold red and white composition, YouTube thumbnail style' \
  --aspect-ratio 16:9 \
  --resolution 4K \
  --wait
```

### Generating a Standalone Thumbnail

**When to use:** The user wants a thumbnail image that isn't based on an existing clip frame.

**Steps:**
1. Run `python scripts/generate_thumbnail.py --prompt "description" --wait` (no `--clip-id`)
2. This produces a pure text-to-image generation
3. The result includes the generated image URL

## Pitfalls

- **19.5 $CLIP per generation.** This is the most expensive per-image operation. Check account-insights first and don't generate multiple variants unless the user asks.
- **Aspect ratio matters.** YouTube thumbnails should be `16:9`, TikTok profile images `1:1`. Default is `16:9`.
- **Text rendering works but isn't perfect.** Keep text short (1-5 words) for best results. Nano Banana Pro handles text better than most models, but very long text may still have artifacts.
- **The prompt should describe what you WANT, not what you don't want.** Positive descriptions only.

## Verification

- **Generation succeeded:** Job status is `completed` and `result.url` is a valid image URL
- **Thumbnail linked to clip:** The clip's `thumbnailUrl` field is updated (check with `get_clip.py`)
- **Image is correct size:** The URL returns an image matching the requested aspect ratio
