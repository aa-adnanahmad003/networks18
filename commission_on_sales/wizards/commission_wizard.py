from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class CommissionWizard(models.TransientModel):
    _name = "commission.wizard"
    _description = "This is Wizard to Commission Calculate"

    from_date = fields.Date('From Date : ')
    to_date = fields.Date('To Date : ', default=lambda self: fields.Date.today())
    commission_agent_id = fields.Many2one('commission.agent', string='Sales Agent')

    def commission_calculate_report(self):
        if self.from_date > self.to_date:
            raise ValidationError("'Start Date' Always should be before 'End Date'.")
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'commission_agent_id': self.commission_agent_id.id,
        }
        return self.env.ref('commission_on_sales.commission_calculate_report_id').report_action(self, data=data)


    def cancel_report(self):
        return {'type': 'ir.actions.act_window_close'}
