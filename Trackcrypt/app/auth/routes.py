from fastapi import APIRouter, Request
from app.auth.controller import signup, signin

router = APIRouter()


@router.post("/signup")
async def signup_route(request: Request):
    data = await request.json()
    return signup(data)


@router.post("/signin")
async def signin_route(request: Request):
    data = await request.json()
    return signin(data)
