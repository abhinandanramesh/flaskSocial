from functools import wraps
from flask import flash, redirect, render_template,request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from app.models import User,Message
from app import db,bcrypt
import os

message_blueprint = Blueprint('messages',__name__)

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

@message_blueprint.route('/send_message/<int:user_id>/',methods=['GET','POST'])
@login_required
def send_message(user_id):
	if request.method == 'POST':
		if user_id != session['user_id']:
			print request.form 
			message = Message(
				user_to = User.query.get(user_id).id,
				user_from = User.query.get(session['user_id']).id,
				content = request.form['message']
				)
			db.session.add(message)
			db.session.commit()
			flash('Message sent')
			return redirect(url_for('users.profile',user_id=user_id))
		else:
			flash('Can\'t send a message to yourself')
			return redirect(url_for('users.profile',user_id=user_id))

	
@message_blueprint.route('/user/messages/')
@login_required
def messages():
	messages = Message.query.filter_by(user_to=session['user_id'])
	for message in messages:
		print message.content
		print message.id
	return render_template('messages.html',messages=messages)

@message_blueprint.route('/messages/<int:message_id>/')
@login_required
def read_message(message_id):
	message = Message.query.get(message_id)
	if session['user_id'] == message.user_to:
		user_from = User.query.get(message.user_from)
		message.read = True
		return render_template('message.html',message=message,user_from=user_from)
	else:
		flash("You do not have permiession for that")
		return redirect(url_for('messages.messages'))

@message_blueprint.route('/messages/<int:message_id>/delete/')
@login_required
def delte_message(message_id):
	message = Message.query.get(message_id)
	if session['user_id'] == message.user_to:
		db.session.delete(message)
		db.session.commit()
		flash('Message deleted')
		return redirect(url_for('messages.messages'))
	elif session['user_id'] != message.user_to:
		flash("You do not have permiession for that")
		return redirect(url_for('messages.messages'))


	