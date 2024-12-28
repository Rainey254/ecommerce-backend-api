from flask import Flask


app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Welcome to the E-commerce API"}


if __name__ == "__main__":
    print("Starting the flask app"
    app.run(debug=True)
