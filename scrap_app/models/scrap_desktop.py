from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapDesktop(models.Model):
    _name = "scrap.desktop"
    _description = "showing models on the desktop"
    _rec_name = "desktop_value_name"
    desktop_value_name = fields.Char("Name")
    desktop_value_image = fields.Image(string="Image")
