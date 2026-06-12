#!/usr/bin/env python3
"""Estimate $CLIP cost for an operation without charging credits.

Usage:
  python estimate_cost.py --operation-type transcription --provider deepgram \
    --model-id nova-3 videoSeconds=120
"""

import argparse
from clipper_client import ClipperClient, print_json, main_wrapper


def parse_metric(value):
    if "=" not in value:
        raise argparse.ArgumentTypeError("metrics must be key=value pairs")

    key, raw = value.split("=", 1)
    key = key.strip()
    if not key:
        raise argparse.ArgumentTypeError("metric key cannot be empty")

    try:
        number = float(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"metric {key} must be numeric") from exc

    return key, number


@main_wrapper
def main():
    parser = argparse.ArgumentParser(description="Estimate a $CLIP credit cost")
    parser.add_argument("--operation-type", required=True, help="Operation type, e.g. transcription")
    parser.add_argument("--provider", required=True, help="Provider name, e.g. deepgram")
    parser.add_argument("--model-id", help="Optional provider model ID")
    parser.add_argument("metrics", nargs="*", type=parse_metric, help="Metric key=value pairs")
    args = parser.parse_args()

    body = {
        "operationType": args.operation_type,
        "provider": args.provider,
        "metrics": dict(args.metrics),
    }
    if args.model_id:
        body["modelId"] = args.model_id

    client = ClipperClient()
    response = client.post("/api/v1/credits/estimate", body)
    print_json(
        {
            "estimatedCostClip": response.get("estimatedCostClip"),
            "affordable": response.get("affordable"),
            "balanceClip": response.get("balanceClip"),
            "spendLimitViolation": response.get("spendLimitViolation"),
            "units": response.get("units", "clip"),
        }
    )


if __name__ == "__main__":
    main()
