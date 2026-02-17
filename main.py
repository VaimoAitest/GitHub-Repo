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

    # ✅ RICHTIG: radius/region im Pfad
    url = f"{IS24_BASE_URL}/search/v1.0/search/{mode}"

    params = {
        "realestatetype": realestatetype,  # Tipp: "apartmentrent" testen!
        "pagesize": pagesize,
        "pagenumber": pagenumber,
    }

    if mode == "radius":
        params["geocoordinates"] = geocoordinates

    if mode == "region":
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
                "body": (response.text or "")[:1500],
                "called_url": response.url,   # 🔥 hilft beim Debug
            },
        )

    return JSONResponse(content={"raw": xmltodict.parse(response.text)})
