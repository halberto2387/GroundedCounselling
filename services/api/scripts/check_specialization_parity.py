"""Parity check for specialization normalization.

Usage:
  python -m scripts.check_specialization_parity [--database-url DB_URL]

If --database-url not provided, falls back to DATABASE_URL env var or sqlite memory.

Reports:
  - Total specialists
  - Specialists with mismatched counts (JSON list length vs association rows)
  - First N mismatch examples
  - Exit code 0 if all match, 1 otherwise
"""
from __future__ import annotations
import os
import argparse
import asyncio
from typing import List, Tuple, Dict, Any
import json
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func

from app.models.specialist import Specialist
from app.models.specialization import SpecialistSpecialization

DEFAULT_DB = 'sqlite+aiosqlite:///:memory:'

async def gather_parity(session: AsyncSession, sample: int = 10) -> Tuple[int, int, List[Tuple[int,int,int]]]:
    total = (await session.execute(select(func.count(Specialist.id)))).scalar_one()
    mismatches: List[Tuple[int,int,int]] = []

    # Iterate specialists in batches to keep memory low
    batch = 200
    offset = 0
    while True:
        rows = (await session.execute(select(Specialist.id, Specialist.specializations).offset(offset).limit(batch))).all()
        if not rows:
            break
        offset += len(rows)
        ids = [r.id for r in rows]
        assoc_counts = (await session.execute(
            select(SpecialistSpecialization.specialist_id, func.count())
            .where(SpecialistSpecialization.specialist_id.in_(ids))
            .group_by(SpecialistSpecialization.specialist_id)
        )).all()
        counts_map = {sid: cnt for sid, cnt in assoc_counts}
        for r in rows:
            json_len = len(r.specializations or [])
            assoc_len = counts_map.get(r.id, 0)
            if json_len != assoc_len:
                mismatches.append((r.id, json_len, assoc_len))
                if len(mismatches) >= sample:
                    # Keep collecting full mismatch list length? For now we stop sampling early
                    pass
    return total, len(mismatches), mismatches[:sample]

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database-url', dest='db_url', default=None)
    parser.add_argument('--sample', type=int, default=10)
    parser.add_argument('--output', type=str, default='parity_report.json', help='Path to write JSON report')
    args = parser.parse_args()

    db_url = args.db_url or os.getenv('DATABASE_URL') or DEFAULT_DB
    engine = create_async_engine(db_url, future=True)
    async with engine.begin() as conn:
        # Do not auto-create metadata here; expect migrations already applied
        pass
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        total, mismatch_count, examples = await gather_parity(session, sample=args.sample)
    report: Dict[str, Any] = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'total_specialists': total,
        'mismatch_total': mismatch_count,
        'examples': [
            {
                'specialist_id': sid,
                'json_count': json_len,
                'association_count': assoc_len,
            }
            for sid, json_len, assoc_len in examples
        ],
        'parity': mismatch_count == 0,
        'sample_limit': args.sample,
    }
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"Total specialists: {total}")
    if mismatch_count == 0:
        print("All specialists have parity between JSON and association rows ✅")
        print(f"Report: {args.output}")
        exit(0)
    else:
        print(f"Mismatched specialists: {mismatch_count}")
        for ex in report['examples']:
            print(f"  Specialist {ex['specialist_id']}: JSON={ex['json_count']} vs Assoc={ex['association_count']}")
        print(f"Report: {args.output}")
        exit(1)

if __name__ == '__main__':
    asyncio.run(main())
