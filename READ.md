```markdown
# Token Generator API

A small FastAPI application that accepts text and returns a list of deterministic pseudorandom tokens
and a SHA-256 checksum of the provided text.

Features
- POST /tokens: Accepts JSON body {"text": "..."}, returns {"tokens": [...], "checksum": "...", "message": "..."}
- GET /: Welcome message

Requirements
- Python 3.8+
- See `requirements.txt`

Install
1. Create a virtual environment (recommended)
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows

2. Install dependencies
   pip install -r requirements.txt

Run locally
1. Start the server with uvicorn:
   uvicorn main:app --reload --port 8000

2. Example using curl:
   curl -X POST "http://127.0.0.1:8000/tokens" -H "Content-Type: application/json" -d '{"text":"hello world"}'

Testing
- Run tests with pytest:
  pytest -q

Notes
- The token generation is deterministic (same input -> same tokens) because it uses a fixed salt.
- Adjust the salt or the generation method if you prefer non-deterministic tokens.
```
