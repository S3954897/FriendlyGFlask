"""modify class ShopAds

Revision ID: 59a2d2aa5e34
Revises: 4277a2b8393f
Create Date: 2023-04-19 17:51:01.596167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59a2d2aa5e34'
down_revision = '4277a2b8393f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shop_ads')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shop_ads',
    sa.Column('displayID', sa.INTEGER(), nullable=False),
    sa.Column('adID', sa.INTEGER(), nullable=False),
    sa.Column('shopID', sa.INTEGER(), nullable=False),
    sa.Column('adOrder', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['adID'], ['advertisements.adID'], ),
    sa.ForeignKeyConstraint(['displayID'], ['displays.displayID'], ),
    sa.ForeignKeyConstraint(['shopID'], ['shops.shopID'], ),
    sa.PrimaryKeyConstraint('displayID', 'adID', 'shopID')
    )
    # ### end Alembic commands ###