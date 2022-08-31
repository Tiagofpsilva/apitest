"""create posts table

Revision ID: 01e057531200
Revises: 
Create Date: 2022-08-29 17:41:20.617113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01e057531200'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
