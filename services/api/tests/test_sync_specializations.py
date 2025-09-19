import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.models.specialist import Specialist
from app.models.specialization import Specialization, SpecialistSpecialization
from app.services.specialist import SpecialistService

SQLITE_URL = 'sqlite+aiosqlite:///:memory:'

@pytest.mark.asyncio
async def test_sync_specializations_create_and_update():
    engine = create_async_engine(SQLITE_URL)
    async with engine.begin() as conn:
        from app.models import base
        await conn.run_sync(base.Base.metadata.create_all)

    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        # Create specialist (no JSON specializations column anymore)
        spec = Specialist(user_id=1, bio='Test', is_available=True)
        session.add(spec)
        await session.flush()

        # Initial sync via association table
        await SpecialistService._sync_specializations(session, spec, ['Anxiety', 'Depression'])
        await session.commit()

        # Verify rows
        all_specs = (await session.execute(select(Specialization))).scalars().all()
        assert {s.slug for s in all_specs} == {'anxiety', 'depression'}
        links = (await session.execute(select(SpecialistSpecialization).where(SpecialistSpecialization.specialist_id == spec.id))).scalars().all()
        assert len(links) == 2

        # Idempotent re-sync (no duplicates)
        await SpecialistService._sync_specializations(session, spec, ['Anxiety', 'Depression'])
        await session.commit()
        links2 = (await session.execute(select(SpecialistSpecialization).where(SpecialistSpecialization.specialist_id == spec.id))).scalars().all()
        assert len(links2) == 2

        # Remove one and add one
        await SpecialistService._sync_specializations(session, spec, ['Depression', 'Trauma'])
        await session.commit()
        links3 = (await session.execute(select(SpecialistSpecialization).where(SpecialistSpecialization.specialist_id == spec.id))).scalars().all()
        # Should have 2 associations (depression, trauma)
        assert len(links3) == 2
        spec_slugs = { (await session.get(Specialization, l.specialization_id)).slug for l in links3 }
        assert spec_slugs == {'depression', 'trauma'}
