import asyncio
import os
import uuid
from typing import List

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.specialist import Specialist
from app.models.user import User
from app.services.specialist import SpecialistService

SQLITE_URL = 'sqlite+aiosqlite:///:memory:'
POSTGRES_TEST_URL = os.getenv('TEST_POSTGRES_URL')  # e.g. postgresql+asyncpg://user:pass@localhost:5432/db

@pytest.mark.asyncio
async def test_specialist_filtering_sqlite_case_insensitive():
    """Ensure fallback LIKE filtering works (case-insensitive) under SQLite."""
    engine = create_async_engine(SQLITE_URL)
    async with engine.begin() as conn:
        # Create tables
        from app.models import base  # assuming models/__init__.py exposes Base as base
        await conn.run_sync(base.Base.metadata.create_all)

    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        # Create user + specialists
        u1 = User(email='user1@example.com', password_hash='x')
        u2 = User(email='user2@example.com', password_hash='x')
        session.add_all([u1, u2])
        await session.commit()
        await session.refresh(u1); await session.refresh(u2)

        s1 = Specialist(user_id=u1.id, bio='Bio 1', specializations=['Anxiety', 'Trauma'], hourly_rate=100.0, is_available=True)
        s2 = Specialist(user_id=u2.id, bio='Bio 2', specializations=['depression'], hourly_rate=120.0, is_available=True)
        session.add_all([s1, s2])
        await session.commit()

        results = await SpecialistService.get_specialists(session, specializations=['anxiety'])
        assert len(results) == 1
        assert results[0].id == s1.id

        results_multi = await SpecialistService.get_specialists(session, specializations=['TRAUMA', 'notfound'])
        assert len(results_multi) == 1
        assert results_multi[0].id == s1.id

@pytest.mark.asyncio
async def test_specialist_filtering_no_substring_collision_sqlite():
    """'art' must not match 'heart' when using normalization logic (association fallback)."""
    engine = create_async_engine(SQLITE_URL)
    async with engine.begin() as conn:
        from app.models import base
        await conn.run_sync(base.Base.metadata.create_all)

    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        u1 = User(email='art@example.com', password_hash='x')
        u2 = User(email='heart@example.com', password_hash='x')
        session.add_all([u1, u2])
        await session.commit(); await session.refresh(u1); await session.refresh(u2)

        s1 = Specialist(user_id=u1.id, bio='Art therapist', specializations=['art'], hourly_rate=80.0, is_available=True)
        s2 = Specialist(user_id=u2.id, bio='Heart wellness', specializations=['heart'], hourly_rate=90.0, is_available=True)
        session.add_all([s1, s2])
        await session.commit()

        r1 = await SpecialistService.get_specialists(session, specializations=['art'])
        assert len(r1) == 1 and r1[0].id == s1.id
        r2 = await SpecialistService.get_specialists(session, specializations=['heart'])
        assert len(r2) == 1 and r2[0].id == s2.id

@pytest.mark.asyncio
@pytest.mark.skipif(not POSTGRES_TEST_URL, reason="TEST_POSTGRES_URL not provided")
async def test_specialist_filtering_postgres_overlap():
    """Ensure Postgres overlap operator still functions when available."""
    engine = create_async_engine(POSTGRES_TEST_URL)
    async with engine.begin() as conn:
        from app.models import base
        await conn.run_sync(base.Base.metadata.create_all)

    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        u1 = User(email='pg1@example.com', password_hash='x')
        u2 = User(email='pg2@example.com', password_hash='x')
        session.add_all([u1, u2])
        await session.commit()
        await session.refresh(u1); await session.refresh(u2)

        s1 = Specialist(user_id=u1.id, bio='PG Bio 1', specializations=['anxiety', 'stress'], hourly_rate=90.0, is_available=True)
        s2 = Specialist(user_id=u2.id, bio='PG Bio 2', specializations=['depression'], hourly_rate=110.0, is_available=True)
        session.add_all([s1, s2])
        await session.commit()

        results = await SpecialistService.get_specialists(session, specializations=['stress'])
        assert len(results) == 1 and results[0].id == s1.id

        results_case = await SpecialistService.get_specialists(session, specializations=['ANXIETY'])
        assert len(results_case) == 1 and results_case[0].id == s1.id
