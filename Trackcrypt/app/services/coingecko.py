import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def fetch_prices():
    response = requests.get(
        COINGECKO_URL,
        params={
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd"
        },
        timeout=5
    )

    data = response.json()

    return {
        "BTC": data["bitcoin"]["usd"],
        "ETH": data["ethereum"]["usd"]
    }
