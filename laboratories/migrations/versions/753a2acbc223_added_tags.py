"""Added Tags

Revision ID: 753a2acbc223
Revises: bb32053a99e0
Create Date: 2023-11-23 01:55:09.410757

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '753a2acbc223'
down_revision = 'bb32053a99e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    # ### end Alembic commands ###
