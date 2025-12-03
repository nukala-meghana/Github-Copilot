from fastapi.testclient import TestClient
import hashlib

from main import app, generate, checksum_of

client = TestClient(app)
