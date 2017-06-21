import json
from user import User

from flask import (Flask, render_template, url_for, 
        redirect, request, make_response, jsonify, session)

users = {}

app = Flask(__name__)

def get_saved_data():
    try:
        data = json.loads(request.cookies.get('user'))
    except TypeError:
        data = {}
    return data

@app.route('/')
def index():
    data = get_saved_data()
    return render_template('login.html', user=data)

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

        data =  {"name":name, "description": description}

        #return render_template('managelists.html', activity=data)
        #return jsonify({"name":name, "description": description})
        return render_template('managelists.html', data=data)
    else:
        data = get_saved_data()
        return render_template('managelists.html', data=data)
    
@app.route('/show_bucket', methods=['GET'])
def show_bucket():
    return render_template('bucketlist.html')

if __name__ == '__main__':
    app.secret_key = 'xcxcyuxcyuxcyuxcyxuee'

    app.run(debug=True)