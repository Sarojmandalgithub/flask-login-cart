from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient('mongodb+srv://saroj8520:Saroj1996@cluster0.qpmtwfy.mongodb.net/mydatabase?retryWrites=true&w=majority')
db = client['user_db']
users_collection = db['users']

@app.route('/')
def landing_page():
    if 'user' in session:
        user_data = users_collection.find_one({'username': session['user']})
        return render_template('index.html', user_data=user_data)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['user'] = username
            return redirect(url_for('landing_page'))
    return render_template('login.html')

@app.route('/admin')
def admin_page():
    if 'user' in session:
        user = users_collection.find_one({'username': session['user']})
        if user and user.get('admin', False):
            all_users = list(users_collection.find())
            return render_template('admin.html', users=all_users)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        user = {
            'username': username,
            'email': email,
            'password': password,
            'role': role
        }
        users_collection.insert_one(user)
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
