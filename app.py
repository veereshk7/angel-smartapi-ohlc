from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
from angel_api import exchange_token, get_ohlc

load_dotenv()

app = FastAPI()

ACCESS_TOKEN = None

ANGEL_API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_ID = os.getenv("ANGEL_CLIENT_ID")
REDIRECT_URI = os.getenv("ANGEL_REDIRECT_URI")


@app.get("/")
def home():
    return {"status": "Angel SmartAPI OAuth Server Running"}


@app.get("/login")
def login():
    """
    Redirect user to Angel login
    """

    url = f"https://smartapi.angelone.in/publisher-login?api_key={ANGEL_API_KEY}"

    return RedirectResponse(url)


@app.get("/callback")
def callback(authcode: str):
    """
    Angel redirects here with auth code
    """

    global ACCESS_TOKEN

    token_data = exchange_token(authcode)

    ACCESS_TOKEN = token_data.get("data", {}).get("jwtToken")

    return {
        "message": "Login successful",
        "token": ACCESS_TOKEN
    }


@app.get("/ohlc")
def fetch_ohlc(symboltoken: str):

    if not ACCESS_TOKEN:
        return {"error": "Not authenticated"}

    data = get_ohlc(ACCESS_TOKEN, symboltoken)

    return data