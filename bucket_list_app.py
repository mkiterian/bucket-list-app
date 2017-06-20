from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/managelists.html')
def managelists():
    return render_template('managelists.html')

@app.route('/bucketlist.html')
def bucket():
    return render_template('bucketlist.html')


if __name__ == '__main__':
    app.run(debug=True)
