from fastapi import APIRouter, HTTPException, status

from schemas.users import User, UserCreate

router = APIRouter()
router.redirect_slashes=False

@router.get("/")
async def all() -> list[User]:
    pass

@router.get("/{id}")
async def get(id: int) -> User:
    return None

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(user_create: UserCreate) -> User:
    pass

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int) -> None:
    pass
