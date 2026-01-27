import os
from threading import Thread
from dotenv import load_dotenv

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.prices.routes import router as price_routes
from app.watchlist.routes import router as watchlist_routes
from app.auth.routes import router as auth_routes
from app.admin import router as admin_routes
from app.workers.price_worker import start_price_worker

# 🔑 Load env
load_dotenv()

app = FastAPI(title="Crypto Price Tracker")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "views"))

# WebSocket connections
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(ws)

# Routers
app.include_router(auth_routes, prefix="/auth")
app.include_router(watchlist_routes, prefix="/watchlist")
app.include_router(price_routes, prefix="/prices")
app.include_router(admin_routes, prefix="/admin")

# Pages
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signin", response_class=HTMLResponse)
def signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

# Background worker
@app.on_event("startup")
def start_worker():
    Thread(target=start_price_worker, daemon=True).start()
