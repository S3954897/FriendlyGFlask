from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import asc
from .models import *
from datetime import datetime


displays = Blueprint('displays', __name__)


@displays.route('/adminDisplays', methods=['GET', 'POST'])
@login_required
def adminDisplays():
    user = current_user
    # retrieve all user data from the database
    displays = Displays.query.all()
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


@displays.route('/adminDisplayEdit/<int:display_id>', methods=['GET', 'POST'])
@login_required
def adminDisplayEdit(display_id):
    displayID = display_id
    user = current_user
    # grabs the selected display using the displayID and loads it into "display"
    display = Displays.query.filter_by(displayID=displayID).first()
    # grabs all the shops in the database for the admin user to select and tie to a shop
    shops = Shops.query.all()
    if request.method == 'POST':
        display.shopID = request.form.get('newShopID')
        db.session.commit()
        return redirect(url_for('displays.adminDisplays'))
    # Need to check the return data to confirm all is being utilised
    return render_template("adminDisplayEdit.html",
                           user=user, displays=displays,
                           displayID=displayID,
                           shops=shops)


@displays.route('/menuSetup/<int:display_id>', methods=['GET', 'POST'])
@login_required
def menuSetup(display_id):
    displayID = display_id
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
    displayID = display_id
    user = current_user
    # display ref
    shopMenus = ShopMenus.query.filter_by(displayID=displayID).all()
    if request.method == 'POST':
        newMenuTitle = request.form.get('newMenuTitle')
        newMenuTypeID = request.form.get('newMenuTypeID')
        newMenuStartTime_alt = request.form.get('newMenuStartTime')
        newMenuFinishTime_alt = request.form.get('newMenuFinishTime')
        newMenuActive = request.form.get('newMenuActive')
        newMenuActive = True if newMenuActive == 'on' else False

        # "if" statement required as there is a change in format of the time from read to write.
        # the if statement handles both cases (The problem lays with the format sometime needing
        # and other times not. I tried a number of more succinct methods but with no success.
        # This may be worth upgrading in the future, but now if a functional alternative.)
        if len(newMenuStartTime_alt) > 5:
            newMenuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M:%S').time()
        else:
            newMenuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M').time()

        if len(newMenuFinishTime_alt) > 5:
            newMenuFinishTime = datetime.strptime(newMenuFinishTime_alt, '%H:%M:%S').time()
        else:
            newMenuFinishTime = datetime.strptime(newMenuFinishTime_alt, '%H:%M').time()

        newMenuSetup = ShopMenus(menuTitle=newMenuTitle,
                                 # This is the selection between Ads and various menu layouts
                                 menuTypeID=newMenuTypeID,
                                 menuStartTime=newMenuStartTime,
                                 menuFinishTime=newMenuFinishTime,
                                 menuActive=newMenuActive,
                                 displayID=displayID)
        db.session.add(newMenuSetup)
        db.session.commit()
        shopMenu_id = newMenuSetup.shopMenuID
        return redirect(url_for('displays.menuSetupEdit', shopMenu_id=shopMenu_id))

    return render_template("menuSetupAddNew.html",
                           user=user,
                           displayID=displayID,
                           shopMenus=shopMenus)


