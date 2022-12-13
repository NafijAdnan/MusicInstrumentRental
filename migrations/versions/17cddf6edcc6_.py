"""empty message

Revision ID: 17cddf6edcc6
Revises: c68540ae7037
Create Date: 2022-12-14 04:17:43.118045

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '17cddf6edcc6'
down_revision = 'c68540ae7037'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instrument', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=20), nullable=True))
        batch_op.drop_constraint('instrument_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['username'], ['username'])
        batch_op.drop_column('user')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instrument', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user', mysql.VARCHAR(length=20), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('instrument_ibfk_1', 'user', ['user'], ['username'])
        batch_op.drop_column('username')

    # ### end Alembic commands ###
