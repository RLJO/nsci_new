# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    custom_booking_ok = fields.Boolean(
        string="Can be Booked",
        # copy=true
        copy=True
    )

class ProductProduct(models.Model):
    _inherit = "product.product"

    custom_organizer_id = fields.Many2one(
        'res.partner',
        domain=[('type', '=', 'contact')],
        string="Supervisor",
        # copy=true
        copy=True
    )
    custom_location_id = fields.Many2one(
        'res.partner',
        domain=[('type', '!=', 'contact')],
        string="Location",
        # copy=true
        copy=True
    )
    custom_responsible_id = fields.Many2one(
        'res.users',
        string="Responsible",
        # copy=true
        copy=True
    )
    custom_capacity = fields.Integer(
        string="Capacity",
        # copy=true
        copy=True
    )
    custom_task_ids = fields.One2many(
        'project.task',
        'custom_booking_id',
        readonly=True,
        string="Booking Request"
    )
    custom_product_amenity_ids = fields.One2many(
        'product.custom.amenity',
        'product_id',
        string="Amenities",
        # copy=true
        copy=True
    )
    custom_booking_type_id = fields.Many2one(
        'product.hall.type',
        string="Booking Type",
        # copy=true
        copy=True
    )

    def custom_show_get_booking_requests(self):
        for rec in self:
            res = self.env.ref('hall_booking_system.custom_product_booking_request_action')
            res = res.read()[0]
            res['domain'] = str([('id', 'in', self.custom_task_ids.ids)])
        return res    