#!/usr/bin/env python3
"""Upload an image, video, or audio file to the ClipIt asset library.

Usage:
  python upload_asset.py --file <path> [--content-type image/png]
"""

import argparse
import mimetypes
import os
import requests
from clipper_client import ClipperClient, print_json, main_wrapper


@main_wrapper
def main():
    parser = argparse.ArgumentParser(description="Upload a library asset")
    parser.add_argument("--file", required=True, help="Path to the asset file")
    parser.add_argument("--content-type", help="MIME type, guessed from file when omitted")
    parser.add_argument("--duration", type=float, help="Duration in seconds for audio/video assets")
    args = parser.parse_args()

    file_path = args.file
    filename = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    content_type = args.content_type or mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    client = ClipperClient()
    signed = client.post(
        "/api/v1/assets/sign-upload",
        {
            "filename": filename,
            "contentType": content_type,
            "size": size,
        },
    )

    with open(file_path, "rb") as file_obj:
        upload_response = requests.put(
            signed["uploadUrl"],
            data=file_obj,
            headers={"Content-Type": content_type},
            timeout=600,
        )
    upload_response.raise_for_status()

    finalize_body = {
        "objectPath": signed["key"],
        "fileSize": size,
    }
    if args.duration is not None:
        finalize_body["duration"] = args.duration

    result = client.post(f"/api/v1/assets/{signed['assetId']}/finalize", finalize_body)
    print_json(result)


if __name__ == "__main__":
    main()
