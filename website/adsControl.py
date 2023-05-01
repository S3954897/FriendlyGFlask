import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from website import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, db
from website.models import Advertisements, ShopAds
from PIL import Image
import secrets
import string


adsControl = Blueprint('adsControl', __name__)


def randomAlphaNumeric(length=10):
    randomName = string.ascii_letters + string.digits
    return ''.join(secrets.choice(randomName) for _ in range(length))


@adsControl.route('/adsMedia')
@login_required
def adsMedia():
    user = current_user
    ads = Advertisements.query.filter_by(primaryUserID=user.id)
    return render_template("adsMedia.html", ads=ads)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@adsControl.route('/upload_ad', methods=['GET', 'POST'])
@login_required
def upload_ad():
    user = current_user
    if 'ad-file' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)

    file = request.files['ad-file']

    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        tempFilename = secure_filename(file.filename)
        # This is to ensure that there cannot be two file names the same.
        # Just incase two users have the same file.
        filename = f'{randomAlphaNumeric(10)}_{tempFilename}'
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Create the thumbnail and save it
        thumbnail_path = os.path.join(UPLOAD_FOLDER, "thumbnails", filename)
        create_thumbnail(file_path, thumbnail_path)

        # Add the file information to the advertisements table
        ad = Advertisements(adName=filename, file_path=file_path, thumbnail_path=thumbnail_path, primaryUserID=user.id)
        db.session.add(ad)
        db.session.commit()

        flash('File uploaded and saved.', category='success')
        return redirect(url_for('adsControl.adsMedia'))
    else:
        flash('File type not allowed.', category='error')
        return redirect(request.url)


def create_thumbnail(image_path, thumbnail_path, size=(200, 200)):
    image = Image.open(image_path)
    image.thumbnail(size)
    image.save(thumbnail_path)


@adsControl.route('/adsDisplay')
def adsDisplay():
    return render_template('adsDisplay.html')


@adsControl.route('/updateAdOrder', methods=['POST'])
@login_required
def update_ad_order():
    # retrieve the new order of ads from the request
    ad_order_data = request.json
    for ad_data in ad_order_data:
        menu_ad = ShopAds.query.get(ad_data['menuAdID'])
        menu_ad.adOrder = ad_data['adOrder']
    db.session.commit()
    return {"status": "success"}
