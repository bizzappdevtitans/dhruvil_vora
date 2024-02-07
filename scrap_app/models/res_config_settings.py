# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    payement_in_days = fields.Char(
        string="Payment Done in ( Days )",
        config_parameter="scrap_app.no_of_days_for_payment",
    )
