"""empty message

Revision ID: 36c679d720d5
Revises: None
Create Date: 2015-11-28 20:02:32.428783

"""

# revision identifiers, used by Alembic.
revision = '36c679d720d5'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('friend_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_sent_from', sa.Integer(), nullable=True),
    sa.Column('user_sent_to', sa.Integer(), nullable=True),
    sa.Column('accepted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_sent_from'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_sent_to'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('friends',
    sa.Column('friend1_id', sa.Integer(), nullable=True),
    sa.Column('friend2_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['friend1_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['friend2_id'], ['users.id'], )
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('poster', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['poster'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_table',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['posts.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association_table')
    op.drop_table('posts')
    op.drop_table('friends')
    op.drop_table('friend_requests')
    op.drop_table('users')
    ### end Alembic commands ###