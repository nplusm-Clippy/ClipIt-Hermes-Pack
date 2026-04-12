#!/usr/bin/env python3
"""List connected social media accounts.

Usage:
  python list_social_accounts.py
"""

from clipper_client import ClipperClient, print_json, main_wrapper


@main_wrapper
def main():
    client = ClipperClient()
    response = client.get("/api/v1/social/accounts")
    print_json(response)


if __name__ == "__main__":
    main()
