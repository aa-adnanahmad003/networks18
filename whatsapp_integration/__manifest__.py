# __manifest__.py
{
    'name': 'WhatsApp Integration',
    'version': '1.0',
    'summary': 'Module to send Invoices via WhatsApp API',
    'description': 'This module allows the Sent Invoices to Customers via WhatsApp API.',
    'author': 'ITSoft Creations',
    'depends': ['base', 'account'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/whatsapp_config.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
