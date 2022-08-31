"""add user table

Revision ID: 52028674b52e
Revises: 1cdf6235be59
Create Date: 2022-08-29 18:02:33.217739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52028674b52e'
down_revision = '1cdf6235be59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')           
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
