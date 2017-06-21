from flask import (Flask, render_template, request, 
                    redirect, url_for, make_response)

from user import User

users = []

app = Flask(__name__)

@app.route('/')
@app.route('/login.html', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user.username == username:
                if user.password == password:
                    return redirect(url_for('managelists', user_name=username))

    else:
        return render_template('login.html')
 
    

    

@app.route('/managelists.html')
def managelists():
    return render_template('managelists.html', username = request.form['username'])

@app.route('/bucketlist.html')
def bucket():
    return render_template('bucketlist.html')

@app.route('/signup.html', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':    
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            user = User(username, email, password)
            users.append(user)

            return render_template('managelists.html', user_name = username)
        else:
            return redirect(url_for('signup'))
    else: 
        return render_template('signup.html')
    


if __name__ == '__main__':
    app.run(debug=True)
