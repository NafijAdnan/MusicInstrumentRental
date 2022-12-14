"""empty message

Revision ID: 846f2ef0ebb6
Revises: 9747c31d97e1
Create Date: 2022-12-14 06:33:52.285396

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '846f2ef0ebb6'
down_revision = '9747c31d97e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instrument', schema=None) as batch_op:
        batch_op.alter_column('approval',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.String(length=8),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instrument', schema=None) as batch_op:
        batch_op.alter_column('approval',
               existing_type=sa.String(length=8),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)

    # ### end Alembic commands ###
