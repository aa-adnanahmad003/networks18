from odoo import models, fields, api, _
from datetime import datetime, date
import time
from odoo.exceptions import AccessError, UserError, ValidationError


class ParametricReport(models.TransientModel):
    _name = "tax.report"
    _description = "This is Wizard for Sale Purchase Tax Parametric Report Date Domain"

    start_date = fields.Date('Start Date : ', required=True)
    end_date = fields.Date('End Date : ', default=datetime.today(), required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')

    def tax_parametric_report(self):
        if self.start_date > self.end_date:
            raise ValidationError("'Start Date' Always should be before 'End Date'.")
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'partner_id': self.partner_id.id,
        }
        return self.env.ref('sale_purchase_tax_report.tax_pdf_report_id').report_action(self, data=data)

    def cancel_tax_report(self):
        return {'type': 'ir.actions.act_window_close'}
