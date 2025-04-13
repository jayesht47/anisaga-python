from fastapi import FastAPI
import logging
from app.models.request_models import RecommendationRequestBody
from app.services.gemini_service import get_recommendation_response
import time
from fastapi import FastAPI, Request

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    body = await request.body()
    headers = request.headers
    logger.debug("received request with headers %s request body %s",headers,body)
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.post("/recommendation")
async def test_route(request_body: RecommendationRequestBody):
    try:
        liked_animes = request_body.likes
        response = get_recommendation_response(liked_animes)
        return response
    except Exception as error:
        print(f'exception in test_route {error}')
    return {"message": "Hello World!"}
