"""add foreign-key to posts table

Revision ID: 05ffea6ea8fc
Revises: 52028674b52e
Create Date: 2022-08-30 19:10:46.171681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05ffea6ea8fc'
down_revision = '52028674b52e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
