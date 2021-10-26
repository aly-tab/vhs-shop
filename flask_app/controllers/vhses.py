from flask_app import app
from flask import render_template, request, redirect, session, flash 
from flask_app.controllers import users
from flask_app.models.user import User
from flask_app.models.vhs import VHS
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from collections import OrderedDict

movie = False

@app.route('/')
def dashboard():
    
    if 'user_id' not in session:
        user = 0
        session_id = 0
    else:
        data = {
            "id" : session['user_id']
        }

        user = User.get_by_id(data)
        print(user)
    
    if 'user_id' in session:
        session_id = session['user_id']
    else:
        session_id = 0

    vhses = VHS.get_all()
    print(vhses)

    if vhses == False:
        vhses = []

    return render_template('dashboard.html', session_id=session_id, user=user, vhses=vhses)

@app.route('/account')
def account():
    data = {
        "id" : session['user_id']
    }

    user = User.get_by_id(data)
    print(user)

    vhses = User.get_users_vhses(data)
    print(vhses)

    if vhses == False:
        vhses = []

    purchases = User.get_users_purchases(data)
    print(purchases)

    if purchases == False:
        purchases = []

    if 'user_id' in session:
        session_id = session['user_id']
    else:
        session_id = 0

    return render_template('account.html', session_id=session_id , user=user, vhses=vhses, purchases=purchases)

@app.route('/new')
def new():
    data = {
       "id" : session['user_id']
    }

    user = User.get_by_id(data)
    print(user)

    if 'user_id' in session:
        session_id = session['user_id']
    else:
        session_id = 0

    return render_template('new.html', session_id=session_id , user=user)

@app.route('/add', methods=['POST'])
def add():
    print(request.form)

    data = {
        "title" : request.form['title'],
        "price" : request.form['price'],
        "poster_id" : session['user_id'],
        "owner_id" : session['user_id']
    }

    if not VHS.validate_vhs(data):
        return redirect('/new')

    VHS.save(data)

    return redirect('/new')

@app.route('/view/<int:id>')
def view(id):

    data = {
        "id" : id
    }

    vhs = VHS.get_vhs(data)
    print(vhs)

    if 'user_id' in session:
        session_id = session['user_id']
    else:
        session_id = 0

    if vhs.poster_id != vhs.owner_id:
        if vhs.poster_id != session_id:
            if vhs.owner_id != session_id:
                return redirect("/")

    return render_template('view.html', session_id=session_id , vhs=vhs)

@app.route('/edit/<int:id>')
def edit(id):
    data = {
        "id" : id
    }

    vhs = VHS.get_vhs(data)
    print(vhs)

    if 'user_id' in session:
        session_id = session['user_id']
    else:
        session_id = 0

    if session_id != vhs.poster_id:
        return redirect("/")

    return render_template('edit.html', session_id=session_id, vhs=vhs)


@app.route('/edit_process/<int:id>', methods=['POST'])
def edit_process(id):

    data = {
        "id" : id,
        "title" : request.form['title'],
        "price" : request.form['price'],
    }

    if not VHS.validate_vhs(data):
        return redirect(f'/edit/{ id }')

    VHS.update(data)

    return redirect(f'/edit/{ id }')

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        "id" : id
    }

    VHS.delete(data)
    return redirect('/')

@app.route('/delete_on_account/<int:id>')
def delete_on_account(id):
    data = {
        "id" : id
    }

    VHS.delete(data)
    return redirect('/account')

@app.route('/delete_on_posts/<int:id>')
def delete_on_posts(id):
    data = {
        "id" : id
    }

    VHS.delete(data)
    return redirect('/posted_list')

@app.route('/edit_account')
def edit_account():
    data = {
        "id" : session['user_id']
    }

    user = User.get_by_id(data)
    print(user)

    if 'user_id' in session:
        session_id = session['user_id']
    else:
        session_id = 0

    return render_template('/edit-account.html', session_id=session_id, user=user)

@app.route('/buy/<int:id>')
def buy(id):
    data = {
        "id" : id,
        "owner_id" : session['user_id']
    }

    VHS.buy(data)

    return redirect(f'/view/{ id }')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/posted_list')
def posted_list():
    data = {
        "id" : session['user_id']
    }

    user = User.get_by_id(data)
    print(user)

    vhses = User.get_users_vhses(data)
    print(vhses)

    if vhses == False:
        vhses = []

    if 'user_id' in session:
        session_id = session['user_id']
    else:
        session_id = 0

    return render_template('/posts.html', session_id=session_id, vhses=vhses)

@app.route('/purchases_list')
def purchases_list():
    data = {
        "id" : session['user_id']
    }

    user = User.get_by_id(data)
    print(user)

    purchases = User.get_users_purchases(data)
    print(purchases)

    if purchases == False:
        purchases = []

    if 'user_id' in session:
        session_id = session['user_id']
    else:
        session_id = 0

    return render_template('/purchases.html', session_id=session_id, purchases=purchases)
