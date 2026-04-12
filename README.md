# ClipIt Hermes Skills Pack

Hermes agent skills for [ClipIt](https://clipit.dev) — an AI-powered video clipping platform that turns long-form video into short viral content.

## What You Can Do

With these skills installed, your Hermes agent can:

- **Import videos** from YouTube, Vimeo, Twitch, or direct file upload
- **Transcribe** videos with word-level timing and speaker diarization (Deepgram Nova-3)
- **Find viral moments** in transcripts using AI (Grok 4.20 with 2M context)
- **Create and edit clips** with precise start/end timing
- **Render clips** as downloadable videos with captions, aspect ratio, and quality control (AWS Lambda + Remotion)
- **Generate thumbnails** with Google Nano Banana Pro (4K, text rendering, image-to-image editing)
- **Generate B-Roll** overlays with Flux 2 Max (image) + Veo 3.1 (video), including start/end frame interpolation
- **Style captions** with presets (bold, neon, minimal, classic, tiktok-viral) or custom fonts/colors
- **Publish** clips to 13 social platforms (YouTube, TikTok, Instagram, Facebook, LinkedIn, Twitter/X, Bluesky, Threads, Pinterest, Reddit, Telegram, Snapchat, Google Business)
- **Schedule** social posts for future publication

## Quick Start

### 1. Get your API key

Go to [clipit.dev](https://clipit.dev) > **Settings** > **API Keys** > **Quick Connect**

This creates a key with all the right permissions and gives you a ready-to-paste setup prompt.

### 2. Install the skills

```bash
hermes skills tap add nplusm-Clippy/ClipIt-Hermes-Pack

hermes skills install clipper/video-management
hermes skills install clipper/clip-creation
hermes skills install clipper/thumbnail-generation
hermes skills install clipper/caption-generation
hermes skills install clipper/broll-generation
hermes skills install clipper/social-publishing
```

### 3. Set your credentials

Add to your Hermes environment (`~/.hermes/.env` or equivalent):

```bash
CLIPPER_API_KEY=clipper_your_key_here
CLIPPER_BASE_URL=https://clipit.dev
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify

Ask your Hermes agent:

> "List my ClipIt videos"

If it returns your video library (even empty), you're connected.

## Usage Examples

Just tell your Hermes agent what you want in natural language:

**Full production pipeline:**
> "Take this YouTube video https://youtube.com/watch?v=..., find the three funniest moments, render them for TikTok with neon captions, generate thumbnails, and post them to TikTok and Instagram"

**Quick clip:**
> "Import this video and create a clip from 1:30 to 2:15 with the title 'Best moment'"

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

## Permissions

Each skill requires specific API key permissions. The **Quick Connect** button in ClipIt settings pre-selects all of them.

| Skill | Required Permissions |
|-------|---------------------|
| video-management | `file_upload`, `url_extraction`, `video_processing`, `transcription` |
| clip-creation | `clip_generation` |
| thumbnail-generation | `thumbnail_generation` |
| caption-generation | `caption_generation` |
| broll-generation | `broll_generation` |
| social-publishing | `social_publishing` |

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
| Lambda render | Varies by clip duration and quality |

Check your balance in the ClipIt web app or via the API.

## Async Operations

Long-running operations (video import, rendering, B-Roll generation) return a `jobId`. The scripts handle polling automatically when you use the `--wait` flag. Without `--wait`, use `wait_for_job.py` to poll:

```bash
python scripts/wait_for_job.py --job-id job_abc123
```

If you've configured a **webhook URL** on your API key, ClipIt will POST a `job.completed` or `job.failed` event when the job finishes.

## API Documentation

Full REST API reference with interactive Swagger UI:
**https://clipit.dev/api/v1/docs**

OpenAPI 3.1 spec:
**https://clipit.dev/api/v1/openapi.json**

## Support

- Issues: https://github.com/nplusm-Clippy/ClipIt-Hermes-Pack/issues
- ClipIt: https://clipit.dev
- API docs: https://clipit.dev/api/v1/docs

## License

MIT
