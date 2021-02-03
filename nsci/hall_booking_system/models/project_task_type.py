# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    custom_is_confirm = fields.Boolean(
        string="Is Booking Confirm",
    )
    custom_is_canceled = fields.Boolean(
        string="Is Booking Canceled",
    )