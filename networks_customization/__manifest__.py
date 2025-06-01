# -- coding: utf-8 --
{
    # Module information
    'name': "Networks Customization",
    'description': """
        Networks Pvt. Ltd. Customization Module 
    """,
    'summary': """
        Networks Pvt. Ltd. Customization Module
    """,
    'author': "Farooq Butt || 0301-5902110",
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    # Dependencies
    'depends': ['base', 'account', 'contacts', 'stock_delivery'],

    # Views
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/res_partner_ext.xml',
        'views/account_move_ext.xml',
        'reports/account_move_ext.xml',
    ],

    # Technical
    "installable": True,
    "application": True,
    "auto_install": False,
}
