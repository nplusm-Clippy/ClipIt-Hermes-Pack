---
name: clipper-video-management
description: Upload, import, list, delete, and transcribe videos in ClipIt
version: 1.0.0
author: nplusm-Clippy
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [Video, ClipIt, Upload, Import, Transcription, YouTube, Vimeo]
  hermes:
    tags: [Video, ClipIt, Upload, Import, Transcription, YouTube, Vimeo]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: CLIPPER_API_KEY
    prompt: "Enter your ClipIt API key"
    help: "Get one at https://clipit.dev -> Settings -> API Keys -> Quick Connect"
    required_for: "ClipIt API access"
  - name: CLIPPER_BASE_URL
    prompt: "Enter the ClipIt base URL (default: https://clipit.dev)"
    default: "https://clipit.dev"
    required_for: "Routing API requests"
---

# ClipIt Video Management

## When to Use

Use this skill when the user wants to:
- Import a video from a URL (YouTube, Vimeo, Twitch, or any supported platform)
- Upload a local video file to their ClipIt library
- List or browse videos in their library
- Transcribe a video (word-level timestamps and speaker identification)
- Fetch an existing transcript
- Delete a video

This skill is typically the **first step** before using clip-creation, thumbnail-generation, or other ClipIt skills. Most workflows start here.

## Quick Reference

| Operation | Script | Permissions Needed |
|-----------|--------|--------------------|
| Import from URL | `import_video_from_url.py --url <url> [--wait]` | `url_extraction` |
| Upload local file | `upload_video.py --file <path> [--wait]` | `file_upload` |
| List videos | `list_videos.py [--limit N] [--offset N]` | `video_processing` |
| Get video details | `get_video.py --video-id <id>` | `video_processing` |
| Delete video | `delete_video.py --video-id <id>` | `video_processing` |
| Start transcription | `transcribe_video.py --video-id <id> [--wait]` | `transcription` |
| Fetch transcript | `get_transcript.py --video-id <id>` | `transcription` |

## Procedure

### Importing a Video from URL

**When to use:** The user provides a YouTube, Vimeo, Twitch, or other video URL they want to work with.

**Steps:**
1. Run `python scripts/import_video_from_url.py --url "<url>" --wait`
2. The script returns the completed job JSON with `result.videoId`
3. Save the `videoId` — you'll need it for transcription and clip creation

**Important notes:**
- YouTube imports use a residential proxy and can take 30-120 seconds depending on video length
- Age-restricted, region-locked, or live stream URLs will fail — the error explains why
- The `--wait` flag polls until complete. Without it, you get a `jobId` to poll manually with `wait_for_job.py`

**Example:**
```bash
python scripts/import_video_from_url.py --url "https://youtube.com/watch?v=dQw4w9WgXcQ" --wait
```

### Uploading a Local Video File

**When to use:** The user has a video file on their machine.

**Steps:**
1. Run `python scripts/upload_video.py --file /path/to/video.mp4 --wait`
2. The completed job contains `result.videoId`, `result.durationSeconds`, and `result.audioHealth`
3. If `audioHealth` is `silent` or `no_audio`, warn the user — transcription will produce empty results

**Example:**
```bash
python scripts/upload_video.py --file ~/Videos/interview.mp4 --wait
```

### Listing Videos

**When to use:** The user asks "what videos do I have?" or you need to find a video ID.

**Steps:**
1. Run `python scripts/list_videos.py`
2. Results are paginated — use `--limit` and `--offset` for large libraries
3. Each video shows: `id`, `title`, `durationSeconds`, `processingStatus`, `audioHealth`

### Transcribing a Video

**When to use:** Before using the clip-creation skill's `suggest_clips.py` (AI needs a transcript to find moments), or when the user asks for a transcript.

**Steps:**
1. First check if a transcript already exists: `python scripts/get_transcript.py --video-id <id>`
   - If it returns data, the transcript already exists — skip to next step
   - If it returns 404, proceed to transcribe
2. Trigger transcription: `python scripts/transcribe_video.py --video-id <id> --wait`
3. Transcription uses Deepgram Nova-3 and typically takes 10-60 seconds depending on video length
4. The transcript includes word-level timestamps and speaker diarization (when multiple speakers are detected)

**Cost:** 1 $CLIP per minute of audio.

### Deleting a Video

**When to use:** The user wants to remove a video and all its associated clips.

**Steps:**
1. Run `python scripts/delete_video.py --video-id <id>`
2. This cascades — all clips, thumbnails, and renders associated with the video are also deleted
3. This action is permanent and cannot be undone

## Pitfalls

- **Don't forget to wait for processing.** Video imports return a `jobId` — you MUST wait for completion before transcribing or creating clips. Use `--wait` or poll with `wait_for_job.py`.
- **Always transcribe before suggesting clips.** The `suggest_clips.py` script (in the clip-creation skill) requires a transcript to analyze. If no transcript exists, it will fail.
- **Don't re-transcribe** a video that already has a transcript — the API returns the existing one without re-running Deepgram, saving credits.
- **YouTube imports can fail** for age-restricted, region-locked, or live stream videos. Check the error message in the job result.
- **Large file uploads** (>2GB) may timeout. For very large videos, consider uploading to YouTube first and importing via URL.

## Verification

- **Import succeeded:** `job.status === "completed"` and `job.result.videoId` is a non-empty string
- **Transcription succeeded:** `get_transcript.py` returns 200 with a non-empty `segments` array
- **Video is ready for clipping:** it has BOTH a completed import AND a transcript
- **Delete succeeded:** `delete_video.py` prints confirmation and the video no longer appears in `list_videos.py`
