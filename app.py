from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')



@app.route('/save', methods=['POST'])
def save():
    import pdb; pdb.set_trace()
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)