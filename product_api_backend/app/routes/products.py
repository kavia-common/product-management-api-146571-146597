"""
Ocean Professional Style - Routes
Product CRUD REST endpoints with OpenAPI documentation via flask-smorest.

Endpoints:
- GET    /products          List all products
- POST   /products          Create a product
- GET    /products/<id>     Retrieve a product by id
- PATCH  /products/<id>     Partially update a product
- PUT    /products/<id>     Replace a product
- DELETE /products/<id>     Delete a product
"""

from http import HTTPStatus
from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import ValidationError

from app.schemas.product import (
    ProductSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
)
from app.services.product_service import product_service, NotFoundError

blp = Blueprint(
    "Products",
    "products",
    url_prefix="/products",
    description="Operations for managing products",
)


@blp.errorhandler(ValidationError)
def handle_validation_error(err: ValidationError):
    """Return a standardized validation error response."""
    return {
        "code": HTTPStatus.BAD_REQUEST,
        "status": "Bad Request",
        "message": "Validation failed",
        "errors": err.messages,
    }, HTTPStatus.BAD_REQUEST


@blp.errorhandler(NotFoundError)
def handle_not_found_error(err: NotFoundError):
    """Return a standardized not found response."""
    return {
        "code": HTTPStatus.NOT_FOUND,
        "status": "Not Found",
        "message": str(err),
        "errors": {},
    }, HTTPStatus.NOT_FOUND


@blp.route("/")
class ProductsCollection(MethodView):
    @blp.response(HTTPStatus.OK, ProductSchema(many=True), description="List of products")
    @blp.doc(summary="List products", description="Retrieve all products.")
    def get(self):
        """List all products."""
        products = product_service.list_products()
        return products

    @blp.arguments(ProductCreateSchema)
    @blp.response(HTTPStatus.CREATED, ProductSchema, description="Created product")
    @blp.doc(
        summary="Create product",
        description="Create a new product with name, price, and quantity.",
    )
    def post(self, data: dict):
        """Create a product."""
        product = product_service.create_product(
            name=data["name"], price=data["price"], quantity=data["quantity"]
        )
        return product, HTTPStatus.CREATED


@blp.route("/<int:product_id>")
class ProductItem(MethodView):
    @blp.response(HTTPStatus.OK, ProductSchema, description="Product details")
    @blp.doc(summary="Get product", description="Retrieve a product by its ID.")
    def get(self, product_id: int):
        """Get a product by ID."""
        product = product_service.get_product(product_id)
        return product

    @blp.arguments(ProductUpdateSchema)
    @blp.response(HTTPStatus.OK, ProductSchema, description="Updated product")
    @blp.doc(
        summary="Update product (partial)",
        description="Partially update a product using provided fields.",
    )
    def patch(self, data: dict, product_id: int):
        """Partially update a product."""
        product = product_service.update_product(
            product_id=product_id,
            name=data.get("name"),
            price=data.get("price"),
            quantity=data.get("quantity"),
        )
        return product

    @blp.arguments(ProductCreateSchema)
    @blp.response(HTTPStatus.OK, ProductSchema, description="Replaced product")
    @blp.doc(
        summary="Replace product (full)",
        description="Replace the product data entirely (PUT semantics).",
    )
    def put(self, data: dict, product_id: int):
        """Completely replace a product (PUT). Creates if missing is not supported; returns 404."""
        # Ensure product exists; if not, raise NotFoundError
        _ = product_service.get_product(product_id)
        product = product_service.update_product(
            product_id=product_id,
            name=data["name"],
            price=data["price"],
            quantity=data["quantity"],
        )
        return product

    @blp.response(HTTPStatus.NO_CONTENT)
    @blp.doc(summary="Delete product", description="Delete a product by its ID.")
    def delete(self, product_id: int):
        """Delete a product by ID."""
        product_service.delete_product(product_id)
        return "", HTTPStatus.NO_CONTENT
