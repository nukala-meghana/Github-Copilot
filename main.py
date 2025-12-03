from typing import List
import hashlib

from fastapi import FastAPI
from pydantic import BaseModel

# Simple FastAPI app to demonstrate:
# - a Pydantic model that accepts JSON with a single "text" field
# - a POST endpoint that returns a list of tokens and a checksum for the provided text
#
# The generate() function produces deterministic pseudorandom tokens per word by hashing
# word + position + a fixed salt. The checksum is a SHA-256 hex digest of the raw text.
#
# Welcome message is customized with the participant name (GitHub login).
#
# API endpoints:
# GET  /           -> welcome message
# POST /tokens     -> accepts {"text": "..."} and returns {"tokens": [...], "checksum": "...", "message": "..."}
#
# Tests are provided in tests/test_main.py.

app = FastAPI(
    title="Token Generator API",
    description="Generates pseudorandom tokens from input text and returns a checksum.",
    version="1.0.0",
)


class TextRequest(BaseModel):
    """
    Pydantic model for the POST /tokens endpoint.

    Expected JSON body example:
    {
      "text": "some text to tokenize"
    }
    """
    text: str


def generate(text: str) -> List[str]:
    """
    Generate a list of deterministic pseudorandom tokens from the provided text.
    - Splits the text into words (on whitespace).
    - For each non-empty word, produce a short token derived from SHA-256(word + index + salt).
    - If the text contains no words, produce a single token derived from the whole text.

    This function is deterministic (same input -> same tokens).
    """
    salt = "fixed_salt_for_demo"  # fixed salt ensures tokens are repeatable for the same input
    words = [w for w in text.split() if w]
    tokens: List[str] = []

    if not words:
        # fallback: produce a single token from the whole text (may be empty string)
        digest = hashlib.sha256((text + salt).encode("utf-8")).hexdigest()
        tokens = [digest[:16]]
        return tokens

    for i, w in enumerate(words):
        # Create a short token: first 16 hex characters of sha256(word + index + salt)
        raw = f"{w}:{i}:{salt}"
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        token = digest[:16]
        tokens.append(token)

    return tokens


def checksum_of(text: str) -> str:
    """Return the SHA-256 checksum (hex digest) of the provided text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@app.get("/")
def root():
    """
    Welcome endpoint.
    Returns a short customized welcome message for the participant.
    """
    participant = "nukala-meghana"  # customize this as required
    return {
        "message": f"Welcome {participant}! Use POST /tokens with JSON {'{\"text\": \"...\"}'} to get tokens and a checksum."
    }


@app.post("/tokens")
def tokens_endpoint(payload: TextRequest):
    """
    POST endpoint that accepts a JSON body with a single field "text" (see TextRequest).
    Uses generate() to create token list, and returns the tokens plus the checksum of the text.

    Response example:
    {
      "tokens": ["...","..."],
      "checksum": "sha256hex...",
      "message": "Welcome nukala-meghana!"
    }
    """
    text = payload.text
    tokens = generate(text)
    cs = checksum_of(text)
    participant = "nukala-meghana"

    return {
        "tokens": tokens,
        "checksum": cs,
        "message": f"Welcome {participant}! Token generation successful."
    }
