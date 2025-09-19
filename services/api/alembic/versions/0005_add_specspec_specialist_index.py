"""Add index on specialist_specializations.specialist_id

Revision ID: 0005_add_specspec_specialist_index
Revises: 0004_backfill_specializations
Create Date: 2025-09-19 00:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0005_add_specspec_specialist_index'
down_revision = '0004_backfill_specializations'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_index('ix_specspec_specialist_id', 'specialist_specializations', ['specialist_id'])


def downgrade() -> None:
    op.drop_index('ix_specspec_specialist_id', table_name='specialist_specializations')
