from fastapi import FastAPI
import logging
from app.models.request_models import RecommendationRequestBody
from app.services.gemini_service import get_recommendation_response

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@app.get("/recommendation")
async def test_route(request_body: RecommendationRequestBody):
    try:
        liked_animes = request_body.likes
        response = get_recommendation_response(liked_animes)
        return response
    except Exception as error:
        print(f'exception in test_route {error}')
    return {"message": "Hello World!"}
