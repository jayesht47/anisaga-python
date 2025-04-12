from pydantic import BaseModel


class RecommendationRequestBody(BaseModel):

    likes: list[str]
