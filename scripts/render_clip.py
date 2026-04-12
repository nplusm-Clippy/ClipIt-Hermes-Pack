#!/usr/bin/env python3
"""Render a clip via AWS Lambda (Remotion). Returns a downloadable video.

Usage:
  python render_clip.py --clip-id <id> [--aspect-ratio 9:16] [--quality high]
  [--captions] [--no-captions] [--caption-style bold] [--watermark] [--wait]
"""

import argparse
from clipper_client import ClipperClient, print_json, main_wrapper


@main_wrapper
def main():
    parser = argparse.ArgumentParser(description="Render a clip")
    parser.add_argument("--clip-id", required=True, help="Clip ID to render")
    parser.add_argument("--aspect-ratio", default="9:16", choices=["16:9", "9:16", "1:1", "4:5"])
    parser.add_argument("--quality", default="high", choices=["standard", "high", "4k"])
    parser.add_argument("--captions", dest="include_captions", action="store_true", default=True)
    parser.add_argument("--no-captions", dest="include_captions", action="store_false")
    parser.add_argument("--caption-style", choices=["bold", "minimal", "neon", "classic"])
    parser.add_argument("--watermark", action="store_true", default=False)
    parser.add_argument("--wait", action="store_true", help="Wait for render to complete")
    args = parser.parse_args()

    body = {
        "aspectRatio": args.aspect_ratio,
        "quality": args.quality,
        "includeCaptions": args.include_captions,
        "watermark": args.watermark,
    }
    if args.caption_style:
        body["captionStyle"] = args.caption_style

    client = ClipperClient()
    response = client.post(f"/api/v1/clips/{args.clip_id}/render", body)

    if args.wait and response.get("jobId"):
        job = client.wait_for_job(response["jobId"], timeout=600)
        print_json(job)
    else:
        print_json(response)


if __name__ == "__main__":
    main()
