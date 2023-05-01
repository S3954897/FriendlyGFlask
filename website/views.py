from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import asc
from .models import *

views = Blueprint('views', __name__)


@views.route('/')
def display():
    return render_template("display.html")


@views.route('/home')
@login_required
def home():
    user = current_user
    return render_template("home.html", user=user)


@views.route('/profile')
@login_required
def profile():
    user = current_user
    userShops = Shops.query.filter_by(primaryUserID=user.id).all()
    # Query displays linked to user's shops
    displays = Displays.query.filter(Displays.shopID.in_([shop.shopID for shop in userShops])).all()
    return render_template("profile.html", user=user, userShops=userShops, displays=displays)


@views.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    user = current_user
    if request.method == 'POST':
        user.firstName = request.form.get('newFirstName')
        user.lastName = request.form.get('newLastName')
        user.email = request.form.get('newEmail')
        user.phone = request.form.get('newPhone')
        db.session.commit()
        return redirect(url_for('views.profile'))
    return render_template("profile_edit.html", user=user)


# The flag for an admin user has to be set manually in the db
@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    user = current_user
    return render_template("admin.html", user=user)


@views.route('/adminUsers', methods=['GET', 'POST'])
@login_required
def adminUsers():
    user = current_user
    users = Users.query.all()  # retrieve all user data from the database
    return render_template('adminUsers.html', users=users, user=user)


@views.route('/adminShops', methods=['GET', 'POST'])
@login_required
def adminShops():
    user = current_user
    shops = Shops.query.all()  # retrieve all user data from the database
    users = Users.query.all()  # retrieve all user data from the database
    return render_template('adminShops.html', shops=shops, user=user, users=users)


@views.route('/adminShopView')
@login_required
def adminShopView():
    user = current_user
    shops = Shops.query.all()  # retrieve all user data from the database
    return render_template('adminShopView.html', shops=shops, user=user)


@views.route('/adminShopEdit/<int:shop_id>', methods=['GET', 'POST'])
@login_required
def adminShopEdit(shop_id):
    shopID = shop_id
    user = current_user
    users = Users.query.all()
    shop = Shops.query.get(shopID)

    if request.method == 'POST':
        shop.shopName = request.form.get('newShopName')
        shop.shopAddress = request.form.get('newShopAddress')
        shop.primaryUserID = request.form.get('newPrimaryUserID')
        db.session.commit()
        return redirect(url_for('views.adminShops'))
    return render_template("adminShopEdit.html", user=user, shop=shop, users=users)


@views.route('/adminShopsAddNew', methods=['GET', 'POST'])
@login_required
def adminShopsAddNew():
    user = current_user
    users = Users.query.all()  # retrieve all user data from the database
    if request.method == 'POST':
        newShopName = request.form.get('newShopName')
        newShopAddress = request.form.get('newShopAddress')
        primaryUserID = request.form.get('primaryUserID')
        shopNameCheck = Shops.query.filter_by(shopName=newShopName).first()
        shopAddressCheck = Shops.query.filter_by(shopAddress=newShopAddress).first()
        if shopNameCheck and shopAddressCheck:
            flash('shop already exists.', category='error')
        elif shopAddressCheck:
            flash('shop address already exists.', category='error')
        else:
            newShop = Shops(shopName=newShopName, shopAddress=newShopAddress, primaryUserID=primaryUserID)
            db.session.add(newShop)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.adminShops'))
    return render_template("adminShopsAddNew.html", user=user, users=users)


@views.route('/items')
@login_required
def items():
    user = current_user
    items = Items.query.filter_by(primaryUserID=user.id).order_by(asc(Items.itemName)).all()
    return render_template("Items.html", user=user, items=items)


@views.route('/itemAddNew', methods=['GET', 'POST'])
@login_required
def itemAddNew():
    user = current_user
    items = Items.query.all()
    if request.method == 'POST':
        newItemName = request.form.get('newItemName')
        newItemPrice = request.form.get('newItemPrice')
        itemNameCheck = Items.query.filter_by(itemName=newItemName, primaryUserID=user.id).first()
        if itemNameCheck:
            flash('item name already exists.', category='error')
        elif newItemName == "":
            flash('no new item enetered', category='error')
            return redirect(url_for('views.items'))
        else:
            newItem = Items(itemName=newItemName, itemPrice=newItemPrice, primaryUserID=user.id)
            db.session.add(newItem)
            db.session.commit()
            return redirect(url_for('views.items'))
    return render_template("itemAddNew.html", user=user, items=items)


@views.route('/itemEdit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def itemEdit(item_id):
    itemID = item_id
    user = current_user
    items = Items.query.all()
    item = Items.query.get(itemID)
    if request.method == 'POST':
        item.itemName = request.form.get('newItemName')
        item.itemPrice = request.form.get('newItemPrice')
        db.session.commit()
        return redirect(url_for('views.items'))
    return render_template("itemEdit.html", user=user, items=items, item=item)


# delete an item from the items list by first removing the item from all of its associated menus
# and then deleting it from the items table
@views.route('/itemDelete/<int:item_id>', methods=['POST'])
@login_required
def itemDelete(item_id):
    itemID = item_id
    item = Items.query.get(itemID)
    nullMenuItems = MenuItems.query.filter_by(itemID=itemID).all()
    if item:
        for nullMenuItem in nullMenuItems:
            if nullMenuItem:
                db.session.delete(nullMenuItem)
                db.session.commit()
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('views.items'))


@views.route('/update_item_order', methods=['POST'])
@login_required
def update_item_order():
    item_order_data = request.json
    for item_data in item_order_data:
        menu_item = MenuItems.query.get(item_data['menuItemID'])
        menu_item.itemOrder = item_data['itemOrder']
    db.session.commit()
    return {"status": "success"}


@views.route('/setup', methods=['GET', 'POST'])
@login_required
def setup():
    if request.method == 'POST':
        item1 = request.form.get('item1')
        if item1:
            pass
    return render_template("setup.html")
