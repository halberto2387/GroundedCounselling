"""Backfill specialization tables from legacy JSON field

Revision ID: 0004_backfill_specializations
Revises: 0003_create_specialization_tables
Create Date: 2025-09-19 00:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select
from sqlalchemy import String, Integer, JSON, text

# revision identifiers, used by Alembic.
revision = '0004_backfill_specializations'
down_revision = '0003_create_specialization_tables'
branch_labels = None
depends_on = None

BATCH_SIZE = 200

def upgrade() -> None:
    conn = op.get_bind()

    specialists_tbl = table(
        'specialists',
        column('id', Integer),
        column('specializations', JSON),
    )
    specializations_tbl = table(
        'specializations',
        column('id', Integer),
        column('slug', String),
        column('display_name', String),
    )
    assoc_tbl = table(
        'specialist_specializations',
        column('specialist_id', Integer),
        column('specialization_id', Integer),
    )

    # Helper: slug normalization mirrors runtime logic (lower + hyphenation of spaces)
    def normalize_slug(raw: str) -> str:
        if raw is None:
            return ''
        s = raw.strip().lower()
        s = ' '.join(s.split())
        return s.replace(' ', '-')

    # Count specialists
    total = conn.execute(text('SELECT COUNT(*) FROM specialists')).scalar() or 0
    if total == 0:
        return

    offset = 0
    while offset < total:
        rows = conn.execute(
            select(specialists_tbl.c.id, specialists_tbl.c.specializations)
            .limit(BATCH_SIZE)
            .offset(offset)
        ).all()
        if not rows:
            break
        offset += len(rows)

        # Collect slugs for this batch
        slug_map = {}  # slug -> display_name (first occurrence title-cased by replacing '-' with space)
        spec_by_specialist = {}  # specialist_id -> set(slug)
        for r in rows:
            raw_list = r.specializations or []
            norm_set = set()
            for raw in raw_list:
                if not raw:
                    continue
                slug = normalize_slug(str(raw))
                if not slug:
                    continue
                norm_set.add(slug)
                if slug not in slug_map:
                    display = slug.replace('-', ' ').title()
                    slug_map[slug] = display
            if norm_set:
                spec_by_specialist[r.id] = norm_set

        if not slug_map:
            continue

        # Insert new specialization slugs (ignore duplicates)
        for slug, display in slug_map.items():
            try:
                conn.execute(
                    sa.text(
                        'INSERT INTO specializations (slug, display_name) VALUES (:slug, :display) ON CONFLICT(slug) DO NOTHING'
                    ),
                    {'slug': slug, 'display': display},
                )
            except Exception:
                # SQLite (without ON CONFLICT slug unique?) or other dialect edge: fallback to silent ignore
                pass

        # Fetch IDs for all slugs in this batch
        slug_rows = conn.execute(
            select(specializations_tbl.c.id, specializations_tbl.c.slug).where(
                specializations_tbl.c.slug.in_(list(slug_map.keys()))
            )
        ).all()
        ids_by_slug = {r.slug: r.id for r in slug_rows}

        # Build association rows
        assoc_inserts = []
        for spec_id, norm_slugs in spec_by_specialist.items():
            for slug in norm_slugs:
                sid = ids_by_slug.get(slug)
                if sid:
                    assoc_inserts.append({'specialist_id': spec_id, 'specialization_id': sid})

        # Insert associations ignoring duplicates
        for rec in assoc_inserts:
            try:
                conn.execute(
                    sa.text(
                        'INSERT INTO specialist_specializations (specialist_id, specialization_id) VALUES (:specialist_id, :specialization_id) ON CONFLICT DO NOTHING'
                    ),
                    rec,
                )
            except Exception:
                # Fallback naive duplicate avoidance for SQLite versions lacking syntax
                pass


def downgrade() -> None:
    # Backfill is irreversible without losing data; leave tables intact, or optionally truncate associations.
    # No-op downgrade to avoid destructive data loss tied to earlier revision.
    pass
