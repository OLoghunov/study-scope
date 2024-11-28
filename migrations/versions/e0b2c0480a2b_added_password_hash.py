"""added password hash

Revision ID: e0b2c0480a2b
Revises: a8e79a923ec3
Create Date: 2024-11-29 00:18:44.386363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e0b2c0480a2b'
down_revision: Union[str, None] = 'a8e79a923ec3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('passwordHash', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'passwordHash')
    # ### end Alembic commands ###