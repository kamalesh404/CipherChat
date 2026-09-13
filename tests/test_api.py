"""API tests."""

from fastapi.testclient import TestClient

from src.api.server import build_app
from src.core.config import Config

import tempfile, os


def _client():
    tmp = tempfile.mkdtemp()
    config = Config(db_path=os.path.join(tmp, "db.json"))
    return TestClient(build_app(config))


def test_health():
    c = _client()
    assert c.get("/health").json()["status"] == "healthy"


def test_register_and_list():
    c = _client()
    r = c.post("/v1/register", json={"username": "alice", "public_key": "a"*64})
    assert r.status_code == 200
    r2 = c.get("/v1/users")
    assert any(u["username"] == "alice" for u in r2.json()["users"])


def test_duplicate_register():
    c = _client()
    c.post("/v1/register", json={"username": "bob", "public_key": "b"*64})
    r = c.post("/v1/register", json={"username": "bob", "public_key": "b"*64})
    assert r.status_code == 400


def test_poll_empty():
    c = _client()
    r = c.get("/v1/messages/alice")
    assert r.json()["messages"] == []


def test_websocket():
    c = _client()
    with c.websocket_connect("/v1/ws/alice") as ws:
        ws.send_text('{"type": "message", "payload": {"sender": "alice", "recipient": "bob", "nonce_ct": "aa", "msg_no": 1}}')
        data = ws.receive_text()
        assert "ack" in data
