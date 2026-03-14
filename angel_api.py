import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_ID = os.getenv("ANGEL_CLIENT_ID")
CLIENT_SECRET = os.getenv("ANGEL_CLIENT_SECRET")

BASE_URL = "https://apiconnect.angelone.in"


def exchange_token(auth_code: str):
    """Exchange authorization code for access token"""

    url = f"{BASE_URL}/rest/auth/angelbroking/user/v1/getAccessToken"

    payload = {
        "clientcode": CLIENT_ID,
        "authcode": auth_code
    }

    headers = {
        "Content-Type": "application/json",
        "X-PrivateKey": API_KEY
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()


def get_ohlc(token: str, symboltoken: str, interval="FIVE_MINUTE"):
    """
    Fetch OHLC data
    """

    url = f"{BASE_URL}/rest/secure/angelbroking/historical/v1/getCandleData"

    now = datetime.utcnow()
    start = now - timedelta(days=1)

    payload = {
        "exchange": "NSE",
        "symboltoken": symboltoken,
        "interval": interval,
        "fromdate": start.strftime("%Y-%m-%d %H:%M"),
        "todate": now.strftime("%Y-%m-%d %H:%M")
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-PrivateKey": API_KEY
    }

    r = requests.post(url, json=payload, headers=headers)

    return r.json()