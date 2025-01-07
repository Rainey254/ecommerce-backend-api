import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from utils.db import test_db, users_collection
from utils.auth import check_role
from werkzeug.security import generate_password_hash, check_password_hash
from routes.products import products_bp
from routes.orders import orders_bp
from routes.notifications import notifications_bp
from routes.audit_logs import audit_logs_bp
from routes.categories import categories_bp
from routes.reviews import reviews_bp
from routes.wishlists import wishlists_bp


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(audit_logs_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(wishlists_bp)


#home route
@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['user'] = {'name': user['name'], 'email': user['email'], 'role': user['role']}
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password. Please try again.", "error")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']


        if users_collection.find_one({'email': email}):
            flash("Email already in use. Please log in.", "error")
            return redirect(url_for('login'))
        
        hashed_password = generate_password_hash(password)

        role = 'user'

        users_collection.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role
        })

        flash("Registration success! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    user = session.get('user')
    if not user:
        flash("You need to log in first.", "error")
        return redirect(url_for('login'))
    
    if not check_role(user, 'admin'):
        flash("You do not have permission to access this page.", "error")
        return redirect(url_for('home'))
    
    return render_template('admin.html')

@app.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        flash("You need to log in first.", "error")
        return redirect(url_for('login'))
    
    return render_template('profile.html', user=user)

if __name__ == "__main__":
    print("Starting the flask app")
    app.run(debug=True)