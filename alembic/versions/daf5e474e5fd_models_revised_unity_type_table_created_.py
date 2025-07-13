"""Models revised, unity_type table created and updated

Revision ID: daf5e474e5fd
Revises: 95f9a2fab17b
Create Date: 2025-07-13 10:44:43.852069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'daf5e474e5fd'
down_revision: Union[str, Sequence[str], None] = '95f9a2fab17b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from sqlalchemy.dialects import postgresql
    op.alter_column(
        'unit_types',
        'base_cost',
        type_=postgresql.JSONB(),
        postgresql_using='base_cost::jsonb'
    )


def downgrade() -> None:
    op.alter_column(
        'unit_types',
        'base_cost',
        type_=sa.Integer(),
        postgresql_using='base_cost::integer'
    )
