from odoo import api, fields, models, _,tools

class Employee(models.Model):
    _inherit = 'hr.employee'

    pan = fields.Char("PAN")
    adahar = fields.Char("Adhaar NO.")
    blood_group = fields.Char("Blood Group")

    country_id = fields.Many2one('res.country', string='Country',
                                 required=True)
    state_id = fields.Many2one('res.country.state', string='State', domain="[('country_id', '=?', country_id)]")
    state_code = fields.Char(related='state_id.code')
    city = fields.Char('City')
    zip = fields.Char('ZIP')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')