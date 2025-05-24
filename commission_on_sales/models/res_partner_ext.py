from odoo import models, fields, api, _

class ResPartnerExt(models.Model):
    _inherit = 'res.partner'

    commission_agent_id = fields.Many2one('commission.agent', string='Commissioned Agent', ondelete='restrict')

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         name = f"{rec.name} - ({rec.commission_agent_id.user_id.name})"
    #         result.append((rec.id, name))
    #     return result
