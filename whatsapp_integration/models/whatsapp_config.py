from odoo import models, fields, api
import base64
import requests
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class WhatsAppConfig(models.Model):
    _name = 'whatsapp.config'
    _description = 'WhatsApp API Configuration'

    name = fields.Char(string='Name', default='WhatsApp API Configuration')
    api_base_url = fields.Char(string='API Base URL', required=True)
    secret = fields.Char(string='Secret', required=True)
    account = fields.Char(string='Account', required=True)

    # active = fields.Boolean(string='Active', default=True)

    def send_invoice_via_whatsapp(self):
        whatsapp_config = self.env['whatsapp.config'].search([], limit=1)
        # Generate the invoice report in text format
        invoice = self.env['account.move'].browse(2258)
        if not invoice:
            raise UserError("Invoice not found.")

        # Create the message body from invoice data
        message = (
            f"*From:*\n"
            f"{invoice.company_id.name}\n"
            f"{invoice.company_id.street}\n"
            f"{invoice.company_id.mobile}\n"
            f"{invoice.company_id.email}\n\n"
            f"*To:*\n"
            f"{invoice.partner_id.name}\n"
            f"{invoice.partner_id.street}\n"
            f"{invoice.partner_id.mobile}\n\n"

            f"*Invoice #:* {invoice.name}\n"
            f"*Last Due Date:* {invoice.invoice_date.replace(day=15).strftime('%d-%m-%Y')}\n"
            f"*Total Amount Due:* Rs.{invoice.amount_total}\n\n"

            f"*Services Provided:*\n"
        )
        service = '\n'.join(
            f"*{i + 1}-* {name}" for i, name in enumerate(filter(None, invoice.invoice_line_ids.mapped('name'))))
        message += service

        invoice_preview_link = 'http://erp.aa-networks.net:8069' + invoice.preview_invoice().get('url')
        message += f"\nPlease view the invoice at the following link: \n\n{invoice_preview_link}\n\nThank you for your business!!"

        bank_accounts = ("Dear Customer,\n"
                         "Please use the following bank accounts for your payment:\n\n"
                         "*Bank Title:* Bank Islami\n"
                         "*Account Title:* A.A Networks PVT LTD\n"
                         "*Account Number:* 213900024880001\n\n"
                         "*Bank Title:* Habib Bank Limited\n"
                         "*Account Title:* A.A Networks PVT LTD\n"
                         "*Account Number:* 16137900878603\n\n"
                         "Please ensure payment is made before the 15th of every month.\n"
                         "Thank you for your business.\n")

        url = "https://watilio.com/api/send/whatsapp"

        # Define the query parameters
        params = {
            'secret': '0d9a5bb8f95f651bee036d791c60b98f112473ed',
            'account': '17133499396c8349cc7260ae62e3b1396831a8398f661fa533a0506',
            'recipient': '+923015902110',
            'type': 'text',
            'message': message
        }
        # Define the query parameters for Banks Detail
        bank_params = {
            'secret': whatsapp_config.secret,
            'account': whatsapp_config.account,
            'recipient': "923015902110",
            'type': 'text',
            'message': bank_accounts
        }

        # Define the headers
        headers = {
            'Accept': 'application/json',  # Ensure the Accept header matches what is expected
            'Content-Type': 'application/json',  # Ensure the Content-Type is correct
            'User-Agent': 'PostmanRuntime/7.28.4'  # Example User-Agent, replace with Postman's User-Agent
        }

        # Send the request
        requests.get(url, headers=headers, params=params)
        requests.get(url, headers=headers, params=bank_params)

        # # Print the response
        # print(response.status_code)
        # print(response.text)
