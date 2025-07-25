"""Add active_city_id to players

Revision ID: e689cea57c23
Revises: daf5e474e5fd
Create Date: 2025-07-15 13:08:23.881973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e689cea57c23'
down_revision: Union[str, Sequence[str], None] = 'daf5e474e5fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('unit_types')
    op.add_column('players', sa.Column('active_city_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'players', 'cities', ['active_city_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'players', type_='foreignkey')
    op.drop_column('players', 'active_city_id')
    op.create_table('unit_types',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('base_training_time', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('base_attack', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('base_defense', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('base_cost', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('base_speed', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('base_carry_capacity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('base_range', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('base_life', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('population_cost', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('upkeep_cost', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('unit_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('unlock_requirements', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('required_building', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('required_research', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('special_ability', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('unit_types_pkey')),
    sa.UniqueConstraint('name', name=op.f('unit_types_name_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    # ### end Alembic commands ###
