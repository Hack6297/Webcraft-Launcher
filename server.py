import os, django
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from socketio import AsyncServer
from socketio.asgi import ASGIApp
import uvicorn

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# FastAPI app
sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = ASGIApp(sio)
app = FastAPI()

app.mount("/ws", socket_app)  # for socket.io

@app.get("/", response_class=HTMLResponse)
async def serve_html(request: Request):
    with open("Webcraft.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)
