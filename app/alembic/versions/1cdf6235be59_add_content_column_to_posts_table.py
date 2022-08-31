"""add content column to posts table

Revision ID: 1cdf6235be59
Revises: 01e057531200
Create Date: 2022-08-29 17:55:18.816586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cdf6235be59'
down_revision = '01e057531200'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
