import os
from urllib import response

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class LLMClient:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured. "
                "Please add it to your .env file."
            )

        # creates a client to interact with the Groq API using the provided API key.
        self.client = Groq(api_key=api_key)

        # Keep the model configurable.
        self.model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        )

    def invoke(self, prompt: str) -> str:

        # Send the prompt to the Groq API and get a response.
        response = self.client.chat.completions.create(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Oracle PL/SQL code reviewer. "
                        "Review code strictly against the supplied "
                        "coding standards."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "plsql_code_review",
                    "strict": True,

                    "schema": {
                        "type": "object",

                        "properties": {

                            "summary": {
                                "type": "object",
                                "properties": {

                                    "total_findings": {
                                        "type": "integer"
                                    },

                                    "high": {
                                        "type": "integer"
                                    },

                                    "medium": {
                                        "type": "integer"
                                    },

                                    "low": {
                                        "type": "integer"
                                    }
                                },

                                "required": [
                                    "total_findings",
                                    "high",
                                    "medium",
                                    "low"
                                ],

                                "additionalProperties": False
                            },

                            "findings": {
                                "type": "array",

                                "items": {
                                    "type": "object",

                                    "properties": {

                                        "rule_id": {
                                            "type": "string"
                                        },

                                        "category": {
                                            "type": "string"
                                        },

                                        "severity": {
                                            "type": "string"
                                        },

                                        "title": {
                                            "type": "string"
                                        },

                                        "line": {
                                            "type": "integer"
                                        },

                                        "code": {
                                            "type": "string"
                                        },

                                        "message": {
                                            "type": "string"
                                        },

                                        "standard": {
                                            "type": "string"
                                        },

                                        "recommendation": {
                                            "type": "string"
                                        }
                                    },

                                    "required": [
                                        "rule_id",
                                        "category",
                                        "severity",
                                        "title",
                                        "line",
                                        "code",
                                        "message",
                                        "standard",
                                        "recommendation"
                                    ],

                                    "additionalProperties": False
                                }
                            }
                        },

                        "required": [
                            "summary",
                            "findings"
                        ],

                        "additionalProperties": False
                    }
                }
            }
    )

        return response.choices[0].message.content