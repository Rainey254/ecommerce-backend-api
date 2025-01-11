import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from utils.db import test_db, users_collection
from utils.auth import generate_jwt, verify_jwt, check_role, get_token_from_request
from werkzeug.security import generate_password_hash, check_password_hash
from routes.products import products_bp
from routes.orders import orders_bp
from routes.notifications import notifications_bp
from routes.audit_logs import audit_logs_bp
from routes.categories import categories_bp
from routes.reviews import reviews_bp
from routes.wishlists import wishlists_bp
from jwt import exceptions


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

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')

        if not name or not email or not password:
            return({"error": "Name, email, and password are required."}), 400

        # Check if user already exists
        if users_collection.find_one({'email': email}):
            return {"error": "Email already in use. Please log in."}, 409
        
        hashed_password = generate_password_hash(password)


        # Save the user in the database
        users_collection.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role
        })

        return {"message": "Registration successful! Please log in."}, 201


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user in the database
        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            # Generate JWT
            token = generate_jwt(user_id=str(user['_id']), role=user['role'])
            return {"message": "Logged in successfully!", "token": token}, 200
        else:
            return {"error": "Invalid email or password."}, 401


@app.route('/admin', methods=['GET'])
def admin():
    try:
        # Extract the token from the request
        token = get_token_from_request()
        if not token:
            return {"error": "Authorization token is missing."}, 400

        # Verify the user's role
        if not check_role(token, 'admin'):
            return {"error": "Access denied. Admin privileges required."}, 403

        # Successful access
        return {"message": "Welcome to the admin page!"}, 200

    except exceptions.ExpiredSignatureError:
        return {"error": "The token has expired. Please log in again."}, 401
    except exceptions.InvalidTokenError:
        return {"error": "The token is invalid. Please log in again."}, 401
    except ValueError as e:
        return {"error": f"An error occurred: {str(e)}"}, 401
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}, 500


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))


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