"""relate users to books

Revision ID: 25fef707a831
Revises: 7606d687f72a
Create Date: 2025-01-13 18:30:49.040447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '25fef707a831'
down_revision: Union[str, None] = '7606d687f72a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('userUid', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'books', 'users', ['userUid'], ['uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'userUid')
    # ### end Alembic commands ###
