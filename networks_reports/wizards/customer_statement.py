from odoo import models, fields, api, _
from datetime import datetime, date
import time
from odoo.exceptions import AccessError, UserError, ValidationError


class CustomerStatement(models.TransientModel):
    _name = "customer.statement"
    _description = "This is Wizard to Partners all Moves"

    from_date = fields.Date('From Date : ')
    to_date = fields.Date('To Date : ', default=lambda self: fields.Date.today())
    partner_id = fields.Many2one('res.partner', string='Customer Name')

    def customer_statement_report(self):
        if self.from_date > self.to_date:
            raise ValidationError("'Start Date' Always should be before 'End Date'.")
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'partner_id': self.partner_id.id,
        }
        return self.env.ref('networks_reports.customer_statement_report_id').report_action(self, data=data)

    def cancel_customer_statement_report(self):
        return {'type': 'ir.actions.act_window_close'}
