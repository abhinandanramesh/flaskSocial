from functools import wraps
from flask import flash, redirect, render_template,request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from .forms import RegisterForm,LoginForm
from app.models import User,FriendRequest
from app import db,bcrypt
import os

users_blueprint = Blueprint('users',__name__)

#helper function
def login_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

def are_friends(user1,user2):
    user1 = User.query.get(user1)
    user2 = User.query.get(user2)
    if user1.is_friend(user2):
        return True
    else:
        return False

@users_blueprint.route('/register/',methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        new_user = User(
            user_name = form.user_name.data,
            email = form.email.data,
            password = bcrypt.generate_password_hash(form.password.data)
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering!')
        except IntegrityError:
            error = "That username and/or email alread exists."
            return render_template('register.html',form=form,error=error)
    return render_template('register.html',form=form)

@users_blueprint.route('/login/',methods=['GET','POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=request.form['email']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                flash('Welcome!')
                flash("Succesfful Logged in")
                return redirect(url_for('users.my_profile'))
            else:
                error = 'Invlaid username or password'
    return render_template('login.html',form=form,error=error)

@users_blueprint.route('/logout/',methods=['GET','POST'])
def logout():
    session.pop('logged_in',None)
    session.pop('user_id',None)
    flash('Goodbye!')
    return redirect(url_for('users.login'))

@users_blueprint.route('/user/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    user_profile = user.id == session['user_id']
    if request.method == 'POST':
        print request.form 
        message = Message(
            user_to = User.query.get(user_id),
            user_from = User.query.get(session['user_id']),
            content = request.form['message']
            )
        db.session.add(message)
        db.session.commit()
    return render_template('user.html',user=user,user_profile=user_profile)


@users_blueprint.route('/user/<int:user_id>/add_friend/')
@login_required
def add_friend(user_id):
    check = FriendRequest.query.filter_by(user_sent_from = session['user_id'],user_sent_to = user_id).first()
    friends = are_friends(session['user_id'],user_id)
    if check == None and not friends:
        fq = FriendRequest(
            user_sent_from = session['user_id'],
            user_sent_to = user_id
        )
        db.session.add(fq)
        db.session.commit()
        flash('Friend request sent!')
        return redirect(url_for('users.profile',user_id = user_id))
    else:
        if friends == True:
            flash('Already friends')
        else:
            flash('Request already sent')
        return redirect(url_for('users.profile',user_id = user_id))

@users_blueprint.route('/user/requests/')
@login_required
def requests():
    user_to = User.query.get(session['user_id'])
    reqs = FriendRequest.query.filter_by(id=1).all()
    users_from = []
    for r in reqs:
        user = User.query.get(r.user_sent_from)
        users_from.append(user)
    return render_template('requests.html',users_from=users_from)

@users_blueprint.route('/user/requests/<int:request_id>/accept/')
@login_required
def accept(request_id):
    request = FriendRequest.query.get(request_id)
    if session['user_id'] == request.user_sent_to:
        request.accept()
        flash('Request accepted')
        return redirect(url_for('users.requests'))
    else:
        flash('Not allowed')
        return redirect(url_for('users.requests'))


@users_blueprint.route('/user/requests/<int:request_id>/reject/')
@login_required
def reject(request_id):
    request = FriendRequest.query.get(request_id)
    if session['user_id'] == request.user_sent_to:
        request.reject()
        flash('Request rejected')
        return redirect(url_for('users.requests'))
    else:
        flash('Not allowed')
        return redirect(url_for('users.requests'))

@users_blueprint.route('/user/friends/')
@login_required
def friends():
    user = User.query.get(session['user_id'])
    return render_template('friends.html',user=user)

@users_blueprint.route('/user/friends/<int:user_id>/delete/')
@login_required
def delete_friend(user_id):
    friend = User.query.get(user_id)
    user = User.query.get(session['user_id'])
    if user.is_friend(friend):
        user.delete_friend(friend)
        flash('User removed from friends list')
        return redirect(url_for('my_profile'))
    else:
        return redirect(url_for('my_profile'))

@users_blueprint.route('/user/')
@login_required
def my_profile():
    user = User.query.get(session['user_id'])
    return render_template('user.html',user=user,user_profile = True)


