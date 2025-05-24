from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrderExt(models.Model):
    _inherit = "sale.order"

    commission_type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], string='Commission Type', default='fixed')
    percentage = fields.Float(string='% Age', default=0.0)
    fixed_amount = fields.Float(string='Fixed Amount', default=0.0)
    commission_agent_id = fields.Many2one('commission.agent', string='Commissioned Agent', compute='_compute_commission_agent', store=True)

    @api.depends('partner_id')
    def _compute_commission_agent(self):
        for rec in self:
            if rec.partner_id and rec.partner_id.commission_agent_id:
                rec.commission_agent_id = rec.partner_id.commission_agent_id.id
            else:
                rec.commission_agent_id = None