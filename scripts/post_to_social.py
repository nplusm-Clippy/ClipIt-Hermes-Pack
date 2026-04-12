#!/usr/bin/env python3
"""Post a rendered clip to social media platforms immediately.

Usage:
  python post_to_social.py --clip-id <id> --platforms tiktok,instagram
  --caption "My caption" [--title "YouTube title"] [--wait]

The clip MUST be rendered first (use render_clip.py --wait).
YouTube requires --title.
"""

import argparse
from clipper_client import ClipperClient, print_json, main_wrapper


@main_wrapper
def main():
    parser = argparse.ArgumentParser(description="Post clip to social media")
    parser.add_argument("--clip-id", required=True, help="Rendered clip ID")
    parser.add_argument("--platforms", required=True, help="Comma-separated platforms (tiktok,instagram,youtube,...)")
    parser.add_argument("--caption", required=True, help="Post caption")
    parser.add_argument("--title", help="Title (required for YouTube)")
    parser.add_argument("--hashtags", help="Comma-separated hashtags")
    parser.add_argument("--wait", action="store_true", help="Wait for posting to complete")
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(",")]

    if "youtube" in platforms and not args.title:
        print("ERROR: --title is required when posting to YouTube.", file=__import__("sys").stderr)
        __import__("sys").exit(1)

    body = {
        "clipId": args.clip_id,
        "platforms": platforms,
        "caption": args.caption,
    }
    if args.title:
        body["title"] = args.title
    if args.hashtags:
        body["hashtags"] = [h.strip().lstrip("#") for h in args.hashtags.split(",")]

    client = ClipperClient()
    response = client.post("/api/v1/social/post", body)

    if args.wait and response.get("jobId"):
        job = client.wait_for_job(response["jobId"], timeout=120)
        print_json(job)
    else:
        print_json(response)


if __name__ == "__main__":
    main()
