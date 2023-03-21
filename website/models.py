from . import db
from flask_login import UserMixin
from sqlalchemy import Time


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
    primaryUserID = db.Column(db.Integer, db.ForeignKey('users.id'))
    displays = db.relationship('Displays', backref='shop')
    shopAds = db.relationship('ShopAds', backref='shop')


class Displays(db.Model):
    displayID = db.Column(db.Integer, primary_key=True)
    shopID = db.Column(db.Integer, db.ForeignKey('shops.shopID'))
    shopMenus = db.relationship('ShopMenus', backref='display')
    shopAds = db.relationship('ShopAds', backref='display')


class Advertisements(db.Model):
    adID = db.Column(db.Integer, primary_key=True)
    adName = db.Column(db.String(50), nullable=False)
    adGraphic = db.Column(db.String(200), nullable=False)
    shopAds = db.relationship('ShopAds', backref='Advertisement')


class ShopAds(db.Model):
    displayID = db.Column(db.Integer, db.ForeignKey('displays.displayID'), primary_key=True)
    adID = db.Column(db.Integer, db.ForeignKey('advertisements.adID'), primary_key=True)
    shopID = db.Column(db.Integer, db.ForeignKey('shops.shopID'), primary_key=True)


class Items(db.Model):
    itemID = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(50), nullable=False)
    itemPrice = db.Column(db.String(50), nullable=False)
    primaryUserID = db.Column(db.Integer, db.ForeignKey('users.id'))
    menuitems = db.relationship('MenuItems', back_populates='item')


class Menus(db.Model):
    menuID = db.Column(db.Integer, primary_key=True)
    menuType = db.Column(db.String(50))
    # menuitems = db.relationship('MenuItems', backref='menu')


class ShopMenus(db.Model):
    shopMenuID = db.Column(db.Integer, primary_key=True)
    displayID = db.Column(db.Integer, db.ForeignKey('displays.displayID'))
    menuTypeID = db.Column(db.Integer, db.ForeignKey('menus.menuID'))
    menuTitle = db.Column(db.String(50), nullable=False)
    menuStartTime = db.Column(db.Time, nullable=False)
    menuFinishTime = db.Column(db.Time, nullable=False)
    menuActive = db.Column(db.Boolean, nullable=False)
    # menuitems = db.relationship('MenuItems', backref='shop_menu')


class MenuItems(db.Model):
    menuItemID = db.Column(db.Integer, primary_key=True)
    itemID = db.Column(db.Integer, db.ForeignKey('items.itemID'))
    menuID = db.Column(db.Integer, db.ForeignKey('shop_menus.shopMenuID'))
    groupID = db.Column(db.Integer, nullable=False)
    itemOrder = db.Column(db.Integer, nullable=False)
    item = db.relationship('Items', back_populates='menuitems')




