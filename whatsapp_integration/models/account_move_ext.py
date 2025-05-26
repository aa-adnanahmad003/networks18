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
import threading



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
    # TODO: Download PDF report (Not using yet)
    def download_attachment(self, attachment_id):
        # prepare download url
        download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(self.env['ir.config_parameter'].search([('key', '=', 'web.base.url')], limit=1).value) + str(download_url),
            "target": "new",
        }
    # TODO: Download PDF report in custom folder
    def save_attachment_to_folder(self, attachment_id, folder_path):
        """Save the attachment to a specific folder on the server."""
        # Ensure the folder exists, if not, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, mode=0o755)

        # Decode the base64 data of the attachment
        attachment_data = base64.b64decode(attachment_id.datas)

        # Full file path where the attachment will be saved
        file_path = os.path.join(folder_path, attachment_id.name)

        # Save the file
        with open(file_path, 'wb') as file:
            file.write(attachment_data)
    # TODO: Send PDF report and Bank information to customer WhatsApp
    @api.model
    def _send_whatsapp_message(self, attachment_id):
        # WhatsApp API details
        url = "https://watilio.com/api/send/whatsapp"
        secret = '0d9a5bb8f95f651bee036d791c60b98f112473ed'
        account = '17133499396c8349cc7260ae62e3b1396831a8398f661fa533a0506'
        mobile = self.partner_id.mobile

        if mobile:
            # Prepare bank information
            bank_info = ("Dear Customer,\n"
                         "Please use the following bank accounts for your payment:\n\n"
                         "*Bank Title:* Bank Islami\n"
                         "*Account Title:* A.A Networks PVT LTD\n"
                         "*Account Number:* 213900024880001\n\n"
                         "*Bank Title:* Habib Bank Limited\n"
                         "*Account Title:* A.A Networks PVT LTD\n"
                         "*Account Number:* 16137900878603\n\n"
                         "*Invoice Preview:* "
                         f"{str(self.env['ir.config_parameter'].search([('key', '=', 'web.base.url')], limit=1).value)}"
                         f"{self.preview_invoice().get('url')}\n\n"
                         "Please ensure payment is made before the 15th of every month.\n"
                         "Thank you for your business.\n")

            # Prepare the payload for sending the document
            file_payload = {
                'secret': secret,
                'account': account,
                'recipient': mobile,
                'type': 'document',
                'message': f"*Total Amount Due:* Rs.{self.amount_total}/=\n"
                           f"*Last Due Date:* {self.invoice_date.replace(day=15).strftime('%d-%m-%Y')}",
                'document_name': attachment_id.name,
                'document_data': attachment_id.datas.decode('utf-8')  # Base64 encoded PDF
            }

            # Prepare the payload for the bank information text
            bank_payload = {
                'secret': secret,
                'account': account,
                'recipient': mobile,
                'type': 'text',
                'message': bank_info
            }

            # HTTP headers
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'Odoo WhatsApp Integration',
            }

            try:
                # POST request to send the PDF document
                with open(f'/home/adnan/odoo18/env/odoo18/addons/networks18/whatsapp_integration/temp_invoices/{self.name.replace("/", "-")}.pdf', 'rb') as file:
                    files = [('document_file', ('invoice.pdf', file, 'application/pdf'))]

                    # TODO: POST request for PDF file
                    response_file = requests.post(url, headers=headers, data=file_payload, files=files)

                if response_file.status_code == 200:
                    _logger.info(f"Invoice PDF successfully sent to {mobile}. Response: {response_file.text}")
                else:
                    _logger.error(f"Failed to send invoice PDF. Response: {response_file.text}")
            except Exception as e:
                _logger.error(f"Error occurred while sending invoice PDF: {e}")

            try:
                # POST request to send bank information
                response_bank = requests.get(url, headers=headers, params=bank_payload)
                if response_bank.status_code == 200:
                    _logger.info(f"Bank information successfully sent to {mobile}. Response: {response_bank.text}")
                else:
                    _logger.error(f"Failed to send bank information. Response: {response_bank.text}")
            except Exception as e:
                _logger.error(f"Error occurred while sending bank information: {e}")
    # TODO: Delete PDF report in custom folder
    def delete_file_in_folder(self, file_path):
        """Delete the specified file from the folder."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                _logger.info(f"File {file_path} has been successfully deleted.")
            else:
                _logger.warning(f"File {file_path} not found for deletion.")
        except Exception as e:
            _logger.error(f"An error occurred while trying to delete file {file_path}: {e}")

    # def action_post(self):
    #     res = super(AccountMoveExt, self).action_post()
    #
    #     url = "https://watilio.com/api/send/whatsapp"
    #     secret = '0d9a5bb8f95f651bee036d791c60b98f112473ed'
    #     account = '17133499396c8349cc7260ae62e3b1396831a8398f661fa533a0506'
    #     mobile = self.partner_id.mobile
    #
    #     # Generate PDF of the invoice
    #     # invoice_report = self.env.ref('account.account_invoices')
    #     # pdf_bytes = base64.b64encode(
    #     #     self.env['ir.actions.report'].sudo()._render_qweb_pdf(
    #     #         invoice_report, [self.id], data=None)[0])
    #
    #     # Create Attachment
    #     attachment_id = self.create_attachment('account.account_invoices', f'{self.name}.pdf')
    #
    #     # prepare download url
    #     download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
    #     # return {
    #     #     "type": "ir.actions.act_url",
    #     #     "url": str(self.env['ir.config_parameter'].search([('key', '=', 'web.base.url')], limit=1).value) + str(download_url),
    #     #     "target": "new",
    #     # }
    #
    #     if mobile:
    #         # TODO: Bank Information
    #         bank_info = ("Dear Customer,\n"
    #                      "Please use the following bank accounts for your payment:\n\n"
    #                      "*Bank Title:* Bank Islami\n"
    #                      "*Account Title:* A.A Networks PVT LTD\n"
    #                      "*Account Number:* 213900024880001\n\n"
    #                      "*Bank Title:* Habib Bank Limited\n"
    #                      "*Account Title:* A.A Networks PVT LTD\n"
    #                      "*Account Number:* 16137900878603\n\n"
    #                      "*Invoice Preview:* "
    #                      f"{str(self.env['ir.config_parameter'].search([('key', '=', 'web.base.url')], limit=1).value)}"
    #                      # f"http://erp.aa-networks.net:8069"
    #                      f"{self.preview_invoice().get('url')}\n\n"
    #                      "Please ensure payment is made before the 15th of every month.\n"
    #                      "Thank you for your business.\n")
    #         # TODO: Payload for PDF file
    #         file_payload = {
    #             'secret': secret,
    #             'account': account,
    #             'recipient': mobile,
    #             'type': 'document',
    #             'message': f"*Total Amount Due:* Rs.{self.amount_total}/=\n"
    #                        f"*Last Due Date:* {self.invoice_date.replace(day=15).strftime('%d-%m-%Y')}"
    #         }
    #         # TODO: Payload for Bank Information
    #         bank_payload = {
    #             'secret': secret,
    #             'account': account,
    #             'recipient': mobile,
    #             'type': 'text',
    #             'message': bank_info
    #         }
    #         # TODO: Header
    #         headers = {
    #             'Accept': 'application/json',
    #             'User-Agent': 'PostmanRuntime/7.28.4',
    #             'Cookie': 'PHPSESSID=f79a175558d3f375c64b82b30ef2cf7b'
    #         }
    #
    #         try:
    #             # POST request to send the PDF as a WhatsApp document
    #             # response_file = requests.post(url, headers=headers, json=file_payload)
    #             with open('/home/farooq-butt/Downloads/Draft Invoice INV_2024_00004.pdf', 'rb') as file:
    #                 files = [('document_file', ('invoice.pdf', file, 'application/pdf'))]
    #
    #                 # TODO: POST request for PDF file
    #                 response = requests.post(url, headers=headers, data=file_payload, files=files)
    #                 # print(response.text)
    #         except Exception as e:
    #             print(f"Error occurred: {e}")
    #
    #         # TODO: Make request to send Bank details
    #         try:
    #             # TODO: API call for Bank Information
    #             pass
    #             # response = requests.get(url, headers=headers, params=bank_payload)
    #             # print(response.text)
    #         except Exception as e:
    #             print(f"Error occurred: {e}")
    #
    #     return res

    # Backup
    def action_post(self):
        # Call super to handle the standard Odoo process
        res = super(AccountMoveExt, self).action_post()

        if self and self.move_type != 'entry':
            # Create the PDF attachment
            attachment_id = self.create_attachment('account.account_invoices', f'{self.name.replace("/", "-")}.pdf')

            # Specify the custom server-side folder where you want to save the file
            custom_folder_path = '/home/adnan/odoo18/env/odoo18/addons/networks18/whatsapp_integration/temp_invoices'

            # Save the attachment to the custom folder
            self.save_attachment_to_folder(attachment_id, custom_folder_path)

            # Commit the current transaction to avoid issues with background processes
            self.env.cr.commit()
            # Now continue with the WhatsApp message sending
            self._send_whatsapp_message(attachment_id)

            self.delete_file_in_folder(custom_folder_path+ f'/{self.name.replace("/", "-")}.pdf')
        return res