@displays.route('/menuSetupEdit/<int:shopMenu_id>', methods=['GET', 'POST'])
@login_required
def menuSetupEdit(shopMenu_id):
    shopMenuID = shopMenu_id
    user = current_user
    # Items menu
    items = Items.query.filter_by(primaryUserID=user.id).all()
    menuItems = MenuItems.query.filter_by(menuID=shopMenuID).order_by(asc(MenuItems.itemOrder)).all()

    # Shops ads campaign
    ads = Advertisements.query.filter_by(primaryUserID=user.id).all()
    menuAds = ShopAds.query.filter_by(menuID=shopMenuID).order_by(asc(ShopAds.adOrder)).all()

    shopMenus = ShopMenus.query.all()
    shopMenu = ShopMenus.query.get(shopMenuID)
    newMenuActive_alt = 'on' if shopMenu.menuActive else 'off'

    # Need a match-case (python switch-case equivalent) to be able to move to the correct ads layout
    # 1 Ads Landscape
    # 2 Ads Portrait (Not yet used)
    # 3 Menu Style 1
    # 4 Menu Style 2 (Not yet used) ... etc.
    # This option allows for the easy addition of additional screen options in the future
    match shopMenu.menuTypeID:
        case 1:
            # ads Landscape
            if request.method == 'POST':
                form_type = request.form.get('form_type')
                if form_type == 'menu_setup_edit':
                    shopMenu.menuTitle = request.form.get('newMenuTitle')
                    # This may need to be removed as this method is now dealing with Ads display as well as items menu
                    shopMenu.menuType = request.form.get('newMenuType')

                    newMenuStartTime_alt = request.form.get('newMenuStartTime')
                    # if statement required as there is a change in format of the time from read to write.
                    # the if statement handles both cases.
                    if len(newMenuStartTime_alt) > 5:
                        shopMenu.menuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M:%S').time()
                    else:
                        shopMenu.menuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M').time()

                    newMenuFinishTime_alt = request.form.get('newMenuFinishTime')

                    # if statement required as there is a change in format of the time from read to write.
                    # the if statement handles both cases.
                    if len(newMenuFinishTime_alt) > 5:
                        shopMenu.menuFinishTime = datetime.strptime(newMenuFinishTime_alt, '%H:%M:%S').time()
                    else:
                        shopMenu.menuFinishTime = datetime.strptime(newMenuFinishTime_alt, '%H:%M').time()

                    newMenuActive_alt = request.form.get('newMenuActive_alt')
                    shopMenu.menuActive = True if newMenuActive_alt == 'on' else False

                    db.session.commit()
                    return redirect(url_for('displays.menuSetup',
                                            display_id=shopMenu.displayID))

                elif form_type == 'add_menu_ads':
                    adIDs = request.form.getlist('ad')

                    # This is to establish the order of ads within the user constructed menu
                    for i, adID in enumerate(adIDs, 1):
                        print(i)
                        ad = ShopAds(menuID=shopMenuID,
                                    adID=adID,
                                    adOrder=i)
                        db.session.add(ad)
                    db.session.commit()
                    return redirect(url_for('displays.menuSetupEdit',
                                            shopMenu_id=shopMenuID))

            return render_template("menuSetupEdit1.html",
                                   user=user,
                                   shopMenus=shopMenus,
                                   shopMenu=shopMenu,
                                   newMenuActive_alt=newMenuActive_alt,
                                   menuItems=menuItems,
                                   menuAds=menuAds,
                                   items=items,
                                   ads=ads)
        case 2:
            # ads Portrait
            pass
        case 3:
            # Menu Style 1

            if request.method == 'POST':
                form_type = request.form.get('form_type')
                if form_type == 'menu_setup_edit':
                    shopMenu.menuTitle = request.form.get('newMenuTitle')
                    shopMenu.menuType = request.form.get('newMenuType')
                    newMenuStartTime_alt = request.form.get('newMenuStartTime')

                    # if statement required as there is a change in format of the time from read to write.
                    # the if statement handles both cases.
                    if len(newMenuStartTime_alt) > 5:
                        shopMenu.menuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M:%S').time()
                    else:
                        shopMenu.menuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M').time()

                    newMenuFinishTime_alt = request.form.get('newMenuFinishTime')

                    # if statement required as there is a change in format of the time from read to write.
                    # the if statement handles both cases.
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

                    # request.form.get('groupID')
                    groupID = 1

                    # This is to establish the order of items within the user constructed menu
                    for i, itemID in enumerate(itemIDs, 1):
                        menuItem = MenuItems(menuID=shopMenuID,
                                             itemID=itemID,
                                             groupID=groupID,
                                             itemOrder=i)
                        db.session.add(menuItem)
                    db.session.commit()
                    return redirect(url_for('displays.menuSetupEdit',
                                            shopMenu_id=shopMenuID))

            return render_template("menuSetupEdit3.html",
                                   user=user,
                                   shopMenus=shopMenus,
                                   shopMenu=shopMenu,
                                   newMenuActive_alt=newMenuActive_alt,
                                   menuItems=menuItems,
                                   menuAds=menuAds,
                                   items=items)
        case _:
            pass


