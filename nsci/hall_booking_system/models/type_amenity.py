# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class TypeAmenity(models.Model):
    _name = "type.amenity"

    name = fields.Char(
        string="Name",
        required = True
    )