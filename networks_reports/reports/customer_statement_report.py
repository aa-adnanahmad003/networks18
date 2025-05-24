from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class CustomerStatements(models.AbstractModel):
    _name = 'report.networks_reports.customer_statement_template'
    _description = 'Customer Statement Report'

    @api.model
    def _get_report_values(self, docids, data):
        if data['from_date'] and data['to_date'] and data['partner_id']:
            doc = self.env['account.move'].search(
                [('invoice_date', '>=', data['from_date']), ('invoice_date', '<=', data['to_date']),
                 ('partner_id', '=', data['partner_id'])])
        elif data['from_date'] and data['to_date']:
            doc = self.env['account.move'].search(
                [('invoice_date', '>=', data['from_date']), ('invoice_date', '<=', data['to_date'])])
        if doc:
            return {
                'docs': doc,
            }
        else:
            raise ValidationError('No Record is available regarding the Parameters.')
