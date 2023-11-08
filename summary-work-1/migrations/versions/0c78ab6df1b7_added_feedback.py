"""Added feedback

Revision ID: 0c78ab6df1b7
Revises: 82b526db21e0
Create Date: 2023-11-02 18:00:56.928393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c78ab6df1b7'
down_revision = '82b526db21e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feedback', sa.String(), nullable=False),
    sa.Column('satisfaction', sa.Enum('VERY_SATISFIED', 'SATISFIED', 'DISSATISFIED', name='satisfaction'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    # ### end Alembic commands ###