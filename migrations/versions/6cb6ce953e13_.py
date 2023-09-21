"""empty message

Revision ID: 6cb6ce953e13
Revises: 
Create Date: 2023-09-21 14:23:37.262219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cb6ce953e13'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=100), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.Column('public_id', sa.String(length=100), nullable=True),
    sa.Column('last_password_reset', sa.DateTime(), nullable=True),
    sa.Column('password_changed', sa.DateTime(), nullable=True),
    sa.Column('reset_token', sa.String(length=255), nullable=True),
    sa.Column('reset_token_expiration', sa.DateTime(), nullable=True),
    sa.Column('verification_token', sa.String(length=255), nullable=True),
    sa.Column('email_verified', sa.Boolean(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###