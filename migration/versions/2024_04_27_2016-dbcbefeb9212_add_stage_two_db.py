"""Add stage two db

Revision ID: dbcbefeb9212
Revises: 0545cabfa9e2
Create Date: 2024-04-27 20:16:43.242218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbcbefeb9212'
down_revision: Union[str, None] = '0545cabfa9e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('regionsstagetwos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('region', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('regionsstagetwos')
    # ### end Alembic commands ###
