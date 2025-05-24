from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class MaesindoGetReports(models.AbstractModel):
    _name = 'report.sale_purchase_tax_report.tax_report_template'
    _description = 'Inventory Reservation QWeb PDF Reports'

    @api.model
    def _get_report_values(self, docids, data):
        # Only Invoices/Bills have Tax
        if data['partner_id']:
            sale_doc = self.env['account.move'].search([('partner_id', '=', int(data['partner_id'])), ('invoice_date', '>=', data['start_date']), ('invoice_date', '<=', data['end_date']), ('state', '=', 'posted'), ('move_type', '=', 'out_invoice'), ('amount_tax_signed', '!=', 0)])
            purchase_doc = self.env['account.move'].search([('partner_id', '=', int(data['partner_id'])), ('invoice_date', '>=', data['start_date']), ('invoice_date', '<=', data['end_date']), ('state', '=', 'posted'), ('move_type', '=', 'in_invoice'), ('amount_tax_signed', '!=', 0)])
        else:
            sale_doc = self.env['account.move'].search([('invoice_date', '>=', data['start_date']), ('invoice_date', '<=', data['end_date']), ('state', '=', 'posted'), ('move_type', '=', 'out_invoice'), ('amount_tax_signed', '!=', 0)])
            purchase_doc = self.env['account.move'].search([('invoice_date', '>=', data['start_date']), ('invoice_date', '<=', data['end_date']), ('state', '=', 'posted'), ('move_type', '=', 'in_invoice'), ('amount_tax_signed', '!=', 0)])

        if sale_doc or purchase_doc:
            return {
                'docs_sale': sale_doc,
                'docs_purchase': purchase_doc,
            }
        else:
            raise ValidationError('No Invoice is available.')