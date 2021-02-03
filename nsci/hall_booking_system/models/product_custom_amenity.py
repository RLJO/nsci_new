# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class ProductCustomAmenity(models.Model):
    _name = "product.custom.amenity"

    amenity_id = fields.Many2one(
        'type.amenity',
        string="Amenity",
        required = True
    )
    value = fields.Char(
        string="Value",
    )
    product_id = fields.Many2one(
        'product.product',
        string="Product"
    )
