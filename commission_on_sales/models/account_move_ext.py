from odoo import api, fields, models

class AccountMoveExt(models.Model):
    _inherit = "account.move"

    def _make_commission_from_invoices(self):
        invoices = self.env['account.move'].search([('move_type', '=', 'out_invoice'), ('state', '=', 'posted'), ('company_id', '=', self.env.company.id)])
        commission_inv_num = self.env['commission.table'].search([]).mapped('invoice_number')
        commission_table = self.env['commission.table']
        for invoice in invoices:
            if invoice.name not in commission_inv_num and invoice.partner_id.commission_agent_id and invoice.line_ids.sale_line_ids and str(invoice.id) not in commission_table.mapped('move_id'):
                vals = {
                    'commission_agent_id': invoice.partner_id.commission_agent_id.id,
                    'partner_id' : invoice.partner_id.id,
                    'invoice_number' : invoice.name,
                    'invoice_date' : invoice.invoice_date,
                    'invoice_amount' : invoice.amount_total_signed,
                    'commission_type' : invoice.line_ids.sale_line_ids.order_id.commission_type,
                    'total_commission' : invoice.line_ids.sale_line_ids.order_id.fixed_amount if invoice.line_ids.sale_line_ids.order_id.commission_type=='fixed' else (invoice.amount_total_signed/100*invoice.line_ids.sale_line_ids.order_id.percentage),
                    'move_id' : invoice.id
                }
                commission_table.create(vals)
                # self.env.cr.commit()
