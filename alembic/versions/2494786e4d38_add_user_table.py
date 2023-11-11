"""add_user_table

Revision ID: 2494786e4d38
Revises: 467d62683d8a
Create Date: 2023-10-21 08:22:34.072906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2494786e4d38'
down_revision: Union[str, None] = '467d62683d8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer()),
                    sa.Column('email', sa.String()),
                    sa.Column('password', sa.String()),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
