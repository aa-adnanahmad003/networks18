# -- coding: utf-8 --
{
    # Module information
    'name': "Sale Purchase Tax Report",

    'description': """
        This module will focuses on:
        - Tax Reports
    """,

    'summary': """
        Report for Sale Purchase Tax
    """,

    'author': "Farooq Butt || 0301-5902110",

    'version': '18.0.1.0.0',

    'license': 'LGPL-3',

    # Dependencies
    'depends': ['base','account_accountant','web', 'sale', 'purchase'],

    # Views
    'data': [
        'security/ir.model.access.csv',
        'wizards/tax_report_wizard_view.xml',
        'reports/tax_pdf_report.xml',
    ],

    # Technical
    "installable": True,
    "auto_install": False,
}
