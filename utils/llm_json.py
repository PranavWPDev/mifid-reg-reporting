# import json
# from typing import Any, Dict, Tuple

# from llm import call_llm


# def _strip_fences(text: str) -> str:
#     text = (text or "").strip()
#     text = text.replace("```json", "").replace("```", "").strip()
#     return text


# def _extract_balanced_json(text: str) -> Any:
#     """
#     Extract the first balanced JSON object/array from a messy LLM response.
#     Returns parsed Python object or None.
#     """
#     if not text:
#         return None

#     text = _strip_fences(text)

#     # Direct parse first
#     try:
#         return json.loads(text)
#     except Exception:
#         pass

#     # Scan for the first balanced object/array
#     start_positions = [i for i, ch in enumerate(text) if ch in "{["]
#     for start in start_positions:
#         opening = text[start]
#         closing = "}" if opening == "{" else "]"
#         depth = 0
#         in_string = False
#         escape = False

#         for idx in range(start, len(text)):
#             ch = text[idx]

#             if in_string:
#                 if escape:
#                     escape = False
#                 elif ch == "\\":
#                     escape = True
#                 elif ch == '"':
#                     in_string = False
#                 continue

#             if ch == '"':
#                 in_string = True
#                 continue

#             if ch == opening:
#                 depth += 1
#             elif ch == closing:
#                 depth -= 1
#                 if depth == 0:
#                     candidate = text[start : idx + 1]
#                     try:
#                         return json.loads(candidate)
#                     except Exception:
#                         break

#     return None


# def call_llm_json(
#     prompt: str,
#     fallback: Dict[str, Any],
#     retries: int = 2,
#     json_mode: bool = True,
# ) -> Tuple[Dict[str, Any], str]:
#     """
#     Calls the LLM and retries with a repair prompt if JSON is malformed/truncated.
#     Returns: (parsed_result, raw_text)
#     """
#     last_raw = ""

#     current_prompt = prompt
#     for attempt in range(retries + 1):
#         try:
#             raw = call_llm(current_prompt, json_mode=json_mode)
#         except Exception as e:
#             raw = f""
#             last_raw = raw
#             if attempt >= retries:
#                 return fallback, last_raw
#             current_prompt = (
#                 prompt
#                 + "\n\nThe previous call failed with an exception. "
#                   "Return the complete JSON only, with no markdown, no explanation."
#             )
#             continue

#         last_raw = raw or ""
#         parsed = _extract_balanced_json(last_raw)

#         if isinstance(parsed, dict):
#             return parsed, last_raw

#         if attempt < retries:
#             current_prompt = (
#                 prompt
#                 + "\n\nThe previous response was incomplete or invalid JSON.\n"
#                   "Previous response:\n"
#                 + last_raw
#                 + "\n\nReturn ONLY a complete JSON object. No markdown. No explanation."
#             )

#     return fallback, last_raw


import json
from typing import Any, Dict, Tuple

from llm import call_llm


def call_llm_json(prompt: str, fallback: Dict[str, Any], retries: int = 2) -> Tuple[Dict[str, Any], str]:
    last_raw = ""

    for _ in range(retries + 1):
        try:
            raw = call_llm(prompt)
        except Exception:
            continue

        last_raw = raw or ""

        try:
            parsed = json.loads(last_raw)
            if isinstance(parsed, dict):
                return parsed, last_raw
        except Exception:
            pass

        # Try extracting JSON
        start = last_raw.find("{")
        end = last_raw.rfind("}")
        if start != -1 and end != -1:
            try:
                parsed = json.loads(last_raw[start:end + 1])
                return parsed, last_raw
            except Exception:
                continue

    return fallback, last_raw