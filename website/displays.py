from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import *
from datetime import datetime, time


displays = Blueprint('displays', __name__)


@displays.route('/adminDisplays', methods=['GET', 'POST'])
@login_required
def adminDisplays():
    user = current_user
    displays = Displays.query.all()  # retrieve all user data from the database
    return render_template('adminDisplays.html',
                           displays=displays,
                           user=user)


@displays.route('/adminDisplaysAddNew', methods=['GET', 'POST'])
@login_required
def adminDisplaysAddNew():
    user = current_user
    shops = Shops.query.all()
    if request.method == 'POST':
        newDisplayID = request.form.get('newDisplayID')
        newShopID = request.form.get('newShopID')
        displayIDCheck = Displays.query.filter_by(displayID=newDisplayID).first()
        if displayIDCheck:
            flash('shop already exists.', category='error')
        else:
            newDisplay = Displays(displayID=newDisplayID, shopID=newShopID)
            db.session.add(newDisplay)
            db.session.commit()
            return redirect(url_for('displays.adminDisplays'))
    return render_template('adminDisplaysAddNew.html',
                           displays=displays,
                           user=user,
                           shops=shops)


@displays.route('/menuSetup/<int:display_id>', methods=['GET', 'POST'])
@login_required
def menuSetup(display_id):
    displayID=display_id
    user = current_user
    display = Displays.query.get(displayID)
    shopMenus = ShopMenus.query.filter_by(displayID=displayID).all()

    return render_template('menuSetup.html',
                           displays=displays,
                           user=user,
                           display=display,
                           shopMenus=shopMenus)

@displays.route('/menuSetupAddNew/<int:display_id>', methods=['GET', 'POST'])
@login_required
def menuSetupAddNew(display_id):
    displayID=display_id
    user = current_user
    shopMenus = ShopMenus.query.filter_by(displayID=displayID).all()
    if request.method == 'POST':
        newMenuTitle = request.form.get('newMenuTitle')
        newMenuTypeID = request.form.get('newMenuTypeID')
        newMenuStartTime_alt = request.form.get('newMenuStartTime')
        newMenuFinishTime_alt = request.form.get('newMenuFinishTime')
        newMenuActive = request.form.get('newMenuActive')
        newMenuActive = True if newMenuActive == 'on' else False

        if len(newMenuStartTime_alt) > 5:
            newMenuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M:%S').time()
        else:
            newMenuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M').time()
        if len(newMenuFinishTime_alt) > 5:
            newMenuFinishTime = datetime.strptime(newMenuFinishTime_alt, '%H:%M:%S').time()
        else:
            newMenuFinishTime = datetime.strptime(newMenuFinishTime_alt, '%H:%M').time()

        # newMenuStartTime = datetime.strptime(newMenuStartTime_str, '%H:%M').time()
        # newMenuFinishTime = datetime.strptime(newMenuFinishTime_str, '%H:%M').time()

        newMenuSetup = ShopMenus(menuTitle=newMenuTitle,
                                 menuTypeID=newMenuTypeID,
                                 menuStartTime=newMenuStartTime,
                                 menuFinishTime=newMenuFinishTime,
                                 menuActive=newMenuActive,
                                 displayID=displayID)
        db.session.add(newMenuSetup)
        db.session.commit()
        return redirect(url_for('displays.menuSetup', display_id=displayID))

    return render_template("menuSetupAddNew.html",
                           user=user,
                           displayID=displayID,
                           shopMenus=shopMenus)

@displays.route('/menuSetupEdit/<int:shopMenu_id>', methods=['GET', 'POST'])
@login_required
def menuSetupEdit(shopMenu_id):

    shopMenuID = shopMenu_id
    user = current_user
    items = Items.query.filter_by(primaryUserID=user.id).all()
    menuItems = MenuItems.query.filter_by(menuID=shopMenuID)
    shopMenus = ShopMenus.query.all()
    shopMenu = ShopMenus.query.get(shopMenuID)
    newMenuActive_alt = 'on' if shopMenu.menuActive else 'off'


    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'menu_setup_edit':
            shopMenu.menuTitle = request.form.get('newMenuTitle')
            shopMenu.menuType = request.form.get('newMenuType')

            newMenuStartTime_alt = request.form.get('newMenuStartTime')
            if len(newMenuStartTime_alt) > 5:
                shopMenu.menuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M:%S').time()
            else:
                shopMenu.menuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M').time()
            newMenuFinishTime_alt = request.form.get('newMenuFinishTime')
            if len(newMenuFinishTime_alt) > 5:
                shopMenu.menuFinishTime = datetime.strptime(newMenuFinishTime_alt, '%H:%M:%S').time()
            else:
                shopMenu.menuFinishTime = datetime.strptime(newMenuFinishTime_alt, '%H:%M').time()

            newMenuActive_alt = request.form.get('newMenuActive_alt')
            shopMenu.menuActive = True if newMenuActive_alt == 'on' else False

            db.session.commit()
            return redirect(url_for('displays.menuSetup',
                                    display_id=shopMenu.displayID))

        elif form_type == 'add_menu_item':
            itemIDs = request.form.getlist('item')
            groupID = 1 # request.form.get('groupID')
            for i, itemID in enumerate(itemIDs, 1):
                menuItem = MenuItems(menuID=shopMenuID,
                                     itemID=itemID,
                                     groupID=groupID,
                                     itemOrder=i)
                db.session.add(menuItem)
            db.session.commit()
            return redirect(url_for('displays.menuSetupEdit',
                                    shopMenu_id=shopMenuID))

    return render_template("menuSetupEdit.html",
                           user=user,
                           shopMenus=shopMenus,
                           shopMenu=shopMenu,
                           newMenuActive_alt=newMenuActive_alt,
                           menuItems=menuItems,
                           items=items)


@displays.route('/D0573')
def D0573():
    displayID = int('0573')
    menuID = 1
    shopMenus = ShopMenus.query.filter_by(displayID=displayID).first()
    menuItems = MenuItems.query.filter_by(menuID=menuID).all()

    return render_template('D0573.html',
                           shopMenus=shopMenus,
                           menuItems=menuItems)


def linkItemName(itemID):
    itemName = Items.query.filter_by(itemID=itemID)
    itemPrice = Items.query.filter_by(itemID=itemID)
    return (itemName, itemPrice)