@displays.route('/deleteMenuAd', methods=['GET', 'POST'])
@login_required
# used to remove an item from a selected menu without deleting the item from the items list
def deleteMenuAd():
    menuAdID = request.json['menuAdID']
    deleteMenuAd = ShopAds.query.get(menuAdID)
    if deleteMenuAd:
        db.session.delete(deleteMenuAd)
        db.session.commit()
        return jsonify({"status": "success", "message": "Menu item removed successfully"})
    else:
        return jsonify({"status": "error", "message": "Menu item not found"})


@displays.route('/menuItemDelete', methods=['GET', 'POST'])
@login_required
# used to remove an item from a selected menu without deleting the item from the items list
def menuItemDelete():
    menuItemID = request.json['menuItemID']
    deleteMenuItem = MenuItems.query.get(menuItemID)
    if deleteMenuItem:
        db.session.delete(deleteMenuItem)
        db.session.commit()
        return jsonify({"status": "success", "message": "Menu item removed successfully"})
    else:
        return jsonify({"status": "error", "message": "Menu item not found"})


@displays.route('/shopMenuDelete', methods=['GET', 'POST'])
@login_required
# Before deleting the shop menu a check is made to see if there is any items attached.
# If items are attached to the menu they are removed prior to deleting the shop menu.
def shopMenuDelete():
    shopMenuID = request.json['shopMenuID']
    deleteShopMenu = ShopMenus.query.get(shopMenuID)
    shopMenuItems = MenuItems.query.filter_by(menuID=shopMenuID).all()
    if deleteShopMenu:
        if shopMenuItems:
            for shopMenuItem in shopMenuItems:
                db.session.delete(shopMenuItem)
                db.session.commit()
        db.session.delete(deleteShopMenu)
        db.session.commit()
        return jsonify({"status": "success", "message": "Menu item removed successfully"})
    else:
        return jsonify({"status": "error", "message": "Menu item not found"})


# The GET request quires the display_id number given to each compute stick.
# The display_id aligns to the set menu options available for the display_id set by the user.
@displays.route('/display/<int:display_id>', methods=['GET', 'POST'])
def display(display_id):
    displayID = display_id

    # grabs all the active menus for the display_id
    shopMenus = ShopMenus.query.filter_by(displayID=displayID, menuActive=True).all()
    if shopMenus:
        for shopMenu in shopMenus:
            # filters the menus by active and time and sends the items in that menu to the display.
            if shopMenu.menuStartTime <= datetime.now().time() < shopMenu.menuFinishTime:
                menuID = shopMenu.shopMenuID
                shopMenuTitle = shopMenu.menuTitle

                match shopMenu.menuTypeID:
                    case 1:
                        ads = ShopAds.query.filter_by(menuID=menuID).order_by(asc(ShopAds.adOrder)).all()
                        return render_template('display.html',
                                               displayID=displayID,
                                               ads=ads,
                                               shopMenu=shopMenu,
                                               shopMenuTitle=shopMenuTitle)

                    case 3:
                        menuItems = MenuItems.query.filter_by(menuID=menuID).order_by(asc(MenuItems.itemOrder)).all()
                        return render_template('display.html',
                                               displayID=displayID,
                                               shopMenu=shopMenu,
                                               menuItems=menuItems,
                                               shopMenuTitle=shopMenuTitle)

            else:
                return render_template('default.html')
    else:
        return render_template('default.html')
