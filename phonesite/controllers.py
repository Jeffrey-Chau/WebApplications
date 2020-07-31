"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import uuid

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from yatl.helpers import A
from . common import db, session, T, cache, auth, signed_url
from py4web.utils.auth import Auth

#auth = Auth(session, db)
auth.enable()
url_signer = URLSigner(session)

# The auth.user below forces login.
@action('index')
@action.uses('index.html', db, auth.user)
def index():
    rows = db(db.contact.user_email == auth.current_user.get('email')).select()
    phones = db(db.phones.user_email == auth.current_user.get('email')).select()

    return dict(rows=rows, url_signer=url_signer, phones=phones)

@action('add_contact', method=['GET', 'POST'])
@action.uses('add_contact.html', session, db)
def add_contact():
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('index'))
    return dict(form=form)


@action('edit_contact/<contact_id>', method=['GET', 'POST'])
@action.uses('add_contact.html', session, db, auth.user)
def edit_contact(contact_id=None):

    # We read the product.
    p = db.contact[contact_id]
    if p is None or p.user_email != auth.current_user.get('email'):
        # Nothing to edit.  This should happen only if you tamper manually with the URL.
        redirect(URL('index'))
    form = Form(db.contact, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('index'))
    return dict(form=form)


@action('delete_contact/<contact_id>', method=['GET', 'POST'])
@action.uses('add_contact.html', session, db, url_signer.verify())
def delete_contact(contact_id=None):

    if contact_id != None:
        p = db.contact[contact_id]
        p.delete_record()
    redirect(URL('index'))



@action('edit_phones/<contact_id>', method=['GET', 'POST'])
@action.uses('edit_phones.html', db, auth.user)
def edit_phones(contact_id=None):



    rows = db(db.phones.phone_id == contact_id).select()
    p = db.contact[contact_id]

    if p is None or p.user_email != auth.current_user.get('email'):
        # Nothing to edit.  This should happen only if you tamper manually with the URL.
        redirect(URL('index'))


    return dict(rows=rows, url_signer=url_signer, p=p, contact_id=contact_id)



@action('add_phone/<contact_id>', method=['GET', 'POST'])
@action.uses('add_phone.html', session, db)
def add_phone(contact_id=None):

    db.phones.phone_id.default = contact_id
    form = Form(db.phones, csrf_session=session, formstyle=FormStyleBulma)

    p = db.contact[contact_id]
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('edit_phones', contact_id))
    return dict(form=form, p=p, contact_id=contact_id)


@action('edit_phone/<contact_id>/<phone_id>', method=['GET', 'POST'])
@action.uses('add_phone.html', session, db, auth.user)
def edit_phone(contact_id=None, phone_id=None):

    # We read the product.
    p = db.phones[phone_id]
    c = db.contact[contact_id]
    if p is None or p.user_email != auth.current_user.get('email'):
        # Nothing to edit.  This should happen only if you tamper manually with the URL.
        redirect(URL('edit_phones', contact_id))
    form = Form(db.phones, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We always want POST requests to be redirected as GETs.
        redirect(URL('edit_phones', contact_id))
    return dict(form=form, p=c)


@action('delete_phone/<contact_id>/<phone_id>', method=['GET', 'POST'])
@action.uses(session, db, url_signer.verify(), auth.user)
def delete_phone(contact_id=None, phone_id=None):

    if contact_id != None and phone_id != None:
        p = db.phones[phone_id]
        #making sure only auth user is deleting entry
        if p.user_email == auth.current_user.get('email'):
            p.delete_record()

    redirect(URL('edit_phones', contact_id))

































