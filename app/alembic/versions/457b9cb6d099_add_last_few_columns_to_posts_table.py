"""add last few columns to posts table

Revision ID: 457b9cb6d099
Revises: 05ffea6ea8fc
Create Date: 2022-08-30 19:15:14.134245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '457b9cb6d099'
down_revision = '05ffea6ea8fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
