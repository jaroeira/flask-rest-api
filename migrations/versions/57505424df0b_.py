"""empty message

Revision ID: 57505424df0b
Revises: 6f3a932c617a
Create Date: 2023-09-27 14:15:21.729305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57505424df0b'
down_revision = '6f3a932c617a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_images',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('image_url', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article_images')
    # ### end Alembic commands ###
