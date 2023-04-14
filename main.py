# curl -d '{"text":"<g>Segment</g> to translate."}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/translate

import json
import requests

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

SOURCE = "est"
TARGET = "fin"
DOMAIN = "general"
APPLICATION = "NLTP"


class TranslationRequest(BaseModel):
    text: str


@app.post("/translate")
async def translate(tr_rq: TranslationRequest):
    print(tr_rq.text)
    r = requests.post("https://api.tartunlp.ai/translation/v2", json={"text": tr_rq.text,
                                                                      "src": SOURCE,
                                                                      "tgt": TARGET,
                                                                      "domain": DOMAIN,
                                                                      "application": APPLICATION})
    print(r.text)
    return {"translation": json.loads(r.text)['result']}


@app.get("/health/ready")
async def ready(response: Response):
    status_code = 200
    title = "OK"
    try:
        r = requests.get("https://api.tartunlp.ai/translation/v2")
        if f'{SOURCE}-{TARGET}' not in list(filter(lambda x: x['name'] == 'General', r.json()['domains']))[0]['languages']:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            status_code = "503"
            title = "Service unavailable!"
    except requests.exceptions.ConnectionError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        status_code = "503"
        title = "Connection error!"
    return {"status": status_code, "title": title}


@app.get("/health/live")
async def live():
    return {"status": 200, "title": "OK"}
