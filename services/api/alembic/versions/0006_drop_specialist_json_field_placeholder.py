"""Placeholder: Drop specialists.specializations JSON field (DO NOT APPLY YET)

Revision ID: 0006_drop_specialist_json_field_placeholder
Revises: 0005_add_specspec_specialist_index
Create Date: 2025-09-19 00:40:00.000000

This migration is a placeholder and should only be activated after sustained
parity (JSON vs association) has been confirmed for N consecutive days.

Activation steps when ready:
1. Ensure parity workflow has reported 0 mismatches for at least N days.
2. Communicate change to stakeholders / deploy window.
3. Replace `raise RuntimeError` with actual DDL to drop column:
     op.drop_column('specialists', 'specializations')
4. Optionally create a backup export beforehand.

Rollback considerations:
- Re-adding the JSON column would lose historical data unless separately archived.
- Prefer delaying removal until you're certain the JSON column is unused.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0006_drop_specialist_json_field_placeholder'
down_revision = '0005_add_specspec_specialist_index'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Safety guard: prevent accidental application
    raise RuntimeError('Placeholder migration not yet intended for application.')


def downgrade() -> None:
    # No-op; placeholder only.
    pass
