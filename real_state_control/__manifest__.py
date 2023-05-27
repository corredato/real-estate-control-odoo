# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Real State Control',
    'version' : '1.0',
    'summary': 'Real State Control',
    'sequence': 10,
    'description': """Controle Imobiliário""",
    'category': 'Productivity',
    'website': 'https://github.com/corredato',
    'depends': ['account', 'mail'],
    'data': ['views/realstate.xml',
             'data/data.xml',
             'views/realstate_property.xml',
             'security/ir.model.access.csv'
             ],
    'images': [],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}