from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

# Create a Flask application instance
app = Flask(__name__)

# Configuration options for your Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/samples.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Create a Flask-RESTx API instance
api = Api(
    app,
    version="1.0",
    title="Labio All Web API",
    description="A simple web API for Labio All",
)

# Import API resources here (you can add more as needed)
from .resources import SampleResource, SampleListResource, SeedDatabaseResource

# Add API namespaces for resources
api.add_namespace(SampleResource)
api.add_namespace(SampleListResource)
api.add_namespace(SeedDatabaseResource)

