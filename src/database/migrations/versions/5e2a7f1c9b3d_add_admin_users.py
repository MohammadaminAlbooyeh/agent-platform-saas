"""add admin_users

Revision ID: 5e2a7f1c9b3d
Revises: 38c99749e0be
Create Date: 2026-11-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e2a7f1c9b3d'
down_revision: Union[str, None] = '38c99749e0be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('admin_users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_users_username'), 'admin_users', ['username'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_admin_users_username'), table_name='admin_users')
    op.drop_table('admin_users')
