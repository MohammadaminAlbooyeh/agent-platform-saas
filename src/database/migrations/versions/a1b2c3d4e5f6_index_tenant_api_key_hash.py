"""index tenant api_key_hash

Revision ID: a1b2c3d4e5f6
Revises: 8f4c1d2a6e71
Create Date: 2026-11-16 00:20:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '8f4c1d2a6e71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Lets the tenant-resolution middleware look up a tenant by its API key
    # hash directly instead of scanning and verifying every tenant row.
    op.create_index(op.f('ix_tenants_api_key_hash'), 'tenants', ['api_key_hash'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_tenants_api_key_hash'), table_name='tenants')
