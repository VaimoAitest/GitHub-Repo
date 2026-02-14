from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI(title="VaimoAI Proxy API", version="1.0.0")


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
    # Demo JSON (damit Actions sicher parsen)
    return JSONResponse(
        content={
            "pageNumber": pagenumber,
            "pageSize": pagesize,
            "numberOfHits": 2,
            "items": [
                {
                    "exposeId": "64752863",
                    "title": "Demo Halle 3'100 m²",
                    "price": 21700.0,
                    "currency": "EUR",
                    "priceInterval": "MONTH",
                    "address": "Berlin 12161",
                    "lat": 52.46688,
                    "lon": 13.33361,
                    "url": "https://www.immobilienscout24.de/expose/64752863",
                    "source": "sandbox"
                },
                {
                    "exposeId": "62234938",
                    "title": "Demo Halle 2'800 m²",
                    "price": 18200.0,
                    "currency": "EUR",
                    "priceInterval": "MONTH",
                    "address": "Berlin 12159",
                    "lat": 52.47656,
                    "lon": 13.33822,
                    "url": "https://www.immobilienscout24.de/expose/62234938",
                    "source": "sandbox"
                }
            ],
        }
    )


@app.get("/is24/expose/{exposeId}")
def is24_expose(exposeId: str):
    return JSONResponse(
        content={
            "exposeId": exposeId,
            "title": "Demo Expose",
            "description": "Demo description (replace with IS24 Expose API later).",
            "propertyType": "Industry",
            "marketingType": "RENT",
            "price": 21700.0,
            "currency": "EUR",
            "priceInterval": "MONTH",
            "size_m2": 3100,
            "address": "Berlin",
            "features": ["Rampe", "Deckenhöhe 8m"],
            "images": [],
            "url": f"https://www.immobilienscout24.de/expose/{exposeId}"
        }
    )
