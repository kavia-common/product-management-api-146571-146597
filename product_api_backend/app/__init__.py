from flask import Flask, jsonify
from flask_cors import CORS
from flask_smorest import Api

from .routes.health import blp as health_blp
from .routes.products import blp as products_blp

# Application factory-like setup with global app instance for simplicity
app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS: Open for demo; restrict in production.
CORS(app, resources={r"/*": {"origins": "*"}})

# Ocean Professional - API Metadata
app.config["API_TITLE"] = "Product Management API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_JSON_PATH"] = "openapi.json"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Api and blueprints
api = Api(app, spec_kwargs={"servers": [{"url": "/"}]})
api.register_blueprint(health_blp)
api.register_blueprint(products_blp)


# PUBLIC_INTERFACE
@app.get("/docs/help")
def docs_help():
    """
    Documentation helper endpoint.

    Returns:
        JSON with quick info about docs and API usage.
    """
    return jsonify(
        {
            "message": "Welcome to the Product Management API",
            "docs": "/docs",
            "openapi": "/docs/openapi.json",
            "endpoints": {
                "health": "/",
                "products": "/products",
            },
        }
    )
