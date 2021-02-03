# -*- coding: utf-8 -*-
# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Booking System Management using Project',
    'version' : '3.1.2',
    'price' : 69.0,
    'currency': 'EUR',
    'category': 'Operations/Project',
    'license': 'Other proprietary',
    'live_test_url': 'https://youtu.be/LZhjmDuEiTw',
    'images': [
        'static/description/img.jpg',
    ],
    'summary' : 'Manage bookings of Halls (banquet hall, marriage hall, conference hall), Training Rooms, Farm House, Meeting Spaces, CO-WORKING space, Village hall...',
    'description': """
Allow your project team to manage booking requests.
Allow you to configure and manage types.
Allow you to configure and manage amenity types.
Allow you to configure and manage booking products.
Allow you to create booking requests and book it and also allow you to cancel it anytime.
Show booking requests a smart button on booking products.
Send the booking confirmation email to the customer.
Allow you to print a booking confirmation slip and send it by email to the customer.
This app is built on top of project task in Odoo so we have used project task model as a booking request which will allow you to manage and use various features of Odoo Project management which can help you.
You can use this app for any kind of booking as mentioned above and if that fit your requirements you can use it for various booking purposes. Above mentioned example might be limited but the app can be used for other bookings as well so it will depend on you how you are going to use it.

For more details please check below screenshots and watch the video. 
    """,
    'author' : 'Probuse Consulting Service Pvt. Ltd.',
    'website' : 'wwww.probuse.com',
    'depends' : [
        'product',
        'project'
    ],
    'support': 'contact@probuse.com',
    'data' : [
        'security/ir.model.access.csv',
        'report/booking_report_view.xml',
        'data/booking_request_sequence.xml',
        'data/mail_data.xml',
        'views/product_template_view.xml',
        'views/product_hall_type_view.xml',
        'views/project_task_view.xml',
        'views/project_task_type_view.xml',
        'views/type_amenity_view.xml',
        'views/product_custom_amenity_view.xml',
        'views/menu.xml',
    ],
    'qweb': [
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
