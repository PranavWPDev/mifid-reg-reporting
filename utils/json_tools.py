import json
import re

def extract_json_object(text: str, fallback: dict):
    try:
        # direct parse
        return json.loads(text)
    except:
        pass

    try:
        # extract JSON block
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except:
        pass

    return fallback