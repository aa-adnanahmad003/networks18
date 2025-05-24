from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import AccessError, UserError, ValidationError

class CommissionAgent(models.Model):
    _name = "commission.agent"
    _rec_name = "user_id"
    _description = "Commission Agent"

    user_id = fields.Many2one('res.users', string='Commission Agent')
    mobile = fields.Char(string='Mobile', compute='_compute_agent_mobile', store=True)

    @api.depends('user_id')
    def _compute_agent_mobile(self):
        for agent in self:
            if agent.user_id:
                agent.mobile = agent.user_id.mobile