"""add quota_overrides

Revision ID: 8f4c1d2a6e71
Revises: 5e2a7f1c9b3d
Create Date: 2026-11-16 00:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f4c1d2a6e71'
down_revision: Union[str, None] = '5e2a7f1c9b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('quota_overrides',
    sa.Column('tenant_id', sa.String(), nullable=False),
    sa.Column('token_limit', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('tenant_id')
    )


def downgrade() -> None:
    op.drop_table('quota_overrides')
