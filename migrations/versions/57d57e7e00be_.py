"""empty message

Revision ID: 57d57e7e00be
Revises: 8cf203d813d3
Create Date: 2018-11-15 21:02:27.010465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57d57e7e00be'
down_revision = '8cf203d813d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revoked_token')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revoked_token',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('jwt', sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='revoked_token_pkey')
    )
    # ### end Alembic commands ###
