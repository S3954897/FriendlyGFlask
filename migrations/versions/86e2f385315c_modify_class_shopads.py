"""modify class ShopAds

Revision ID: 86e2f385315c
Revises: 59a2d2aa5e34
Create Date: 2023-04-19 18:04:10.490074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86e2f385315c'
down_revision = '59a2d2aa5e34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shop_ads',
    sa.Column('menuAdID', sa.Integer(), nullable=False),
    sa.Column('adID', sa.Integer(), nullable=True),
    sa.Column('menuID', sa.Integer(), nullable=True),
    sa.Column('adOrder', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['adID'], ['advertisements.adID'], name='shop_ads_ad_id_fkey'),
    sa.ForeignKeyConstraint(['menuID'], ['shop_menus.shopMenuID'], name='shop_ads_shop_menu_id_fkey'),
    sa.PrimaryKeyConstraint('menuAdID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shop_ads')
    # ### end Alembic commands ###
