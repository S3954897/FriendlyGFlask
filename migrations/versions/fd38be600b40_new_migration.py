"""New Migration

Revision ID: fd38be600b40
Revises: 7d96ebd19353
Create Date: 2023-04-09 16:19:00.475743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd38be600b40'
down_revision = '7d96ebd19353'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_path', sa.String(length=200), nullable=False))
        batch_op.drop_column('adFilePath')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('adFilePath', sa.VARCHAR(length=200), nullable=False))
        batch_op.drop_column('file_path')

    # ### end Alembic commands ###
