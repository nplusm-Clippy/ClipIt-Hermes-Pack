#!/usr/bin/env python3
"""Delete a clip.

Usage:
  python delete_clip.py --clip-id <id>
"""

import argparse
from clipper_client import ClipperClient, main_wrapper


@main_wrapper
def main():
    parser = argparse.ArgumentParser(description="Delete a clip")
    parser.add_argument("--clip-id", required=True, help="Clip ID to delete")
    args = parser.parse_args()

    client = ClipperClient()
    client.delete(f"/api/v1/clips/{args.clip_id}")
    print(f"Clip {args.clip_id} deleted.")


if __name__ == "__main__":
    main()
