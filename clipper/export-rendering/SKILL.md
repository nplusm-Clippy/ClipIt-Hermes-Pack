---
name: clipper-export-rendering
description: Start, wait for, and download ClipIt export rendering jobs
version: 1.0.0
author: nplusm-Clippy
license: MIT
platforms: [macos, linux, windows]
metadata:
  tags: [Video, ClipIt, Export, Render, Download, Remotion]
  hermes:
    tags: [Video, ClipIt, Export, Render, Download, Remotion]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: CLIPPER_API_KEY
    prompt: "Enter your ClipIt API key"
    help: "Get one at https://clipit.dev -> Settings -> API Keys -> Connect an Agent"
    required_for: "ClipIt API access"
---

# ClipIt Export Rendering

## When to Use

Use this skill when the user wants to:
- Export a clip as a downloadable media file
- Choose export format, aspect ratio, resolution, bitrate, codec, or audio options
- Poll a running export job
- Get a fresh signed download URL for a completed export

Exports are separate from generic jobs. Always poll export jobs with `GET /api/v1/exports/{jobId}` via `wait_for_export.py`, not `wait_for_job.py`.

## Quick Reference

| Operation | Script | Cost |
|-----------|--------|------|
| Start export | `start_export.py --clip-id <id> [--start 0] [--end 30] [--format mp4]` | Varies |
| Wait for export | `wait_for_export.py --job-id <exportJobId>` | Free |
| Download export | `download_export.py --job-id <exportJobId>` | Free |

## Procedure

### Starting an Export

**When to use:** The user wants a finished media file with specific export settings.

**Steps:**
1. Use account-insights first: `python scripts/get_credits_balance.py`
2. When duration is known, estimate render/export cost:
   ```bash
   python scripts/estimate_cost.py \
     --operation-type lambda_render \
     --provider aws_lambda \
     --model-id remotion-4.0 \
     videoSeconds=30
   ```
3. Run `python scripts/start_export.py --clip-id <id> --start 0 --end 30 --format mp4 --aspect-ratio 9:16 --wait`
4. If you omit `--wait`, save the returned `exportJobId`

**Common options:**
- `--format` — `mp4`, `mov`, `avi`, `webm`, `mkv`
- `--aspect-ratio` — `original`, `16:9`, `9:16`, `1:1`, `4:3`, `4:5`, `2:3`
- `--resolution` — `2160p`, `1080p`, `720p`, `480p`, `360p`, `original`
- `--bitrate`, `--framerate`, `--codec`, `--quality-preset` — quality settings
- `--include-audio` / `--no-audio` — include or omit audio
- `--options-json` — pass advanced exportStart schema fields as a JSON object

### Waiting for an Export

**When to use:** `start_export.py` returned an `exportJobId` and the export is still pending or processing.

**Steps:**
1. Run `python scripts/wait_for_export.py --job-id <exportJobId>`
2. The script polls `/api/v1/exports/{jobId}` until status is `completed`, `failed`, or `cancelled`
3. On success, the result includes export metadata and output details

### Downloading an Export

**When to use:** Export status is `completed` and the user needs a fresh signed URL.

**Steps:**
1. Run `python scripts/download_export.py --job-id <exportJobId>`
2. Use the returned `downloadUrl` before it expires
3. If the URL expires, run the script again for a fresh one

## Error Handling

- **402 insufficient credits / spend limit.** Stop and use account-insights. The user needs more $CLIP or a higher API-key spend limit.
- **409 premature download.** The export is not completed yet. Run `wait_for_export.py` and retry download after completion.
- **404 export not found.** Check the `exportJobId` and that it belongs to the same API key owner.
- **Failed export.** Inspect the error returned by `wait_for_export.py`; source media issues may require re-rendering or choosing different export settings.

## Verification

- **Export started:** Response includes `exportJobId`, `status`, and `pollUrl`
- **Export completed:** `wait_for_export.py` returns `status: "completed"`
- **Download URL available:** `download_export.py` returns `downloadUrl`
- **Correct poller used:** Export jobs are never polled with `wait_for_job.py`
