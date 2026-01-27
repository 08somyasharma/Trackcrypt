import os
import time
from datetime import datetime
import asyncio

from app.services.coingecko import fetch_prices
from app.services.market_store import save_market_price

from app.main import active_connections

from app.services.publisher import (
    publish_price_event,
    publish_user_alert_event
)

from app.db.dynamo import get_dynamodb

dynamodb = get_dynamodb()


WATCHLIST_TABLE = "Watchlist"

print({
    "region": os.getenv("AWS_REGION")
})


def poll():
    prices = fetch_prices()
    print("polled !", prices)

    timestamp = int(datetime.utcnow().timestamp() * 1000)

    for symbol, price in prices.items():

        # 1️⃣ Save historical price (AWS optional)
        try:
            save_market_price(symbol, price)
        except Exception:
            print("⚠️ DynamoDB save skipped (no credentials)")

        # 2️⃣ Publish real-time price (local WebSocket)
        for ws in list(active_connections):
            try:
                asyncio.run(
                    ws.send_json({
                        "symbol": symbol,
                        "price": price,
                        "timestamp": timestamp
                    })
                )
            except Exception:
                pass

        # 3️⃣ Optional: external publish (safe)
        try:
            publish_price_event({
                "symbol": symbol,
                "price": price,
                "timestamp": timestamp
            })
        except Exception:
            pass

        # 4️⃣ Evaluate alerts (AWS optional)
        try:
            alerts = dynamodb.query(
                TableName=WATCHLIST_TABLE,
                IndexName="cryptoSymbol-index",
                KeyConditionExpression="cryptoSymbol = :s",
                ExpressionAttributeValues={
                    ":s": {"S": symbol}
                }
            )

            for alert in alerts.get("Items", []):
                alert_price = float(alert["alertPrice"]["N"])

                if price >= alert_price:
                    publish_user_alert_event(
                        alert["userId"]["S"],
                        {
                            "symbol": symbol,
                            "threshold": alert_price,
                            "price": price,
                            "timestamp": timestamp
                        }
                    )

        except Exception:
            print("⚠️ Watchlist check skipped (no AWS credentials)")


def start_price_worker():
    poll()
    while True:
        time.sleep(30)
        poll()
