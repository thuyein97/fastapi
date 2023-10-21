"""add content column to posts table

Revision ID: 467d62683d8a
Revises: d4400ffaab5f
Create Date: 2023-10-21 08:07:09.801767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '467d62683d8a'
down_revision: Union[str, None] = 'd4400ffaab5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String()))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
