import logging
from google import genai
from google.genai import types
from app.services import GEMINI_API_KEY
import json

logger = logging.getLogger()


def get_recommendation_response(likes: list[str]):

    RECOMMENDATION_SYSTEM_PROMPT = """
    You are a Anime Recommendation Engine,
    Given the input of Anime / List of Animes which user likes Suggest 5 Animes which the user
    might like apart from the ones provided.
    Respond strictly in a JSON Array format
    [
        {"anime": // This should be an object with name of anime,
        "reasoning": // This should be the reasoning behing the suggestions
        }
    ]
    """

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        input = 'User Likes the following Animes : '+','.join(likes)
        response = client.models.generate_content(model="gemini-2.0-flash", config=types.GenerateContentConfig(
            system_instruction=RECOMMENDATION_SYSTEM_PROMPT,
            response_mime_type="application/json",
            max_output_tokens=8192,
            top_p=0.95,
            top_k=40,
            temperature=1,
            tools=[types.Tool(
                google_search=types.GoogleSearchRetrieval()
            )]
        ), contents=types.Part.from_text(text=input))
        return json.loads(response.candidates[0].content.parts[0].text)
    except Exception as e:
        logger.exception("Exception occurred in get_model",
                         e, stack_info=True)
