#!/usr/bin/env python3
"""Generate an AI thumbnail using Nano Banana Pro.

Usage:
  python generate_thumbnail.py --prompt <prompt> [--clip-id <id>]
  [--aspect-ratio 16:9] [--resolution 2K] [--wait]

With --clip-id: enhances a frame from the clip (image-to-image).
Without --clip-id: generates from scratch (text-to-image).
"""

import argparse
from clipper_client import ClipperClient, print_json, main_wrapper


@main_wrapper
def main():
    parser = argparse.ArgumentParser(description="Generate thumbnail")
    parser.add_argument("--prompt", required=True, help="Description of the thumbnail")
    parser.add_argument("--clip-id", help="Clip to base the thumbnail on (image-to-image)")
    parser.add_argument("--aspect-ratio", default="16:9", choices=["16:9", "9:16", "1:1", "4:5", "3:4"])
    parser.add_argument("--resolution", default="2K", choices=["2K", "4K"])
    parser.add_argument("--wait", action="store_true", help="Wait for generation to complete")
    args = parser.parse_args()

    body = {
        "prompt": args.prompt,
        "aspectRatio": args.aspect_ratio,
        "resolution": args.resolution,
    }
    if args.clip_id:
        body["clipId"] = args.clip_id

    client = ClipperClient()
    response = client.post("/api/v1/thumbnails", body)

    if args.wait and response.get("jobId"):
        job = client.wait_for_job(response["jobId"], timeout=120)
        print_json(job)
    else:
        print_json(response)


if __name__ == "__main__":
    main()
