from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    customer_credit = fields.Float(string="Customer Credit", compute="_compute_customer_credit")
    print_customer_credit_on_invoice = fields.Boolean(string="Print Customer Credit", default=True)

    # @api.depends("invoice_line_ids.product_id", "invoice_line_ids.quantity")
    def _compute_customer_credit(self):
        for invoice_id in self:
            customer_credit = 0
            move_ids = self.env["account.move"].search([("partner_id", "=", self.partner_id.id), ('move_type', '=', 'out_invoice')])
            for move in move_ids:
                customer_credit += move.amount_residual
            invoice_id.customer_credit = customer_credit