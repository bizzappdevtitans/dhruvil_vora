from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapDesktop(models.Model):
    _name = "scrap.category"
    _description = "category of scrap"
    _rec_name = "scrap_category_name"
    scrap_category_name = fields.Char("Scrap Category name")
    scrap_category_price = fields.Float(string="Scrap Price", digits=(2, 1))
    scrap_category_image = fields.Image(string="Scrap Image")
