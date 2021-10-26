from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/login')          
def login():
    return render_template('login.html') 

@app.route('/login_process', methods=['POST'])
def login_process():

    data = { "email" : request.form["email"] }
    user = User.get_by_email(data)

    if not user:
        flash("Invalid Email/Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')

    session['user_id'] = user.id       
    return redirect('/')


@app.route('/register')
def register():
    return render_template('register.html') 

@app.route('/register_process', methods = ['POST'])
def register_process():
    print(request.form)

    data = {
        "fname" : request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "confirm-password" : request.form["confirm-password"],
        "address" : request.form['address'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "zip" : request.form['zip']        
    }

    if not User.validate_email_and_password(data): 
        return redirect('/register')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "fname" : request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"],
        "password" : pw_hash,
        "address" : request.form['address'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "zip" : request.form['zip']   
    }

    user_id = User.save(data)

    session['user_id'] = user_id

    return redirect('/')

@app.route('/edit_account_process', methods = ['POST'])
def edit_account_process():
    print(request.form)

    data = {
        "fname" : request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"],
        "prev_email" : request.form["prev_email"],
        "password" : request.form["password"],
        "confirm-password" : request.form["confirm-password"],
        "address" : request.form['address'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "zip" : request.form['zip']        
    }

    if not User.validate_and_update(data): 
        return redirect('/edit_account')

    print("clear ") 
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data2 = {
        "id" : session['user_id'],
        "fname" : request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"],
        "password" : pw_hash,
        "address" : request.form['address'],
        "city" : request.form['city'],
        "state" : request.form['state'],
        "zip" : request.form['zip']   
    }

    User.update(data2)

    return redirect('/edit_account')

@app.route('/delete_account/<int:id>')
def delete_user(id):
    data = {
        "id" : id
    }

    User.delete(data)
    session.clear()

    return redirect('/')


