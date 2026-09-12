import json

from llm_reviewer import build_review_prompt


def review_code(code, standards, llm_client):

    prompt = build_review_prompt(
        code,
        standards
    )

    response = llm_client.invoke(prompt)

    return json.loads(response)