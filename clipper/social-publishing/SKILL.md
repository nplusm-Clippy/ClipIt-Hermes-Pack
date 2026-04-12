---
name: clipper-social-publishing
description: Post and schedule clips to 13 social media platforms via ClipIt
version: 1.0.0
author: nplusm-Clippy
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [Video, ClipIt, Social Media, TikTok, YouTube, Instagram, Publishing, Scheduling]
    requires_toolsets: [terminal]
required_environment_variables:
  - name: CLIPPER_API_KEY
    prompt: "Enter your ClipIt API key"
    help: "Get one at https://clipit.dev -> Settings -> API Keys -> Quick Connect"
    required_for: "ClipIt API access"
---

# ClipIt Social Publishing

## When to Use

Use this skill when the user wants to:
- Post a rendered clip to social media immediately
- Schedule a clip for future posting
- Check the status of a published or scheduled post
- Cancel a scheduled post
- See which social accounts are connected

**Supported platforms:** YouTube, TikTok, Instagram, Facebook, LinkedIn, Twitter/X, Bluesky, Threads, Pinterest, Reddit, Telegram, Snapchat, Google Business.

**Prerequisite:** The clip MUST be rendered first (use `render_clip.py --wait` from the clip-creation skill). Social platforms need an actual video file, not just clip metadata.

**Account setup:** Social accounts are connected via the ClipIt web UI (Settings -> Social Accounts). The API cannot connect new accounts — only post through already-connected ones.

## Quick Reference

| Operation | Script | Cost |
|-----------|--------|------|
| List connected accounts | `list_social_accounts.py` | Free |
| Post immediately | `post_to_social.py --clip-id <id> --platforms tiktok --caption "..." [--wait]` | 65 $CLIP/platform |
| Schedule post | `schedule_social_post.py --clip-id <id> --platforms tiktok --caption "..." --scheduled-for <iso>` | Billed at post time |
| Check post status | `get_social_post.py --post-id <id>` | Free |
| Cancel scheduled post | `cancel_social_post.py --post-id <id>` | Free |

## Procedure

### Checking Connected Accounts

**When to use:** Before posting, verify which platforms the user has connected.

**Steps:**
1. Run `python scripts/list_social_accounts.py`
2. Each entry shows: `platform`, `connected` (true/false), `accountName`
3. If the user wants to post to a platform that isn't connected, direct them to https://clipit.dev/settings/social to connect it

### Posting a Clip Immediately

**When to use:** The user says "post this to TikTok" or "share on Instagram."

**Prerequisites:**
- The clip MUST be rendered (`renderStatus === 'completed'`). If not, render it first.
- The user MUST have the target platform(s) connected. Check with `list_social_accounts.py`.

**Steps:**
1. Verify the clip is rendered: `python scripts/get_clip.py --clip-id <id>` — check `renderStatus`
2. Run `python scripts/post_to_social.py --clip-id <id> --platforms tiktok,instagram --caption "Your caption here" --wait`
3. For YouTube, you MUST include `--title "Video Title"` — YouTube requires a separate title field
4. The result includes per-platform results (each platform may succeed or fail independently)

**Example:**
```bash
python scripts/post_to_social.py \
  --clip-id clip_xyz \
  --platforms tiktok,instagram,youtube \
  --caption "This is the best moment from today's stream! #viral #clips" \
  --title "INSANE PLAY - Best Moment" \
  --hashtags "viral,clips,gaming" \
  --wait
```

### Scheduling a Post

**When to use:** The user wants to post at a specific time (e.g., "post tomorrow at 9am").

**Steps:**
1. Run `python scripts/schedule_social_post.py --clip-id <id> --platforms tiktok --caption "..." --scheduled-for "2026-04-15T09:00:00Z"`
2. The `--scheduled-for` value MUST be in the future (ISO 8601 format with timezone)
3. Credits are NOT charged at scheduling time — they're charged when the post actually fires
4. The response includes a `postId` you can use to check status or cancel

### Checking Post Status

**When to use:** The user asks "did it post?" or you need to verify a post succeeded.

**Steps:**
1. Run `python scripts/get_social_post.py --post-id <id>`
2. Status values: `pending` → `posting` → `posted` (success) or `failed`
3. For scheduled posts: `scheduled` → `posting` → `posted` or `failed`
4. The `perPlatformResults` field shows success/failure per platform with individual post URLs

### Cancelling a Scheduled Post

**When to use:** The user wants to cancel a post before it goes out.

**Steps:**
1. Run `python scripts/cancel_social_post.py --post-id <id>`
2. Only works on `scheduled` or `pending` status — cannot cancel already-posted content
3. If the post was already sent to the scheduling queue, it's also cancelled there

## Pitfalls

- **Clip MUST be rendered.** The API returns `CLIP_NOT_RENDERED` if you try to post an unrendered clip. Always check with `get_clip.py` first.
- **YouTube requires `--title`.** If you're posting to YouTube without a title, the API returns 400. Always include `--title` when YouTube is in the platforms list.
- **65 $CLIP per platform per post.** Posting to 3 platforms costs 195 $CLIP. Confirm with the user before posting to many platforms.
- **Scheduled posts aren't free to cancel.** While no credits are charged until the post fires, cancelling at the last second might not work if the post is already in the posting queue.
- **Platform-specific character limits.** Twitter/X: 280 chars, TikTok: 2200 chars, Instagram: 2200 chars. The API validates these but it's better to respect them upfront.
- **Social accounts are connected via the web UI only.** You cannot connect a new social account through the API. If the user needs to connect one, direct them to https://clipit.dev/settings/social.

## Verification

- **Post succeeded:** `status === "posted"` and `perPlatformResults` shows success for each platform
- **Post URL available:** Each platform's result includes a `postUrl` linking to the published content
- **Schedule created:** Response has `status === "scheduled"` and `scheduledFor` matches the requested time
- **Cancel succeeded:** Post status changes to `cancelled`
- **Failed post:** Check `perPlatformResults` for per-platform error messages — some platforms may succeed while others fail
