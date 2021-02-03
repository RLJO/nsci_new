# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class ProductHallType(models.Model):
    _name = "product.hall.type"

    name = fields.Char(
    	string="Name",
    	required = True
	)