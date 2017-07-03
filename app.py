from flask import (Flask, render_template, url_for,
                   redirect, request, session)

from activity import Activity
from bucketlist import BucketList
from user import User


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
    ''' logs out user and redirects to login page '''
    session.clear()

    return redirect(url_for('login'))

@app.route('/add_bucketlist', methods=['POST', 'GET'])
def add_bucketlist():
    ''' creates a new bucketlist and adds it to user's bucketlists property '''
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

    return render_template('addlists.html', bucketlists=user.bucketlists)

@app.route('/back_to_bucketlists', methods=['GET'])
def back_to_bucketlists():
    user = None
    username = session['user']['username']

    if username in users.keys():
        user = users[username]

        return render_template('addlists.html', bucketlists=user.bucketlists)

@app.route('/update_bucket', methods=['POST', 'GET'])
def update_bucket():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        user = None
        username = session['user']['username']

        if username in users.keys():
            user = users[username]
            user.bucketlists[name] = BucketList(name, description)

        return render_template('addlists.html', bucketlists=user.bucketlists)

    else:
        return render_template('update_bucketlist.html')

@app.route('/update_bucketlist/<name>/<description>', methods=['POST', 'GET'])
def update_bucketlist(name, description):
    username = session['user']['username']

    user = None

    if username in users.keys():
        user = users[username]
        if name in user.bucketlists.keys():
            del user.bucketlists[name]

    return redirect(url_for('update_bucket', name=name, description=description))

@app.route('/update_activity/<name>/<title>/<description>', methods=['POST', 'GET'])
def update_activity(name, title, description):
    username = session['user']['username']

    user = None

    if username in users.keys():
        user = users[username]
        if name in user.bucketlists.keys():
            for i in range(len(user.bucketlists[name].activities)):
                if user.bucketlists[name].activities[i].title == title:
                    user.bucketlists[name].activities.pop(i)
                    break

    return redirect(url_for('updt_act', name=name, title=title, description=description))

@app.route('/updt_act', methods=['POST', 'GET'])
def updt_act():    
    user = None
    username = session['user']['username']

    if username in users.keys():
        user = users[username]

    current_bucketlist = request.args.get('name')

    if request.method == 'POST':
        current_bucketlist = request.form['name']

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
        return render_template('update_activity.html', name=current_bucketlist)

@app.route('/add_activity', methods=['POST', 'GET'])
def add_activity_to_bucketlist():
    ''' Add activity to named bucketlist '''
    user = None
    username = session['user']['username']

    if username in users.keys():
        user = users[username]

    current_bucketlist = request.args.get('name')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']


        activity = Activity(title, description)

        if current_bucketlist in user.bucketlists.keys():
            user.bucketlists[current_bucketlist].add_activity(activity)

        activities = user.bucketlists[current_bucketlist].activities

        return render_template('bucketlist.html',
                               name=current_bucketlist,
                               activities=activities)
    else:
        return render_template('bucketlist.html', name=current_bucketlist,
                               activities=user.bucketlists[current_bucketlist].activities)

@app.route('/delete_activity/<name>/<title>', methods=['GET'])
def delete_activity(name, title):
    ''' delete an activity given a name '''
    username = session['user']['username']

    user = None

    if username in users.keys():
        user = users[username]

    for i in range(len(user.bucketlists[name].activities)):
        if user.bucketlists[name].activities[i].title == title:
            user.bucketlists[name].activities.pop(i)

            return redirect(url_for('add_activity_to_bucketlist',
                                    name=user.bucketlists[name].name,
                                    activities=user.bucketlists[name].activities))

if __name__ == '__main__':
    app.secret_key = 'xcxcyuxcyuxcyuxcyxuee'

    app.run(debug=True)
