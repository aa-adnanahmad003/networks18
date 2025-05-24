from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date

class CommissionSettlement(models.Model):
    _name = 'commission.settlement'
    _description = 'Commission Settlement'
    _rec_name = 'commission_agent_id'

    commission_agent_id = fields.Many2one('commission.agent', string='Commission Agent')
    commission_date = fields.Date(string='Commission Date', default=fields.Date.context_today)
    commission_type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], string='Commission Type', default='fixed')
    percentage = fields.Float(string='% Age', default=0.0)
    commission_settlement_ids = fields.One2many('commission.settlement.line', 'commission_settlement_id')

class CommissionSettlementLine(models.Model):
    _name = 'commission.settlement.line'
    _description = 'Commission Settlement Line'

    partner_id = fields.Many2one('res.partner', string='Customers', domain=[('commission_agent_id', '!=', False)])
    fixed_amount = fields.Float(string='Fixed Amount', default=0.0)
    commission_settlement_id = fields.Many2one('commission.settlement', string='Commission Settlement')


