import json
from user import User

from flask import (Flask, render_template, url_for, 
        redirect, request, make_response, jsonify)

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



@app.route('/save', methods=['POST', 'GET'])
def save():
    if request.method == 'POST':
        response = make_response(redirect(url_for('manage')))
        data = get_saved_data()
        data.update(dict(request.form.items()))
        response.set_cookie('user', json.dumps(data))#dict(request.form.items())['username'])

        return response
    else:
        return render_template('managelists.html', data=data)

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
    


if __name__ == '__main__':
    app.run(debug=True)