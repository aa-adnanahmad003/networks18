{
    'name': 'Customer Balance in Invoice',
    'version': '18.0.1.0.0',
    'category': 'Account',
    'summery': 'Check for customer credit on Invoice View/Print',
    'author': 'INKERP',
    'website': "https://www.INKERP.com",
    'depends': ['account'],
    
    'data': [
        'reports/account_report_template.xml',
        'views/account_move_view.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
