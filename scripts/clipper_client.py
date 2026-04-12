"""
Clipper REST client shared by all skill scripts.

Reads CLIPPER_API_KEY and CLIPPER_BASE_URL from environment variables.
Never logs the API key.
"""

import os
import sys
import json
import time
import requests
from typing import Any, Dict, List, Optional

DEFAULT_BASE_URL = "https://clipit.dev"


class ClipperError(Exception):
    """Raised for API errors. Contains status code and parsed error response."""

    def __init__(self, status_code: int, code: str, message: str, details: Any = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(f"[{code}] {message}")


class ClipperClient:
    """
    Thin REST client for the Clipper API v1.

    Handles authentication, error parsing, and file uploads.
    Does NOT handle retries — long operations should be polled via wait_for_job.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.environ.get("CLIPPER_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "CLIPPER_API_KEY not set. Add it to your Hermes environment "
                "or pass it explicitly to ClipperClient()."
            )
        self.base_url = (
            base_url or os.environ.get("CLIPPER_BASE_URL") or DEFAULT_BASE_URL
        ).rstrip("/")

    def _headers(self) -> Dict[str, str]:
        return {
            "X-API-Key": self.api_key,
            "Accept": "application/json",
            "User-Agent": "ClipperHermesSkills/1.0",
        }

    def _handle_response(self, response: requests.Response) -> Any:
        if response.status_code in (200, 201, 202, 204):
            if response.status_code == 204:
                return None
            return response.json()

        try:
            body = response.json()
            raise ClipperError(
                status_code=response.status_code,
                code=body.get("code", "UNKNOWN"),
                message=body.get("error", "Unknown error"),
                details=body.get("details"),
            )
        except (ValueError, KeyError):
            raise ClipperError(
                status_code=response.status_code,
                code="INVALID_RESPONSE",
                message=f"HTTP {response.status_code}: {response.text[:200]}",
            )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        response = requests.get(
            f"{self.base_url}{path}",
            headers=self._headers(),
            params=params,
            timeout=30,
        )
        return self._handle_response(response)

    def post(self, path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
        response = requests.post(
            f"{self.base_url}{path}",
            headers={**self._headers(), "Content-Type": "application/json"},
            json=json_body,
            timeout=60,
        )
        return self._handle_response(response)

    def patch(self, path: str, json_body: Dict[str, Any]) -> Any:
        response = requests.patch(
            f"{self.base_url}{path}",
            headers={**self._headers(), "Content-Type": "application/json"},
            json=json_body,
            timeout=30,
        )
        return self._handle_response(response)

    def delete(self, path: str) -> Any:
        response = requests.delete(
            f"{self.base_url}{path}",
            headers=self._headers(),
            timeout=30,
        )
        return self._handle_response(response)

    def upload_file(self, path: str, file_path: str, field_name: str = "file") -> Any:
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{self.base_url}{path}",
                headers={
                    "X-API-Key": self.api_key,
                    "Accept": "application/json",
                    "User-Agent": "ClipperHermesSkills/1.0",
                },
                files={field_name: f},
                timeout=600,
            )
        return self._handle_response(response)

    def wait_for_job(
        self,
        job_id: str,
        poll_interval: float = 3.0,
        timeout: float = 600.0,
        show_progress: bool = True,
    ) -> Dict[str, Any]:
        """Poll GET /api/v1/jobs/:jobId until status is terminal."""
        deadline = time.time() + timeout
        last_progress = -1
        while time.time() < deadline:
            job = self.get(f"/api/v1/jobs/{job_id}")
            status = job.get("status")
            progress = job.get("progress", 0)

            if show_progress and progress != last_progress:
                print(f"  [{status}] {progress}%", file=sys.stderr)
                last_progress = progress

            if status == "completed":
                return job
            if status == "failed":
                err = job.get("error") or {}
                raise ClipperError(
                    status_code=500,
                    code=err.get("code", "JOB_FAILED"),
                    message=err.get("message", "Job failed"),
                    details=err,
                )
            if status == "cancelled":
                raise ClipperError(500, "JOB_CANCELLED", "Job was cancelled")

            time.sleep(poll_interval)

        raise ClipperError(
            500, "JOB_TIMEOUT", f"Job {job_id} did not complete within {timeout}s"
        )


def print_json(obj: Any) -> None:
    """Pretty-print JSON to stdout (used by scripts for agent consumption)."""
    print(json.dumps(obj, indent=2, default=str))


def main_wrapper(fn):
    """Decorator for script main functions. Catches ClipperError and prints
    a clean error message to stderr, exits with code 1."""

    def wrapped():
        try:
            fn()
        except ClipperError as e:
            print(
                f"ERROR: {e.message} (code: {e.code}, status: {e.status_code})",
                file=sys.stderr,
            )
            if e.details:
                print(
                    f"Details: {json.dumps(e.details, indent=2, default=str)}",
                    file=sys.stderr,
                )
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nCancelled.", file=sys.stderr)
            sys.exit(130)
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    return wrapped
