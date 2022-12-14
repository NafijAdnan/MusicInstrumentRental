"""empty message

Revision ID: c459406224bd
Revises: 24c0c51f9981
Create Date: 2022-12-20 19:36:37.331427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c459406224bd'
down_revision = '24c0c51f9981'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('voucher', sa.String(length=15), nullable=True))
        batch_op.create_foreign_key(None, 'coupon', ['voucher'], ['code'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('voucher')

    # ### end Alembic commands ###
