# -*- coding: utf-8 -*-
from dateutil import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, Warning, ValidationError
from datetime import datetime, date


class ProjectTask(models.Model):
    _inherit = "project.task"

    custom_is_booking_request = fields.Boolean(
        string="Is Booking",
        # copy=tru
        copy=True
    )
    custom_is_confirm_stage = fields.Boolean(
        string="Is Confirm Stage",
        copy=False
    )
    custom_is_cancel_stage = fields.Boolean(
        string="Is Cancel Stage",
        copy=False
    )
    custom_booking_id = fields.Many2one(
        'product.category',
        string="Room Type"
    )
    custom_service_ids = fields.Many2many(
        'product.hall.type',
        string="Services"
    )
    custom_organizer_id = fields.Many2one(
        'res.partner',
        string="Supervisor"
    )
    custom_location_id = fields.Many2one(
        'res.partner',
        readonly=True,
        string="Location"
    )
    custom_responsible_id = fields.Many2one(
        'res.users',
        string="Responsible"
    )
    custom_capacity = fields.Integer(
        string="Capacity"
    )
    custom_start_date = fields.Datetime(
        string="Start Date"
    )
    custom_end_date = fields.Datetime(
        string="End Date"
    )
    custom_buffer_start_date = fields.Datetime(
        string="Buffer Start Date"
    )
    custom_buffer_end_date = fields.Datetime(
        string="Buffer End Date"
    )
    custom_booking_number = fields.Char(
        string="Booking No.",
        readonly=True
    )

    def custom_services_print(self):
        str_services = ''
        for rec in self:
            for service in self.custom_service_ids:
                if str_services == '':
                    str_services = service.name
                else:
                    str_services = str_services + ' , ' + service.name
        return str_services

    def action_custom_booking_slip_send(self):
        self.ensure_one()
        template = self.env.ref('hall_booking_system.custom_mail_template_booking_slip', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='project.task',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            custom_layout='mail.mail_notification_light',
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    # @api.onchange('custom_booking_id')
    # def _onchange_custom_booking_id(self):
    #     if self.custom_booking_id:
    #         #self.custom_organizer_id = self.custom_booking_id.custom_organizer_id.id
    #         self.custom_location_id = self.custom_booking_id.custom_location_id.id
    #         self.custom_responsible_id = self.custom_booking_id.custom_responsible_id.id
    #         self.custom_capacity = self.custom_booking_id.custom_capacity
    #         self.custom_service_ids = [(6, 0, self.custom_booking_id.custom_booking_type_id.ids)]

    @api.onchange('custom_buffer_end_date')
    def _onchange_custom_buffer_end_date(self):
        if self.custom_buffer_end_date:
            self.date_deadline = self.custom_buffer_end_date

    def write(self, vals):
        if vals.get('stage_id'):
            stage_id = self.env['project.task.type'].browse(vals.get('stage_id'))
            if stage_id.custom_is_confirm:
                self.custom_is_confirm_stage = True
                self.custom_is_cancel_stage = False
                if self.custom_booking_id:
                    for task in self.custom_booking_id.custom_task_ids:
                        if task.stage_id.custom_is_confirm:
                            if task.custom_buffer_start_date <= self.custom_buffer_start_date and task.custom_buffer_end_date >= self.custom_buffer_start_date:
                                raise UserError(_('Seems selected location is already booked.'))
                            if task.custom_buffer_start_date <= self.custom_buffer_end_date and task.custom_buffer_end_date >= self.custom_buffer_end_date:
                                raise UserError(_('Seems selected location is already booked.'))
        return super(ProjectTask, self).write(vals)

    def custom_booking_confirm(self):
        stage_id = self.env['project.task.type'].search([('custom_is_confirm', '=', True)], limit=1)
        self.stage_id = stage_id.id
        if not self.custom_booking_number:
            self.custom_booking_number = self.env['ir.sequence'].next_by_code('booking.request.confirm')

    def custom_booking_cancel(self):
        stage_id = self.env['project.task.type'].search([('custom_is_canceled', '=', True)], limit=1)
        self.stage_id = stage_id.id
        self.custom_is_confirm_stage = False
        self.custom_is_cancel_stage = True

    guest_country = fields.Char(string="Guest Country")
    contact_person = fields.Char(string="Contact Person")

    agent_name = fields.Char(string="Agent Name")
    remark = fields.Char(string="Remark")
    other_info = fields.Char(string="Other Info")
    cancellation_date = fields.Date(string="Cancellation Date")
    member_id = fields.Many2one('res.partner', string="Membership ID")
    room_number_id = fields.Many2one('product.product', string="Room Number ID")
    number_of_rooms = fields.Integer(string="Number of Rooms")
    number_of_adults = fields.Integer(string="No. of Adults")
    number_of_children = fields.Integer(string="No. of Children")

    total_guests = fields.Integer(string="Total No. of guests", compute="_onchange_number_of_adultsChildren")

    total_no_nights = fields.Integer(string="Total No. Nights", compute="_onchange_number_of_nights")

    payment_terms = fields.Many2one('account.payment.term', string="Payment Terms")
    room_price = fields.Float(string="Room Price", compute="_onchange_room_type", store=True)

    custom_name = fields.Char(string="Name")
    custom_age = fields.Char(string="Age")

    guest_room_type = fields.Char(string="Guest Room Type", compute="_onchange_guest_member")
    guest_room_no_id = fields.Char(string="Guest Room No.", compute="_onchange_guest_member")
    guest_number_of_children = fields.Char(string="Guest Number of Children", compute="_onchange_guest_member")
    guest_number_of_adults = fields.Char(string="Guest Number of Adults", compute="_onchange_guest_member")
    # room_no_column = fields.Char(string="Room No.")
    total_no_guests = fields.Char(string="Total No. Guests", compute="_onchange_guest_member")

    guest_or_member = fields.Char(string="Guest or Member")
    # room_position = fields.One2many('custom.room.position', 'temp_field', string="Room Position")
    # capacity = fields.Char(string="Capacity", compute="_onchange_room_number_id")

    # @api.depends('room_number_id')
    # def _onchange_room_number_id(self):
    #     for record in self:
    #         if record.room_number_id and record.room_number_id.custom_capacity:
    #             record.capacity = record.room_number_id.custom_capacity

    @api.onchange('guest_or_member', 'number_of_children', 'number_of_adults', 'total_guests', 'custom_booking_id', 'room_number_id')
    def _onchange_guest_member(self):
        if (self.guest_or_member == 'guest') and self.custom_booking_id and self.room_number_id and self.number_of_adults and self.total_guests or self.number_of_children:
            self.guest_room_type = self.custom_booking_id.name
            self.guest_room_no_id = self.room_number_id.name
            self.guest_number_of_children = self.number_of_children
            self.guest_number_of_adults = self.number_of_adults
            self.total_no_guests = self.total_guests
        else:
            self.guest_room_type = "0"
            self.guest_room_no_id = "0"
            self.guest_number_of_children = "0"
            self.guest_number_of_adults = "0"
            self.total_no_guests = "0"

    @api.depends('room_number_id', 'number_of_rooms')
    def _onchange_room_type(self):
        for record in self:
            if record.room_number_id and record.number_of_rooms:
                record.room_price = record.number_of_rooms * record.room_number_id.lst_price

    @api.onchange('number_of_adults', 'number_of_children', 'number_of_rooms')
    def _onchange_number_of_adultsChildren(self):
        for record in self:
            total = record.number_of_adults + record.number_of_children
            if record.number_of_adults and record.number_of_rooms or record.number_of_children:
                if ((float(total) / float(record.number_of_rooms)) > 4):
                    raise ValidationError(_("More than 4 guests not allowed in a single room."))
                else:
                    record.total_guests = total

    @api.onchange('custom_start_date', 'custom_end_date')
    def _onchange_number_of_nights(self):
        if self.custom_end_date and self.custom_start_date:
            date1 = datetime.strptime(str(self.custom_end_date), '%Y-%m-%d %H:%M:%S')
            date2 = datetime.strptime(str(self.custom_start_date), '%Y-%m-%d %H:%M:%S')
            r = relativedelta.relativedelta(date1, date2)
            # time_min = r.days * 1440 + r.hours * 60 + r.minutes
            # time = time_min / 60
            self.total_no_nights = r.days
        # for i in self:
        # end_date = self.custom_end_date.strftime("%dd/%mm%yyyy")
        # start_date = self.custom_start_date.strftime("%dd/%mm%yyyy")
        # no_of_nights = end_date - start_date
        # self.total_no_nights = no_of_nights

# class CustomRoomPosition(models.Model):
#     _name = 'custom.room.position'
#
#     temp_field = fields.Many2one('project.task', string="temp")
#

    # @api.onchange('custom_booking_id', 'room_number_id', '')
    # def on_change_room_type(self):
    #     for record in self:
    #         if record.custom_boking_id and record.room_number_id:
    #             record.room_type_column = record.custom_booking_id
    #             record.room_no_column = record.room_number_id











