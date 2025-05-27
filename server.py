import os
import django

# server.py
from socketio import AsyncServer
from socketio.asgi import ASGIApp
from fastapi import FastAPI

sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
app.mount("/", ASGIApp(sio))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
fastapi_app = FastAPI()

# 👉 Добавим отдачу HTML-файла с кнопкой запуска
@fastapi_app.get("/", response_class=HTMLResponse)
async def root():
    with open("Webcraft.html", "r", encoding="utf-8") as f:
        return f.read()

app = ASGIApp(sio, other_asgi_app=fastapi_app)

# 👇 Всё остальное — как раньше
players = {}

@sio.event
async def connect(sid, environ):
    print(f"[+] {sid} connected")
    players[sid] = {'x': 0, 'y': 0, 'z': 0, 'color': (255, 255, 255), 'nickname': 'Player'}
    await sio.emit('player_update', players)

@sio.event
async def disconnect(sid):
    print(f"[-] {sid} disconnected")
    players.pop(sid, None)
    await sio.emit('player_update', players)

@sio.event
async def player_position(sid, data):
    players[sid] = {
        'x': data['x'],
        'y': data['y'],
        'z': data['z'],
        'color': data['color'],
        'nickname': data.get('nickname', 'Player')
    }
    await sio.emit('player_update', players)

@sio.event
async def block_update(sid, data):
    await sio.emit('block_update', data, skip_sid=sid)

@sio.event
async def block_remove(sid, data):
    await sio.emit('block_remove', data, skip_sid=sid)
