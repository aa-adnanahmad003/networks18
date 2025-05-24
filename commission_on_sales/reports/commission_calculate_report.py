from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class CommissionCalculate(models.AbstractModel):
    _name = 'report.commission_on_sales.commission_calculate_template_id'
    _description = 'Commission Calculate Report'

    @api.model
    def _get_report_values(self, docids, data):
        if data['from_date'] and data['to_date'] and data['commission_agent_id']:
            doc = self.env['commission.table'].search([('invoice_date', '>=', data['from_date']), ('invoice_date', '<=', data['to_date']), ('commission_agent_id', '=', data['commission_agent_id'])])
        elif data['from_date'] and data['to_date'] and not data['commission_agent_id']:
            doc = self.env['commission.table'].search([('invoice_date', '>=', data['from_date']), ('invoice_date', '<=', data['to_date'])])
        if doc:
            return {
                'docs': doc,
            }
        else:
            raise ValidationError('No Record is available regarding the Parameters.')


