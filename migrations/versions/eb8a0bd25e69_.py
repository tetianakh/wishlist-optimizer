"""empty message

Revision ID: eb8a0bd25e69
Revises: 72107fd5d8aa
Create Date: 2018-11-08 20:59:27.408769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb8a0bd25e69'
down_revision = '72107fd5d8aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_name_mkm_id', 'language', ['name', 'mkm_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_name_mkm_id', 'language', type_='unique')
    # ### end Alembic commands ###