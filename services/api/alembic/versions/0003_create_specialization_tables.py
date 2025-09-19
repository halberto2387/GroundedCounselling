"""Create specialization and association tables

Revision ID: 0003_create_specialization_tables
Revises: 323c08db1e6f
Create Date: 2025-09-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_create_specialization_tables'
down_revision = '323c08db1e6f'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'specializations',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=150), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.UniqueConstraint('slug', name='uq_specializations_slug'),
    )
    op.create_index('ix_specializations_slug', 'specializations', ['slug'])

    op.create_table(
        'specialist_specializations',
        sa.Column('specialist_id', sa.Integer(), nullable=False),
        sa.Column('specialization_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['specialist_id'], ['specialists.id'], name='fk_specspec_specialist_id_specialists', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['specialization_id'], ['specializations.id'], name='fk_specspec_specialization_id_specializations', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('specialist_id', 'specialization_id', name='pk_specialist_specializations'),
    )
    op.create_index('ix_specspec_specialization_id', 'specialist_specializations', ['specialization_id'])


def downgrade() -> None:
    op.drop_index('ix_specspec_specialization_id', table_name='specialist_specializations')
    op.drop_table('specialist_specializations')
    op.drop_index('ix_specializations_slug', table_name='specializations')
    op.drop_table('specializations')
