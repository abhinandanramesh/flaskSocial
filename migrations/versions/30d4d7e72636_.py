"""empty message

Revision ID: 30d4d7e72636
Revises: 23068abd2aff
Create Date: 2015-12-01 21:20:51.076095

"""

# revision identifiers, used by Alembic.
revision = '30d4d7e72636'
down_revision = '23068abd2aff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('group', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'groups', ['group'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'group')
    ### end Alembic commands ###