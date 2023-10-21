"""add_foregin_key_to_post_table

Revision ID: 60aa5cc650d0
Revises: 2494786e4d38
Create Date: 2023-10-21 13:53:25.288024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60aa5cc650d0'
down_revision: Union[str, None] = '2494786e4d38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer()))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                         local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
