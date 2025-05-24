# -- coding: utf-8 --
{
    # Module information
    'name': "Networks Reports",

    'description': """
        This module will focuses on:
        - Reports
    """,

    'summary': """
        Report for Networks Pvt. Ltd.
    """,

    'author': "Farooq Butt || 0301-5902110",

    'version': '18.0.1.0.0',

    'license': 'LGPL-3',

    # Dependencies
    'depends': ['base', 'stock', 'sale_purchase_tax_report'],

    # Views
    'data': [
        'security/ir.model.access.csv',
        'wizards/products_detail_wizard.xml',
        'wizards/customer_statement.xml',
        'reports/products_detail_report.xml',
        'reports/customer_statement_report.xml',
        'reports/account_move_report.xml',
    ],

    # Technical
    "installable": True,
    "auto_install": False,
}
