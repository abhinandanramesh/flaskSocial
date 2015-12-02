"""empty message

Revision ID: 6586d640e92
Revises: 3aa699fb8a0
Create Date: 2015-12-01 20:29:02.104067

"""

# revision identifiers, used by Alembic.
revision = '6586d640e92'
down_revision = '3aa699fb8a0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'comments_parent_fkey', 'comments', type_='foreignkey')
    op.drop_column('comments', 'parent')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('parent', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'comments_parent_fkey', 'comments', 'posts', ['parent'], ['id'])
    ### end Alembic commands ###
