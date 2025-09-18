from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.security.password import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, password_hash=hash_password(payload.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/login", response_model=UserOut)
async def login(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user
