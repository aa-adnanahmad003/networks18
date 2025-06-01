
from odoo import models, fields

class AccountMoveLineExt(models.Model):
    _inherit = 'account.move.line'

    hs_code = fields.Char(
        string='HS Code',
        related='product_id.hs_code',
        store=True,
        readonly=True
    )
