from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class ResPartnerExt(models.Model):
    _inherit = 'res.partner'

    @api.constrains('mobile')
    def _check_mobile_number(self):
        for partner in self:
            if partner.mobile and partner.mobile[0] == '+':
                if partner.mobile[:3] != '+92' or len(partner.mobile) != 13:
                    raise ValidationError("Mobile number must start with '+92' and should be exactly 13 characters long.")
            elif partner.mobile and (partner.mobile[:2] != '92' or len(partner.mobile) != 12):
                raise ValidationError("Mobile number must start with '92' and should be exactly 12 characters long.")