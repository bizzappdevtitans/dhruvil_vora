from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapDesktop(models.Model):
    _name = "scrap.desktop"
    _description = "showing models on the desktop"
    desktop_value_name = fields.Char("Desktop value name ")
    desktop_value_image = fields.Image(string="Desktop image")
