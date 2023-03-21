from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
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
            #if statement required as there is a change in format of the time from read to write.
            #the if statement handles both cases.
            if len(newMenuStartTime_alt) > 5:
                shopMenu.menuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M:%S').time()
            else:
                shopMenu.menuStartTime = datetime.strptime(newMenuStartTime_alt, '%H:%M').time()

            newMenuFinishTime_alt = request.form.get('newMenuFinishTime')
            #if statement required as there is a change in format of the time from read to write.
            #the if statement handles both cases.
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

    return render_template("menuSetupEdit.html",
                           user=user,
                           shopMenus=shopMenus,
                           shopMenu=shopMenu,
                           newMenuActive_alt=newMenuActive_alt,
                           menuItems=menuItems,
                           items=items)


#The GET request aquires the display_id number given to each compute stick.
#The display_id aligns to the set menu options available for the display_id set by the user.
@displays.route('/display/<int:display_id>', methods=['GET', 'POST'])
def display(display_id):
    displayID = display_id
    #grabs all the menus for the display_id
    shopMenus = ShopMenus.query.filter_by(displayID=displayID).all()
    menuID = 1
    shopMenuTitle = "Default"

    for shopMenu in shopMenus:
        #filters the menus by active and time and sends the items in that menu to the display.
        if shopMenu.menuStartTime <= datetime.now().time() < shopMenu.menuFinishTime:
            menuID = shopMenu.shopMenuID
            shopMenuTitle = shopMenu.menuTitle
    menuItems = MenuItems.query.filter_by(menuID=menuID).all()
    return render_template('display.html',
                           shopMenus=shopMenus,
                           menuItems=menuItems,
                           shopMenuTitle=shopMenuTitle)


# def linkItemName(itemID):
#     itemName = Items.query.filter_by(itemID=itemID)
#     itemPrice = Items.query.filter_by(itemID=itemID)
#     return (itemName, itemPrice)
