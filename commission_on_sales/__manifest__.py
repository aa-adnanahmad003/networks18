# -- coding: utf-8 --
{
    # Module information
    'name': "Commission on Sales",
    'description': """
        Commission Module 
    """,
    'summary': """
        Calculate Commission on Sales
    """,
    'category': 'Commission',
    'author': "Farooq Butt || 0301-5902110",
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    # Dependencies
    'depends': ['base', 'sale_subscription', 'spreadsheet_sale_management'],

    # Views
    'data': [
        'security/ir.model.access.csv',
        'data/schedual_actions.xml',
        'views/commission_agent.xml',
        'views/res_partner_ext.xml',
        'views/sale_order_ext.xml',
        'views/commission_table.xml',
        'wizards/commission_wizard.xml',
        'reports/commission_calculate_report.xml',
    ],

    # Technical
    "installable": True,
    "auto_install": False,
}
