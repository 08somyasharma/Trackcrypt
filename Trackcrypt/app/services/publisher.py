import os
import requests

VELYX_PUBLISH_URL = "https://velyx.me/publish"
API_KEY = os.getenv("VELYX_API_KEY")


def _headers():
    return {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }


def publish_price_event(data: dict):
    requests.post(
        VELYX_PUBLISH_URL,
        json={
            "topic": "crypto:prices",
            "payload": data
        },
        headers=_headers(),
        timeout=5
    )


def publish_user_alert_event(user_id: str, data: dict):
    requests.post(
        VELYX_PUBLISH_URL,
        json={
            "topic": f"user:{user_id}:alerts",
            "payload": data
        },
        headers=_headers(),
        timeout=5
    )
