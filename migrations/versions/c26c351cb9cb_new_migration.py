"""New Migration

Revision ID: c26c351cb9cb
Revises: f23c00727037
Create Date: 2023-04-10 00:42:09.899096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c26c351cb9cb'
down_revision = 'f23c00727037'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('primaryUserID', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fkAdUsers', 'users', ['primaryUserID'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('advertisements', schema=None) as batch_op:
        batch_op.drop_constraint('fkAdUsers', type_='foreignkey')
        batch_op.drop_column('primaryUserID')

    # ### end Alembic commands ###
