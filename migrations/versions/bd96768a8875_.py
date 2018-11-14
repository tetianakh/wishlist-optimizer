"""empty message

Revision ID: bd96768a8875
Revises: eb8a0bd25e69
Create Date: 2018-11-12 16:06:41.243819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd96768a8875'
down_revision = 'eb8a0bd25e69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sub', sa.Text(), nullable=False),
        sa.Column('admin', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###