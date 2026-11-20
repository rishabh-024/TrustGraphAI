from fastapi import APIRouter, Depends

from app.models import User
from app.security.dependencies import require_roles

router = APIRouter(prefix="/api/access", tags=["Role Access"])


@router.get("/admin")
def admin_access(
    user: User = Depends(require_roles("admin")),
):
    return {"message": "Admin access granted"}


@router.get("/analyst")
def analyst_access(
    user: User = Depends(require_roles("admin", "analyst")),
):
    return {"message": "Analyst access granted"}


@router.get("/approver")
def approver_access(
    user: User = Depends(require_roles("admin", "approver")),
):
    return {"message": "Approver access granted"}