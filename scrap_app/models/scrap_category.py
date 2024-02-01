from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ScrapCategory(models.Model):
    _name = "scrap.category"
    _description = "category of scrap"
    _rec_name = "scrap_category_name"
    scrap_category_sequence = fields.Integer(string="Sequence")
    scrap_category_name = fields.Char("Category name")
    scrap_category_price = fields.Float(string="Price", digits=(2, 1))
    scrap_category_image = fields.Image(string="Image")

