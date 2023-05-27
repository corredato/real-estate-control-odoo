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
    'depends': ['base','account', 'mail'],
    'data': ['security/ir.model.access.csv',
             'data/data.xml',
             'views/realstate.xml',
             'views/realstate_property.xml'
             ],
    'images': [],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}