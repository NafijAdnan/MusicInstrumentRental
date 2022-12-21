"""empty message

Revision ID: 464167eea629
Revises: 66aea1f4f15e
Create Date: 2022-12-21 17:42:01.809017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '464167eea629'
down_revision = '66aea1f4f15e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('paid', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('paid')

    # ### end Alembic commands ###