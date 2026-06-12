# ClipIt Agent Pack

Skills and Python script bindings for [ClipIt](https://clipit.dev), an AI-powered video clipping platform that turns long-form video into short viral content. This pack works with any agent framework that can read skill files and run CLI commands.

## What You Can Do

With these skills installed, your agent can:

- **Import videos** from YouTube, Vimeo, Twitch, or direct file upload
- **Transcribe** videos with word-level timing and speaker diarization (Deepgram Nova-3)
- **Find viral moments** in transcripts using AI (Grok 4.20 with 2M context)
- **Create and edit clips** with precise start/end timing
- **Render and export clips** as downloadable videos with captions, aspect ratio, format, codec, and quality control
- **Generate thumbnails** with Google Nano Banana Pro (4K, text rendering, image-to-image editing)
- **Generate B-Roll** overlays with Flux 2 Max (image) + Veo 3.1 (video), including start/end frame interpolation
- **Style captions** with presets (bold, neon, minimal, classic, tiktok-viral) or custom fonts/colors
- **Publish** clips to 13 social platforms (YouTube, TikTok, Instagram, Facebook, LinkedIn, Twitter/X, Bluesky, Threads, Pinterest, Reddit, Telegram, Snapchat, Google Business)
- **Check credits and estimate costs** before paid operations
- **Review analytics** across posts, platforms, and top clips
- **Upload and list assets** for logos, images, videos, audio, and overlays
- **Run agent orchestration workflows** with approval handling

## Quick Start

### 1. Get your API key

Go to [clipit.dev](https://clipit.dev) > **Settings** > **API Keys** > **Connect an Agent**.

This creates a key with the right permissions and gives you a ready-to-paste setup prompt.

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your credentials

Add these variables to the environment used by your agent:

```bash
CLIPPER_API_KEY=clipper_your_key_here
CLIPPER_BASE_URL=https://clipit.dev
```

### 4. Verify

Ask your agent:

> "List my ClipIt videos"

If it returns your video library, even empty, the connection is working.

## Works with Any Agent Framework

### Hermes

```bash
hermes skills tap add nplusm-Clippy/ClipIt-Agent-Pack

hermes skills install clipper/video-management
hermes skills install clipper/clip-creation
hermes skills install clipper/thumbnail-generation
hermes skills install clipper/caption-generation
hermes skills install clipper/broll-generation
hermes skills install clipper/social-publishing
hermes skills install clipper/account-insights
hermes skills install clipper/export-rendering
```

Add credentials to `~/.hermes/.env` or the equivalent environment file for that runtime.

### Claude Code, Codex, and Other CLI Agents

For the richer native setup path, install the ClipIt CLI:

```bash
npm install -g @clipit/cli
clipit agent install <target>
```

You can also clone this repository and point your agent at the skill files in `clipper/*/SKILL.md`.

### Any Agent Using Raw REST

Fetch current agent instructions directly:

```bash
python scripts/get_agent_instructions.py --target generic --format markdown
```

Agents can also call `GET /api/v1/agent/instructions?target=generic&format=markdown` and use the Python scripts in `scripts/` as thin REST bindings.

## Usage Examples

Just tell your agent what you want in natural language:

**Full production pipeline:**
> "Take this YouTube video https://youtube.com/watch?v=..., find the three funniest moments, render them for TikTok with neon captions, generate thumbnails, and post them to TikTok and Instagram"

**Quick clip:**
> "Import this video and create a clip from 1:30 to 2:15 with the title 'Best moment'"

**Cost preflight:**
> "Check my $CLIP balance and estimate the cost before rendering this 45-second clip"

**Export:**
> "Export clip_xyz as a 1080p MP4 in 9:16 and give me the download URL"

**Thumbnail:**
> "Generate a thumbnail for clip_xyz showing a shocked reaction face with the text 'INSANE PLAY' in bold red"

**B-Roll:**
> "Add a B-Roll overlay to clip_xyz from 10s to 16s showing a city skyline transitioning from day to night"

**Social:**
> "Post clip_xyz to TikTok and YouTube with the caption 'Best moment of 2026' and schedule it for tomorrow at 9am"

## Skills

| Skill | What It Does | Key Scripts |
|-------|-------------|-------------|
| [video-management](clipper/video-management/SKILL.md) | Import, upload, list, transcribe, delete videos | `import_video_from_url.py`, `transcribe_video.py`, `list_videos.py` |
| [clip-creation](clipper/clip-creation/SKILL.md) | AI clip suggestion, create, edit, render, download | `suggest_clips.py`, `create_clip.py`, `render_clip.py` |
| [thumbnail-generation](clipper/thumbnail-generation/SKILL.md) | Nano Banana Pro AI thumbnails | `generate_thumbnail.py` |
| [caption-generation](clipper/caption-generation/SKILL.md) | Word-level captions with style presets | `generate_captions.py`, `update_captions.py` |
| [broll-generation](clipper/broll-generation/SKILL.md) | Flux 2 + Veo 3.1 B-Roll video overlays | `plan_broll.py`, `generate_broll.py` |
| [social-publishing](clipper/social-publishing/SKILL.md) | Post/schedule to 13 platforms | `post_to_social.py`, `schedule_social_post.py` |
| [account-insights](clipper/account-insights/SKILL.md) | Credits, cost estimates, analytics | `get_credits_balance.py`, `estimate_cost.py`, `get_top_clips.py` |
| [export-rendering](clipper/export-rendering/SKILL.md) | Export jobs and download URLs | `start_export.py`, `wait_for_export.py`, `download_export.py` |

Additional script bindings include `upload_asset.py`, `list_assets.py`, `orchestrate.py`, `approve_workflow.py`, and `get_agent_instructions.py`.

## Permissions

Each skill requires specific API key permissions. The **Connect an Agent** button in ClipIt settings pre-selects the common agent permissions.

| Capability | Required Permissions |
|------------|---------------------|
| video-management | `file_upload`, `url_extraction`, `video_processing`, `transcription` |
| clip-creation | `clip_generation` |
| thumbnail-generation | `thumbnail_generation` |
| caption-generation | `caption_generation` |
| broll-generation | `broll_generation` |
| social-publishing | `social_publishing` |
| account-insights | API key access to credits and analytics endpoints |
| export-rendering | `clip_generation` |
| assets | `file_upload` |
| orchestration | `clippy_agent` |

## Credit Costs

Operations consume [$CLIP credits](https://clipit.dev). Same rates as the web UI:

| Operation | Cost |
|-----------|------|
| Video transcription | 1 $CLIP per minute of audio |
| AI clip suggestions (Grok 4.20) | ~5 $CLIP |
| Thumbnail generation (Nano Banana Pro) | ~19.5 $CLIP |
| Flux 2 Max image generation | ~9.1 $CLIP |
| Veo 3.1 video generation (8s, no audio) | ~208 $CLIP |
| Veo 3.1 video generation (8s, with audio) | ~416 $CLIP |
| Social post | 65 $CLIP per platform |
| Lambda render/export | Varies by clip duration and quality |

Check balance and estimates with:

```bash
python scripts/get_credits_balance.py
python scripts/estimate_cost.py --operation-type lambda_render --provider aws_lambda --model-id remotion-4.0 videoSeconds=45
```

## Async Operations

Long-running operations return IDs that must be polled. Generic jobs use `wait_for_job.py`:

```bash
python scripts/wait_for_job.py --job-id job_abc123
```

Export jobs use the export endpoint, not the generic jobs endpoint:

```bash
python scripts/wait_for_export.py --job-id export_abc123
```

If you've configured a **webhook URL** on your API key, ClipIt will POST completion or failure events when supported jobs finish.

## API Documentation

Full REST API reference with interactive Swagger UI:
**https://clipit.dev/api/v1/docs**

OpenAPI 3.1 spec:
**https://clipit.dev/api/v1/openapi.json**

## Support

- Issues: https://github.com/nplusm-Clippy/ClipIt-Agent-Pack/issues
- ClipIt: https://clipit.dev
- API docs: https://clipit.dev/api/v1/docs

## License

MIT
