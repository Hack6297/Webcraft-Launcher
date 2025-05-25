import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from socketio import AsyncServer
from socketio.asgi import ASGIApp
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Socket.IO сервер
sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# FastAPI обёртка
fastapi_app = FastAPI()

# Главная страница (для проверки)
@fastapi_app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>🌐 WebCraft Server is Live!</h1>"

# Оборачиваем socket.io в ASGI
app = ASGIApp(sio, other_asgi_app=fastapi_app)

# Игроки
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
