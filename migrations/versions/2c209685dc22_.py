"""empty message

Revision ID: 2c209685dc22
Revises: None
Create Date: 2015-12-04 11:01:36.684434

"""

# revision identifiers, used by Alembic.
revision = '2c209685dc22'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banned_members',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('banned_members')
    ### end Alembic commands ###
