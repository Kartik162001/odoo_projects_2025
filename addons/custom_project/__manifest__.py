# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Water Jug Supply',
    'version': '17.0.1.0',
    'summary': 'Invoices & Payments',
    'sequence': 11,
    'description': """
    """,
    'depends': ['base','mail'],
    'data': [
        "security/group.xml",
        "security/ir.model.access.csv",
        "views/delivery_view.xml",
        "data/whatsapp_templates.xml"
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
