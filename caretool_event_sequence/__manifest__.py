#-*- coding:utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'Caretool Event Sequence',
    'summary': 'Dedicated number sequence for Event-related Sale Orders and Invoices',
    'description': """
Assigns a separate, editable sequence to Sale Orders
keeping them numbered apart from regular
sales.
    """,
    'version': '18.0.1.0.0',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'company': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'https://acespritech.com',
    'category': 'Tool',
    'depends': ['base', 'sale_management', 'account', 'website_sale', 'event_sale'],
    'data': [
        'data/ir_sequence.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: