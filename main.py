import os
import requests
import xmltodict
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from requests_oauthlib import OAuth1

app = FastAPI(title="VaimoAI Proxy API", version="2.0.0")

@app.get("/version")
def version():
    return {"version": "2.0-real-is24", "base_url": IS24_BASE_URL}


# Environment Variables (aus Render)
IS24_BASE_URL = os.getenv("IS24_BASE_URL", "https://rest.sandbox-immobilienscout24.de/restapi/api")
CONSUMER_KEY = os.getenv("IS24_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("IS24_CONSUMER_SECRET")


def oauth1():
    if not CONSUMER_KEY or not CONSUMER_SECRET:
        raise HTTPException(status_code=500, detail="Missing IS24_CONSUMER_KEY / IS24_CONSUMER_SECRET")
    return OAuth1(CONSUMER_KEY, CONSUMER_SECRET)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/is24/search")
def is24_search(
    realestatetype: str,
    mode: str,
    geocoordinates: Optional[str] = None,
    geocodes: Optional[str] = None,
    pagesize: int = 20,
    pagenumber: int = 1,
    features: Optional[str] = None,
):
    if mode not in ("radius", "region"):
        raise HTTPException(status_code=400, detail="mode must be radius or region")

    if mode == "radius" and not geocoordinates:
        raise HTTPException(status_code=400, detail="geocoordinates required for radius mode")

    if mode == "region" and not geocodes:
        raise HTTPException(status_code=400, detail="geocodes required for region mode")

    url = f"{IS24_BASE_URL}/search/v1.0/search/{mode}"

    params = {
        "realestatetype": realestatetype,
        "pagesize": pagesize,
        "pagenumber": pagenumber,
    }

    if geocoordinates:
        params["geocoordinates"] = geocoordinates

    if geocodes:
        params["geocodes"] = geocodes

    if features:
        params["features"] = features

    response = requests.get(
        url,
        params=params,
        auth=oauth1(),
        headers={"Accept": "application/xml"},
        timeout=30,
    )

    if response.status_code >= 400:
        return JSONResponse(
            status_code=response.status_code,
            content={
                "error": "IS24 Error",
                "status": response.status_code,
                "body": response.text[:1500],
            },
        )

    data = xmltodict.parse(response.text)

    return JSONResponse(content={"raw": data})


@app.get("/is24/expose/{exposeId}")
def is24_expose(exposeId: str):
    url = f"{IS24_BASE_URL}/search/v1.0/expose/{exposeId}"

    response = requests.get(
        url,
        auth=oauth1(),
        headers={"Accept": "application/xml"},
        timeout=30,
    )

    if response.status_code >= 400:
        return JSONResponse(
            status_code=response.status_code,
            content={
                "error": "IS24 Error",
                "status": response.status_code,
                "body": response.text[:1500],
            },
        )

    data = xmltodict.parse(response.text)

    return JSONResponse(content={"raw": data})
