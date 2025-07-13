"""Created Army Model

Revision ID: c5c44d0baa4d
Revises: 4047da8e0508
Create Date: 2025-07-13 07:02:49.752717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql



# revision identifiers, used by Alembic.
revision: str = 'c5c44d0baa4d'
down_revision: Union[str, Sequence[str], None] = '4047da8e0508'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Change base_cost from INTEGER to JSONB
    op.alter_column(
        'unit_types',
        'base_cost',
        type_=postgresql.JSONB(),
        postgresql_using='base_cost::jsonb'
    )

def downgrade():
    # Change base_cost back to INTEGER (will fail if data is not integer-compatible)
    op.alter_column(
        'unit_types',
        'base_cost',
        type_=sa.Integer(),
        postgresql_using='base_cost::integer'
    )
