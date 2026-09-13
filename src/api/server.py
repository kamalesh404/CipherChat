"""FastAPI + WebSocket server for CipherChat."""

from __future__ import annotations

import json
from typing import Dict, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

from src.core.config import Config
from src.core.models import RegisterRequest, RegisterResponse, UserRecord, MessageEnvelope
from src.core.store import Store


def build_app(config: Config | None = None) -> FastAPI:
    config = config or Config.from_env()
    app = FastAPI(title="CipherChat", version="0.1.0")
    store = Store(config.db_path)
    # username -> set of websockets
    connections: Dict[str, Set[WebSocket]] = {}

    @app.get("/health")
    def health():
        return {"status": "healthy", "version": "0.1.0"}

    @app.post("/v1/register", response_model=RegisterResponse)
    def register(req: RegisterRequest):
        if store.get_user(req.username):
            return JSONResponse({"error": "username taken"}, status_code=400)
        rec = UserRecord(username=req.username, public_key=req.public_key)
        store.add_user(rec)
        return rec

    @app.get("/v1/users")
    def list_users():
        return {"users": [u.model_dump() for u in store.list_users()]}

    @app.get("/v1/users/{username}")
    def get_user(username: str):
        rec = store.get_user(username)
        if not rec:
            return JSONResponse({"error": "not found"}, status_code=404)
        return rec

    @app.post("/v1/messages")
    def send_message(env: MessageEnvelope):
        # Store and try to deliver live
        store.enqueue(env)
        # If recipient is connected, push immediately is handled via WS poll
        return {"queued": True}

    @app.get("/v1/messages/{username}")
    def poll_messages(username: str):
        msgs = store.dequeue_all(username)
        return {"messages": [m.model_dump() for m in msgs]}

    @app.websocket("/v1/ws/{username}")
    async def ws_endpoint(ws: WebSocket, username: str):
        await ws.accept()
        connections.setdefault(username, set()).add(ws)
        # Deliver any queued messages on connect
        for env in store.dequeue_all(username):
            await ws.send_text(json.dumps({"type": "message", "payload": env.model_dump()}))
        try:
            while True:
                raw = await ws.receive_text()
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    await ws.send_text(json.dumps({"type": "error", "payload": {"msg": "bad json"}}))
                    continue
                mtype = data.get("type")
                payload = data.get("payload", {})
                if mtype == "message":
                    try:
                        env = MessageEnvelope(**payload)
                    except Exception as e:
                        await ws.send_text(json.dumps({"type": "error", "payload": {"msg": str(e)}}))
                        continue
                    store.enqueue(env)
                    # Deliver if recipient online
                    for conn in list(connections.get(env.recipient, [])):
                        try:
                            await conn.send_text(json.dumps({"type": "message", "payload": env.model_dump()}))
                        except Exception:
                            pass
                    await ws.send_text(json.dumps({"type": "ack", "payload": {"msg_no": env.msg_no}}))
                else:
                    await ws.send_text(json.dumps({"type": "error", "payload": {"msg": "unknown type"}}))
        except WebSocketDisconnect:
            pass
        finally:
            connections.get(username, set()).discard(ws)

    # Static frontend if present
    static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
    if os.path.isdir(static_dir):
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")

    return app


def main():
    import uvicorn
    config = Config.from_env()
    uvicorn.run(build_app(config), host=config.host, port=config.port)


if __name__ == "__main__":
    main()
