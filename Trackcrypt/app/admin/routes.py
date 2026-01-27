from fastapi import APIRouter, Depends
from app.middleware.auth import admin_required
from app.db.dynamo import users_table, watchlist_table

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(dep=Depends(admin_required)):
    # Fetch all users
    users_resp = users_table.scan()
    users = users_resp.get("Items", [])

    # Fetch all watchlists
    wl_resp = watchlist_table.scan()
    watchlists = wl_resp.get("Items", [])

    return {
        "users": users,
        "watchlists": watchlists
    }
