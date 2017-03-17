# -*- coding: utf-8 -*-
"""Shop section, including search and posting items."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from palette.extensions import login_manager
from palette.public.views import load_user
from palette.public.forms import LoginForm
from palette.shop.forms import ItemForm
from palette.shop.models import Item
from palette.utils import flash_errors

blueprint = Blueprint('shop', __name__, static_folder='../static')


@blueprint.route('/find/')
def find():
    """Find item."""
    form = LoginForm(request.form)
    items = Item.query.filter_by(is_active=True)
    return render_template('shop/find.html', items=items, form=form)  # , str=str())


# @blueprint.route('/user/<username>/item/<item_id>')
@blueprint.route('/item/<item_id>')
def item(item_id):  # user_id,
    """item page."""
    form = LoginForm(request.form)
    item = Item.query.filter_by(id=item_id).first()
    return render_template('shop/item.html', item=item, form=form)


@blueprint.route('/share/', methods=['GET', 'POST'])
@login_required
def share():
    """Register new user."""
    # login_form = LoginForm(request.form)
    form = ItemForm(request.form)  # , meta.csrf=False)
    if form.validate_on_submit():
        user_id = current_user.id
        username = current_user.username
        item = Item.create(name=form.name.data,
                           description=form.description.data,
                           terms=form.terms.data,
                           # active=True,
                           price=form.price.data,
                           user_id=user_id)
        item_id = item.id
        flash('Thank you for sharing.')  #, str(res))
        return redirect(url_for('shop.item', item_id=item_id))  # user_id=user_id,
    else:
        flash_errors(form)
    return render_template('shop/share.html', form=form)
