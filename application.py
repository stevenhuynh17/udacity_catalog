#!/usr/bin/env python

from flask import Flask, flash, render_template, request, redirect, \
    url_for, jsonify
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Brand, Model, User

# Importing libraries to support oauth system
from flask import session as login_session
from flask import make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Car Catalog Application"

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DB = sessionmaker(bind=engine)
session = DB()

# Login system
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Third party OAuth sign in via Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    if getUserID(login_session['email']) is None:
        print "User currently doesn't exist: creating a new one..."
        createUser(login_session)
    else:
        print "User already exists, restablishing connection..."

    return render_template('login_success.html', info=login_session)

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print "Access Token is None"
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    login_session.clear()

    brand = session.query(Brand).all()
    models = session.query(Model).order_by(Model.id.desc())
    flash("Successfully logged out!")
    return render_template('publicHome.html', brands=brand, models=models)

def login_required(f):
    @wraps(f)
    def checkLogin():
        brand = session.query(Brand).all()
        models = session.query(Model).order_by(Model.id.desc())
        if 'username' in login_session:
            return render_template(
                'publicHome.html', brands=brand, models=models)
    return checkLogin

@app.route('/')
@login_required
def main():
    brand = session.query(Brand).all()
    models = session.query(Model).order_by(Model.id.desc())
    if 'username' not in login_session:
        return render_template(
            'publicHome.html', brands=brand, models=models)
    else:
        user = getUserInfo(getUserID(login_session['email']))
        return render_template(
            'home.html', brands=brand, models=models, user=user)


@app.route('/new', methods=['GET', 'POST'])
def newModel():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # brand = session.query(Brand).filter_by(name=request.form['name']).one()
        try:
            print "IN TRY BLOCK"
            brandname = session.query(Brand).\
                filter_by(name=request.form['brand']).one()
            print "Brandname already exists"
            newModel = Model(
                name=request.form['name'],
                description=request.form['description'],
                price=request.form['price'],
                category=request.form['category'],
                brand=brandname,
                user_id=getUserID(login_session['email'])
            )
            session.add(newModel)
            session.commit()

            return redirect(url_for("listModels", brand_id=brandname.id))

        except:
            print "IN EXCEPTION BLOCK"
            newBrand = Brand(
                name=request.form['brand'],
                user_id=getUserID(login_session['email'])
            )
            session.add(newBrand)
            session.commit()

            print "NEW BRAND!"
            print newBrand.name

            newModel = Model(
                name=request.form['name'],
                description=request.form['description'],
                price=request.form['price'],
                category=request.form['category'],
                brand=session.query(Brand).filter_by(name=newBrand.name).one(),
                user_id=getUserID(login_session['email'])
            )
            session.add(newModel)
            session.commit()

            return redirect(url_for("listModels", brand_id=newBrand.id))

    return render_template(
        'newModel.html'
    )


@app.route('/<int:brand_id>/models')
def listModels(brand_id):
    carMakers = session.query(Brand).all()
    selectedBrand = session.query(Brand).filter_by(id=brand_id).one()
    models = session.query(Model).filter_by(model_id=brand_id).all()
    if 'username' not in login_session:
        return render_template(
            'publicModels.html',
            brands=carMakers,
            models=models,
            brand=selectedBrand
        )
    elif getUserID(login_session['email']) is not selectedBrand.user.id:
        user = getUserInfo(getUserID(login_session['email']))
        return render_template(
            'models.html',
            brands=carMakers,
            models=models,
            brand=selectedBrand,
            user=user
        )
    else:
        user = getUserInfo(getUserID(login_session['email']))
        return render_template(
            'models_personal.html',
            brands=carMakers,
            models=models,
            brand=selectedBrand,
            user=user
        )



@app.route('/models/<int:model_id>')
def modelInfo(model_id):
    data = session.query(Model).filter_by(id=model_id).one()

    if 'username' not in login_session:
        return render_template(
            'publicModelInfo.html', info=data
        )
    elif getUserID(login_session['email']) is not data.user.id:
        user = getUserInfo(getUserID(login_session['email']))
        return render_template(
            'modelInfo.html', info=data, user=user
        )
    else:
        user = getUserInfo(getUserID(login_session['email']))
        return render_template(
            'modelInfo_personal.html', info=data, user=user
        )


@app.route('/models/<int:model_id>/edit', methods=['GET', 'POST'])
def editModel(model_id):
    data = session.query(Model).filter_by(id=model_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    elif getUserID(login_session['email']) is not data.user.id:
        return render_template(
            'publicModelInfo.html', info=data
        )
    modified = session.query(Model).filter_by(id=model_id).one()
    if request.method == 'POST':
        if request.form['name']:
            modified.name = request.form['name']
            session.add(modified)
            session.commit()
        elif request.form['description']:
            modified.description = request.form['description']
            session.add(modified)
            session.commit()
        elif request.form['price']:
            modified.price = request.form['price']
            session.add(modified)
            session.commit()
        elif request.form['category']:
            modified.category = request.form['category']
        return redirect(url_for('modelInfo', model_id=model_id))
    else:
        return render_template(
            'editModel.html', model_id=model_id, car=modified
        )


@app.route('/models/<int:model_id>/delete', methods=['GET', 'POST'])
def deleteModel(model_id):
    toDelete = session.query(Model).filter_by(id=model_id).one()
    print "USER ID!!!"
    print toDelete.user.id
    print "INFORMATION!!!"
    print getUserID(login_session['email'])

    if 'username' not in login_session:
        return redirect('/login')
    elif getUserID(login_session['email']) is not toDelete.user.id:
        return redirect('/')
    else:
        if request.method == 'POST':
            session.delete(toDelete)
            session.commit()
            return redirect(url_for('listModels', brand_id=model_id))
        else:
            return render_template(
                "deleteModel.html", model_id=model_id, item=toDelete
            )


@app.route('/brand/<int:brand_id>/delete', methods=['GET', 'POST'])
def deleteBrand(brand_id):
    data = session.query(Brand).filter_by(id=brand_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    elif getUserID(login_session['email']) is not data.user.id:
        return redirect('/')
    deleteBrand = session.query(Brand).filter_by(id=brand_id).one()

    if request.method == 'POST':
        session.delete(deleteBrand)
        session.query(Model).filter_by(model_id=brand_id).delete()
        session.commit()
        return redirect(url_for('main'))
    else:
        return render_template(
            "deleteBrand.html", brand_id=brand_id, item=deleteBrand
        )


@app.route('/JSON')
def dataJSON():
    models = session.query(Model).all()
    return jsonify(Catalog=[i.serialize for i in models])


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    print "User " + newUser.name + " successfully created!"

# Function to get general user infomration
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Function to retrieve user ID via email
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
