from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _name = "scrapapp_product.category"
    _description = "category of product"
    _rec_name = "scrapapp_product_category_name"
    scrapapp_product_category_name = fields.Char("Category name", required=True)
    scrapapp_product_category_image = fields.Image(string="Image")


_sql_constraints = [
    (
        "unique_scrapapp_product_category_name",
        "unique(scrapapp_product_category_name)",
        "Category name should be unique !",
    ),
]
