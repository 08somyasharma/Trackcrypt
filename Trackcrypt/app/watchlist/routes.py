from fastapi import APIRouter, Request, Depends
from app.middleware.auth import auth_middleware
from app.watchlist.controller import add_alert, list_alerts

router = APIRouter()


@router.post("/")
async def add_alert_route(
    request: Request,
    _=Depends(auth_middleware)
):
    data = await request.json()
    user_id = request.state.user_id
    return add_alert(user_id, data)


@router.get("/")
def list_alerts_route(
    request: Request,
    _=Depends(auth_middleware)
):
    user_id = request.state.user_id
    return list_alerts(user_id)
