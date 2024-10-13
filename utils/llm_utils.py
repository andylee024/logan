import json
import logging
import os

import anthropic
import openai
from dotenv import load_dotenv
from jsonschema import SchemaError, ValidationError, validate

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
anthropic_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)


def run_llm(prompt, provider, json_format=True):

    response = None

    if provider not in ["open_ai", "claude", "gpt-4o", "gpt-o1"]:
        raise ValueError(f"Invalid LLM client: {provider}")
    
    if not json_format:
        openai_completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
        )
        response = openai_completion.choices[0].message.content
        return response

    if provider in ["open_ai", "gpt-4o"]:
        openai_completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            response_format={"type": "json_object"},
        )
        response = openai_completion.choices[0].message.content

    elif provider == "claude":
        claude_completion = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.0,
            messages=prompt,
        )
        response = claude_completion.content[0].text

    elif provider == "gpt-o1":
        openai_completion = openai_client.chat.completions.create(
            model="o1-preview", 
            messages=prompt)
        response = openai_completion.choices[0].message.content

    return response


def run_robust_llm(prompt, provider, schema):

    response = run_llm(prompt=prompt, provider=provider)

    if is_valid_json_schema(response, schema):
        return response
    else:
        return fix_bad_json_with_llm(response, schema)
    

def is_valid_json_schema(response, schema):

    try:
        json_data = extract_json_from_response(response)
        validate(instance=json_data, schema=schema)
        return True

    except (
        ValidationError,
        AttributeError,
        SchemaError,
        json.JSONDecodeError,
    ) as e:
        print(f"Invalid JSON data: {e}")
        return False


def extract_json_from_response(response):
    """Return JSON dict object from response regardless of input type"""

    if isinstance(response, dict):
        return response

    if isinstance(response, str):
        try:
            return json.loads(response)

        except Exception:
            # extract only text after first '{' and before last '}'
            start = response.find("{")
            end = response.rfind("}")
            if start == -1 or end == -1:
                return None

            text = response[start : end + 1]
            return json.loads(text)

    else:
        raise ValueError(f"Unrecognized json type: {type(response)}")


def fix_bad_json_with_llm(response, schema):
    """Given a faulty response and schema, run an LLM to fix the faulty response."""

    def _build_json_fix_prompt():
        base_prompt = "Your job is to fix a bad JSON and by converting it to the correct JSON format. Change FAULTY_JSON to match the SCHEMA"
        faulty_json = f"FAULTY_JSON : {response}"
        correct_schema = f"SCHEMA : {schema}"
        prompt = "\n".join([base_prompt, faulty_json, correct_schema])
        return [{"role": "user", "content": prompt}]

    print("prompt: ", _build_json_fix_prompt())
    new_response = run_llm(_build_json_fix_prompt(), "gpt-4o")
    print("new_response: ", new_response)

    logging.info(
        {"msg": "Function: fix_bad_json_with_llm", "faulty response": response, "fixed Response": new_response}
    )

    if is_valid_json_schema(new_response, schema):
        return new_response

    else:
        raise ValueError("JSON retry failed. Review the JSON schema and response.")


