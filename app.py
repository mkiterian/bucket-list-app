from user import User
from bucketlist import BucketList

from activity import Activity

from flask import (Flask, render_template, url_for, 
        redirect, request, jsonify, session, flash)

users = {}

app = Flask(__name__)

current_bucketlist = None

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    ''' logs in a registered user '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = None

        if username in users.keys():
            user = users[username]
            if password == user.password:
                session['user'] = {'username':user.username, 'email':user.email}

                return render_template('addlists.html', bucketlists=user.bucketlists)
            else:
                return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ''' registers a new user if the signup form is posted '''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            user = User(username, email, password)
            users[username] = user

            session['user'] = {'username': username, 'email': email}

            return redirect(url_for('add_bucketlist', user=session['user']['username']))

        else:
            return redirect(url_for('signup'))
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('login'))

@app.route('/add_bucketlist', methods=['POST', 'GET'])
def add_bucketlist():
    ''' creates a new bucketlist and adds it to user's bucketlists property'''
    if request.method == 'POST':
        name = request.form['title']
        description = request.form['description']
        user = None
        username = session['user']['username']

        if username in users.keys():
            user = users[username]
            user.bucketlists[name] = BucketList(name, description)

        return render_template('addlists.html', bucketlists=user.bucketlists)
    else:
        username = session['user']['username']
        return render_template('addlists.html', username=username)

@app.route('/delete_bucketlist/<name>', methods=['GET'])
def delete_bucketlist(name):
    ''' delete bucketlist given a name '''
    username = session['user']['username']

    user = None

    if username in users.keys():
        user = users[username]
        if name in user.bucketlists.keys():
            del user.bucketlists[name]
    
    return render_template('addlists.html', bucketlists = user.bucketlists)

@app.route('/add_activity', methods=['POST', 'GET'])
def add_activity_to_bucketlist():
    user = None
    username = session['user']['username']

    if username in users.keys():
            user = users[username]

    current_bucketlist = request.args.get('bucketlist')


    if request.method == 'POST':       
        title = request.form['title']        
        description = request.form['description']
                
        activity = Activity(title, description)

        if current_bucketlist in user.bucketlists.keys():
            user.bucketlists[current_bucketlist].add_activity(activity)

        activities = user.bucketlists[current_bucketlist].activities

        return render_template('bucketlist.html',
                               bucketlist=current_bucketlist,
                               activities=activities)
    else:
        return render_template('bucketlist.html', bucketlist=current_bucketlist,
                               activities=user.bucketlists[current_bucketlist].activities)


@app.route('/update_activity')
def update_activity():
    pass

if __name__ == '__main__':
    app.secret_key = 'xcxcyuxcyuxcyuxcyxuee'

    app.run(debug=True)