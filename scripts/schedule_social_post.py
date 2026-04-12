#!/usr/bin/env python3
"""Schedule a rendered clip for future social media posting.

Usage:
  python schedule_social_post.py --clip-id <id> --platforms tiktok
  --caption "My caption" --scheduled-for "2026-04-15T09:00:00Z"
  [--title "YouTube title"]
"""

import argparse
from clipper_client import ClipperClient, print_json, main_wrapper


@main_wrapper
def main():
    parser = argparse.ArgumentParser(description="Schedule a social post")
    parser.add_argument("--clip-id", required=True, help="Rendered clip ID")
    parser.add_argument("--platforms", required=True, help="Comma-separated platforms")
    parser.add_argument("--caption", required=True, help="Post caption")
    parser.add_argument("--scheduled-for", required=True, help="ISO 8601 datetime (must be in the future)")
    parser.add_argument("--title", help="Title (required for YouTube)")
    parser.add_argument("--hashtags", help="Comma-separated hashtags")
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(",")]

    body = {
        "clipId": args.clip_id,
        "platforms": platforms,
        "caption": args.caption,
        "scheduledFor": args.scheduled_for,
    }
    if args.title:
        body["title"] = args.title
    if args.hashtags:
        body["hashtags"] = [h.strip().lstrip("#") for h in args.hashtags.split(",")]

    client = ClipperClient()
    response = client.post("/api/v1/social/schedule", body)
    print_json(response)


if __name__ == "__main__":
    main()
