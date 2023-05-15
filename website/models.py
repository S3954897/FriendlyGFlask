from . import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    userType = db.Column(db.Integer)
    shops = db.relationship('Shops', backref='user')
    items = db.relationship('Items', backref='user')


class Shops(db.Model):
    shopID = db.Column(db.Integer, primary_key=True)
    shopName = db.Column(db.String(50), nullable=False)
    shopAddress = db.Column(db.String(120), nullable=False)
    primaryUserID = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_shops_users'))
    displays = db.relationship('Displays', back_populates='shops')

class Displays(db.Model):
    displayID = db.Column(db.Integer, primary_key=True)
    shopID = db.Column(db.Integer, db.ForeignKey('shops.shopID', name='fk_shops_shopID'))
    shopMenus = db.relationship('ShopMenus', backref='display')
    shops = db.relationship('Shops', back_populates='displays')


class Advertisements(db.Model):
    adID = db.Column(db.Integer, primary_key=True)
    adName = db.Column(db.String(50))
    file_path = db.Column(db.String(200), nullable=False)
    thumbnail_path = db.Column(db.String(150), nullable=False)
    primaryUserID = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_advertisements_users'))
    shopAd = db.relationship('ShopAds', backref='Advertisement')


class ShopAds(db.Model):
    menuAdID = db.Column(db.Integer, primary_key=True)
    adID = db.Column(db.Integer, db.ForeignKey('advertisements.adID', name='shop_ads_ad_id_fkey'))
    menuID = db.Column(db.Integer, db.ForeignKey('shop_menus.shopMenuID', name='shop_ads_shop_menu_id_fkey'))
    adOrder = db.Column(db.Integer, nullable=False)
    advertisement = db.relationship('Advertisements', back_populates='shopAd', viewonly=True)


class Items(db.Model):
    itemID = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(50), nullable=False)
    itemPrice = db.Column(db.String(50), nullable=False)
    itemSubitem = db.Column(db.String(120))
    primaryUserID = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_items_users'))
    menuitems = db.relationship('MenuItems', back_populates='item')


class Menus(db.Model):
    menuID = db.Column(db.Integer, primary_key=True)
    menuType = db.Column(db.String(50))
    # menuitems = db.relationship('MenuItems', backref='menu')


class ShopMenus(db.Model):
    shopMenuID = db.Column(db.Integer, primary_key=True)
    displayID = db.Column(db.Integer, db.ForeignKey('displays.displayID', name='fk_shop_menus_display_id'))
    menuTypeID = db.Column(db.Integer, db.ForeignKey('menus.menuID', name='fk_shops_menus_menu_type_id'))
    menuTitle = db.Column(db.String(50), nullable=False)
    menuStartTime = db.Column(db.Time, nullable=False)
    menuFinishTime = db.Column(db.Time, nullable=False)
    menuActive = db.Column(db.Boolean, nullable=False)
    # menuitems = db.relationship('MenuItems', backref='shop_menu')


class MenuItems(db.Model):
    menuItemID = db.Column(db.Integer, primary_key=True)
    itemID = db.Column(db.Integer, db.ForeignKey('items.itemID', name='fk_menu_items_item_id'))
    menuID = db.Column(db.Integer, db.ForeignKey('shop_menus.shopMenuID', name='fk_menu_items_menu_id'))
    groupID = db.Column(db.Integer, nullable=False)
    itemOrder = db.Column(db.Integer, nullable=False)
    item = db.relationship('Items', back_populates='menuitems')


class DisplayMenu(db.Model):
    displayMenuID = db.Column(db.Integer, primary_key=True)
    displayID = db.Column(db.Integer, db.ForeignKey('displays.displayID', name='fk_display_menu_display_id'))
    shopMenuID = db.Column(db.Integer, db.ForeignKey('menus.menuID', name='fk_display_menu_shop_menu_id'))
