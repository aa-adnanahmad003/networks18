
from odoo import models, fields

class ProductTemplateExt(models.Model):
    _inherit = 'product.template'

    hs_code = fields.Char(string='HS Code')
