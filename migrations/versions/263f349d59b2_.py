"""empty message

Revision ID: 263f349d59b2
Revises: 2c209685dc22
Create Date: 2015-12-04 14:11:27.977034

"""

# revision identifiers, used by Alembic.
revision = '263f349d59b2'
down_revision = '2c209685dc22'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    ### end Alembic commands ###
