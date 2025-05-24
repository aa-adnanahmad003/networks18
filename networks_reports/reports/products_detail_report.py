from odoo import _,api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class ProductsDetail(models.AbstractModel):
    _name = 'report.networks_reports.products_detail_template'
    _description = 'Products Detail QWeb PDF Reports'

    @api.model
    def _get_report_values(self, docids, data):
        if data['report_type'] == 'out_invoice':
            if data['product_id']:
                doc = self.env['account.move.line'].search([('date', '>=', data['start_date']), ('date', '<=', data['end_date']), ('parent_state', '=', 'posted'), ('move_type', '=', 'out_invoice'), ('product_id', '!=', False), ('product_id', '=', data['product_id'])])
            else:
                doc = self.env['account.move.line'].search([('date', '>=', data['start_date']), ('date', '<=', data['end_date']), ('parent_state', '=', 'posted'), ('move_type', '=', 'out_invoice'), ('product_id', '!=', False)])
        else:
            if data['product_id']:
                doc = self.env['account.move.line'].search([('date', '>=', data['start_date']), ('date', '<=', data['end_date']), ('parent_state', '=', 'posted'), ('move_type', '=', 'in_invoice'), ('product_id', '!=', False), ('product_id', '=', data['product_id'])])
            else:
                doc = self.env['account.move.line'].search([('date', '>=', data['start_date']), ('date', '<=', data['end_date']), ('parent_state', '=', 'posted'), ('move_type', '=', 'in_invoice'), ('product_id', '!=', False)])

        if doc:
            return {
                'docs': doc,
            }
        else:
            raise ValidationError('No Record is available regarding the Parameters.')