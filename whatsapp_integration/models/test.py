from odoo import models, fields, api
from odoo.addons.website.models.ir_attachment import Attachment
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date
import os
import logging
_logger = logging.getLogger(__name__)
import requests
import base64
from io import BytesIO
import http.client
import mimetypes
from codecs import encode

class AccountMoveExt(models.Model):
    _inherit = 'account.move'

    # TODO: Create PDF type attachment of any PDF report
    def create_attachment(self, report_ref, name):
        """Creates an attachment for the specified report."""
        report = self.env.ref(report_ref)
        pdf = report._render_qweb_pdf(report.id, res_ids=self.id)
        b64_pdf = base64.b64encode(pdf[0])

        attachment = self.env['ir.attachment'].create({
            'name': name,
            'type': 'binary',
            'datas': b64_pdf,
            'store_fname': name,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })
        return attachment

    def action_post(self):
        res = super(AccountMoveExt, self).action_post()

        url = "https://watilio.com/api/send/whatsapp"
        secret = '0d9a5bb8f95f651bee036d791c60b98f112473ed'
        account = '17133499396c8349cc7260ae62e3b1396831a8398f661fa533a0506'
        mobile = self.partner_id.mobile

        # Generate PDF of the invoice
        invoice_report = self.env.ref('account.account_invoices')
        pdf_bytes = base64.b64encode(
            self.env['ir.actions.report'].sudo()._render_qweb_pdf(
                invoice_report, [self.id], data=None)[0])
        # Create Attachment
        attachment = self.create_attachment('account.account_invoices', f'{self.name}')

        if mobile:
            # TODO: Bank Information
            bank_info = ("Dear Customer,\n"
                             "Please use the following bank accounts for your payment:\n\n"
                             "*Bank Title:* Bank Islami\n"
                             "*Account Title:* A.A Networks PVT LTD\n"
                             "*Account Number:* 213900024880001\n\n"
                             "*Bank Title:* Habib Bank Limited\n"
                             "*Account Title:* A.A Networks PVT LTD\n"
                             "*Account Number:* 16137900878603\n\n"
                             "*Invoice Preview:* "
                             f"http://erp.aa-networks.net:8069"
                             f"{self.preview_invoice().get('url')}\n\n"
                             "Please ensure payment is made before the 15th of every month.\n"
                             "Thank you for your business.\n")
            # TODO: Payload for PDF file
            file_payload = {
                'secret': secret,
                'account': account,
                'recipient': mobile,
                'type': 'document',
                'message': f"*Total Amount Due:* Rs.{self.amount_total}/=\n"
                           f"*Last Due Date:* {self.invoice_date.replace(day=15).strftime('%d-%m-%Y')}"
            }
            # TODO: Payload for Bank Information
            bank_payload = {
                'secret': secret,
                'account': account,
                'recipient': mobile,
                'type': 'text',
                'message': bank_info
            }
            # TODO: Header
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'PostmanRuntime/7.28.4',
                'Cookie': 'PHPSESSID=f79a175558d3f375c64b82b30ef2cf7b'
            }

            try:
                with open('/home/farooq-butt/Downloads/Draft Invoice INV_2024_00004.pdf', 'rb') as file:
                    files = [('document_file', ('invoice.pdf', file, 'application/pdf'))]

                    # TODO: POST request for PDF file
                    response = requests.post(url, headers=headers, data=file_payload, files=files)
                    print(response.text)
            except Exception as e:
                print(f"Error occurred: {e}")

            # TODO: Make request to send Bank details
            try:
                # TODO: API call for Bank Information
                # response = requests.get(url, headers=headers, params=bank_payload)
                print(response.text)
            except Exception as e:
                print(f"Error occurred: {e}")

        return res

        # return res
        # # Generate the download URL
        # download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
        # base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # full_download_url = f"{base_url}{download_url}"
        #
        # # Return the action to immediately open the download link
        # result = {
        #     "type": "ir.actions.act_url",
        #     "url": full_download_url,
        #     "target": "new",
        # }