from odoo import models, fields, api, _
from datetime import datetime, date
import time
from odoo.exceptions import AccessError, UserError, ValidationError


class ProductsDetail(models.TransientModel):
    _name = "products.detail"
    _description = "This is Wizard for Products Detail Parametric Report Date Domain"

    start_date = fields.Date('Start Date : ', required=True)
    end_date = fields.Date('End Date : ', default=datetime.today(), required=True)
    product_id = fields.Many2one('product.product', 'Product : ')
    report_type = fields.Selection([('out_invoice', 'Sale Report'), ('in_invoice', 'Purchase Report')], 'Report Type :',default='out_invoice' , required=True)

    def products_detail_report(self):
        if self.start_date > self.end_date:
            raise ValidationError("'Start Date' Always should be before 'End Date'.")
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'report_type': self.report_type,
            'product_id': self.product_id.id,
        }
        return self.env.ref('networks_reports.products_detail_report_id').report_action(self, data=data)

    def cancel_report(self):
        return {'type': 'ir.actions.act_window_close'}
