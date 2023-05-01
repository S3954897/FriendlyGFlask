"""New Migration

Revision ID: 2b918c824530
Revises: fd38be600b40
Create Date: 2023-04-09 16:26:51.988252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b918c824530'
down_revision = 'fd38be600b40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.alter_column('adName',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.alter_column('adName',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###
