"""checking votes table

Revision ID: bf2de9caa8db
Revises: 189953bcc4d9
Create Date: 2024-11-13 09:46:41.207891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'bf2de9caa8db'
down_revision: Union[str, None] = '189953bcc4d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vote', 'temp')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vote', sa.Column('temp', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
