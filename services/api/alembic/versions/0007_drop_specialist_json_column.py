"""Drop specialists.specializations JSON column

Revision ID: 0007_drop_specialist_json_column
Revises: 0006_drop_specialist_json_field_placeholder
Create Date: 2025-09-19 01:05:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0007_drop_specialist_json_column'
down_revision = '0006_drop_specialist_json_field_placeholder'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.drop_column('specialists', 'specializations')


def downgrade() -> None:
    # Recreate column (data cannot be restored automatically)
    op.add_column('specialists', sa.Column('specializations', sa.JSON(), nullable=False, server_default='[]'))
