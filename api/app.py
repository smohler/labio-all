from flask import Flask
from flask_restx import Api
from api_init import api  # Updated import

# Create Flask app
app = Flask(__name__)

# Initialize the Flask-RESTx API
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)

