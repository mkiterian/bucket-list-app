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



@app.route('/save', methods=['POST', 'GET'])
def save():
    if request.method == 'POST':
        return redirect(url_for('manage'))

    else:
        return render_template('managelists.html')

@app.route('/manage', methods=['POST', 'GET'])
def manage():

    if request.method == 'POST':
        name = request.form['title']
        description = request.form['description']

        username = session['username']
        
        for user in users.values():
            if user.username == username:
                user.bucketlists[name] = BucketList(name, description)

        data = user.bucketlists
        
        return render_template('managelists.html', acts=data)
    else:
        #pass bucketlist in get
        username = session['username']
        return render_template('managelists.html', data=username)

@app.route('/delete_bucketlist/<name>', methods=['GET'])
def delete_bucketlist(name):
    username = session['username']

    bucketlists = None

    for user in users.values():
        #delete from user.bucketlists
        if user.username == username:
            bucketlists = user.bucketlists
            break

    if name in bucketlists.keys():
        del user.bucketlists[name]
                
    return redirect(url_for('manage'))

@app.route('/add_activity/<bucketlist>')
@app.route('/add_activity', methods=['POST', 'GET'])
def add_activity_to_bucketlist():
    current_bucketlist = request.args.get('bucketlist')
    if request.method == 'POST':
        
        title = request.form['title']        
        description = request.form['description']

        this_user  = None

        username = session['username']

        activity = None
        
        for user in users.values():
            if user.username == username:
                this_user = user
                activity = Activity(title, description)

        

        bcktls = None

        for key in user.bucketlists.keys():
            if current_bucketlist == key:
                bcktls = user.bucketlists[key]
                break

        user.bucketlists[current_bucketlist].add_activity(activity)

        data = user.bucketlists[current_bucketlist].activities

        return render_template('bucketlist.html', bucketlist=current_bucketlist, acts=data)
    else:
        bucketlist = request.args['bucketlist']

        username = session['username']
        return render_template('bucketlist.html', data=username)


@app.route('/update_activity')
def update_activity():
    pass

if __name__ == '__main__':
    app.secret_key = 'xcxcyuxcyuxcyuxcyxuee'

    app.run(debug=True)