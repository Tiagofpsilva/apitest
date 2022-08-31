"""add phone number

Revision ID: 214cb0866b11
Revises: ab54b090c8f3
Create Date: 2022-08-31 10:53:39.977586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '214cb0866b11'
down_revision = 'ab54b090c8f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
