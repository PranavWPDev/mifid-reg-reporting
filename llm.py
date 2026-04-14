from functools import lru_cache
import logging

import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv

from config import get_settings

load_dotenv()
logger = logging.getLogger(__name__)


@lru_cache
def _get_model():
    settings = get_settings()
    vertexai.init(
        project=settings.gemini_project_id,
        location=settings.gemini_location,
    )
    return GenerativeModel(settings.gemini_model_name)


def call_llm(prompt: str, json_mode: bool = False) -> str:
    model = _get_model()

    generation_config = {
        "temperature": 0.0,
        "max_output_tokens": 4096,
        "top_p": 0.1,
    }

    if json_mode:
        generation_config["response_mime_type"] = "application/json"

    response = model.generate_content(
        prompt,
        generation_config=generation_config,
    )

    text = (response.text or "").strip()

    # Keep only the JSON body if the model adds extra text
    if "{" in text:
        text = text[text.find("{"):]
    if "}" in text:
        text = text[: text.rfind("}") + 1]

    print("\n🧠 RAW LLM OUTPUT:\n", text, "\n")
    return text

# from functools import lru_cache
# import logging

# import vertexai
# from vertexai.generative_models import GenerativeModel

# from config import get_settings


# logger = logging.getLogger(__name__)


# @lru_cache(maxsize=8)
# def _get_model(model_name: str | None = None):
#     settings = get_settings()

#     project_id = settings.gcp_project_id or settings.gemini_project_id
#     location = settings.gcp_region or settings.gemini_location
#     model_to_use = model_name or settings.llm_model or settings.gemini_model_name

#     if not project_id:
#         raise RuntimeError("GCP_PROJECT_ID is not configured.")
#     print("🔥 PROJECT:", settings.gemini_project_id)
#     print("🔥 LOCATION:", settings.gemini_location)
#     print("🔥 MODEL:", settings.gemini_model_name)
#     vertexai.init(
#         project=project_id,
#         location=location,
#     )
#     return GenerativeModel(model_to_use)


# def call_llm(prompt: str, json_mode: bool = False, model_name: str | None = None) -> str:
#     model = _get_model(model_name)

#     generation_config = {
#         "temperature": 0.0,
#         "max_output_tokens": 4096,
#         "top_p": 0.1,
#     }

#     if json_mode:
#         generation_config["response_mime_type"] = "application/json"

#     response = model.generate_content(
#         prompt,
#         generation_config=generation_config,
#     )

#     text = (response.text or "").strip()

#     if "{" in text:
#         text = text[text.find("{"):]
#     if "}" in text:
#         text = text[: text.rfind("}") + 1]

#     print("\n🧠 RAW LLM OUTPUT:\n", text, "\n")
#     return text