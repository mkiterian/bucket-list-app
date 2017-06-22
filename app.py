import json
from user import User
from bucketlist import BucketList
from user import User
from activity import Activity

from flask import (Flask, render_template, url_for, 
        redirect, request, make_response, jsonify, session)

users = {}

app = Flask(__name__)

'''
def get_saved_data():
    try:
        data = json.loads(request.cookies.get('user'))
    except TypeError:
        data = {}
    return data
'''

current_bucketlist = None

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print('tttttttttttttttttttttttttttt')
        print(users)

        
        for user in users.values():
            if user.username == username:
                if user.password == password:
                    session['username'] = request.form['username']
                    return redirect(url_for('manage'))
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            user = User(username, email, password)
            users['email'] = user

            session['username'] = request.form['username']
            
            return redirect(url_for('manage', data = username))

        else:
            return redirect(url_for('signup'))
    else:
        return render_template('signup.html')


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
        #data =  {"name":name, "description": description}
        
        #return render_template('managelists.html', activity=data)
        #return jsonify({"name":name, "description": description})
        return render_template('managelists.html', acts=data)
    else:

        username = session['username']
        return render_template('managelists.html', data=username)
    
@app.route('/show_bucket', methods=['GET'])
def show_bucket():
    return render_template('bucketlist.html')

@app.route('/add_activity/<bucketlist>')
@app.route('/add_activity', methods=['POST', 'GET'])
def add_activity_to_bucketlist():
    current_bucketlist = request.args.get('bucketlist')
    print('++++++++++++++++++++++++++++')
    print(current_bucketlist)
    print('++++++++++++++++++++++++++++')
    if request.method == 'POST':
        
        title = request.form['title']        
        description = request.form['description']

        print('#'*20)
        print(title)
        print(description)

        username = session['username']
        
        for user in users.values():
            if user.username == username:
               activity = Activity(title, description)
            #    current_bucketlis = "Travel"
            #    current_bucketlist.add_activity(activity)

        data =  {"title":title, "description": description}
        print('dddddddddddddddddddddddd')
        print(data)
        print('dddddddddddddddddddddd')
        
        #return render_template('managelists.html', activity=data)
        #return jsonify({"name":name, "description": description})
        return render_template('bucketlist.html', bucketlist=current_bucketlist, acts=data)
    else:
        bucketlist = request.args['bucketlist']

        username = session['username']
        return render_template('bucketlist.html', data=username)



if __name__ == '__main__':
    app.secret_key = 'xcxcyuxcyuxcyuxcyxuee'

    app.run(debug=True)