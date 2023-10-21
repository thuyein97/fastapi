"""create_post_table

Revision ID: d4400ffaab5f
Revises: 
Create Date: 2023-10-20 20:20:06.715808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4400ffaab5f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('title', sa.String()))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
