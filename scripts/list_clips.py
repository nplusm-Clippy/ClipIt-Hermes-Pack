#!/usr/bin/env python3
"""List clips, optionally filtered by video ID.

Usage:
  python list_clips.py [--video-id <id>] [--limit N] [--offset N]
"""

import argparse
from clipper_client import ClipperClient, print_json, main_wrapper


@main_wrapper
def main():
    parser = argparse.ArgumentParser(description="List clips")
    parser.add_argument("--video-id", help="Filter by video ID")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()

    params = {"limit": args.limit, "offset": args.offset}
    if args.video_id:
        params["videoId"] = args.video_id

    client = ClipperClient()
    response = client.get("/api/v1/clips", params)
    print_json(response)


if __name__ == "__main__":
    main()
