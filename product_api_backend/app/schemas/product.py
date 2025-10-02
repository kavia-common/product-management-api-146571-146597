"""
Ocean Professional Style - Schemas
Marshmallow schemas for request validation and response serialization.
"""

from marshmallow import Schema, fields, validate


class ProductBaseSchema(Schema):
    name = fields.String(
        required=True,
        description="Human-readable product name",
        validate=validate.Length(min=1, max=255),
        example="Premium Coffee Beans",
    )
    price = fields.Float(
        required=True,
        description="Unit price (>= 0)",
        validate=validate.Range(min=0),
        example=19.99,
    )
    quantity = fields.Integer(
        required=True,
        description="Available stock quantity (>= 0)",
        validate=validate.Range(min=0),
        example=100,
    )


class ProductCreateSchema(ProductBaseSchema):
    """Schema for creating a new product (server assigns id)."""
    pass


class ProductUpdateSchema(Schema):
    """Schema for updating an existing product (partial updates allowed)."""
    name = fields.String(
        required=False,
        description="Human-readable product name",
        validate=validate.Length(min=1, max=255),
        example="Premium Coffee Beans",
    )
    price = fields.Float(
        required=False,
        description="Unit price (>= 0)",
        validate=validate.Range(min=0),
        example=21.99,
    )
    quantity = fields.Integer(
        required=False,
        description="Available stock quantity (>= 0)",
        validate=validate.Range(min=0),
        example=90,
    )


class ProductSchema(ProductBaseSchema):
    id = fields.Integer(
        required=True,
        description="Unique identifier",
        example=1,
    )
