from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CommissionsTable(models.Model):
    _name = "commission.table"
    _description = "Commissions Table"
    _rec_name = "invoice_number"

    commission_agent_id = fields.Many2one('commission.agent', string='Sales Agent')
    partner_id = fields.Many2one('res.partner', string='Customer')
    invoice_number = fields.Char(string='Invoice No.')
    invoice_date = fields.Date(string='Invoice Date')
    invoice_amount = fields.Float(string='Invoice Amount')
    commission_type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], string='Commission Type')
    percentage = fields.Float(string='% Age', default=0.0)
    fixed_amount = fields.Float(string='Fixed Amount', default=0.0)
    total_commission = fields.Float(string='Total Commission')
    move_id = fields.Many2one('account.move')