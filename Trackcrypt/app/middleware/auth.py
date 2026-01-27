from fastapi import Request, HTTPException, Depends
from functools import wraps
from app.auth.jwt import verify_token

# --- Regular auth middleware ---
def auth_middleware(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    decoded = verify_token(token)
    request.state.user_id = decoded.get("userId")
    request.state.role = decoded.get("role")  # save role for admin check
    return decoded


# --- Admin decorator for routes ---
def admin_required(request: Request = Depends(auth_middleware)):
    """
    Dependency for admin routes.
    Ensures that the JWT belongs to an admin.
    """
    if request.state.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return request
