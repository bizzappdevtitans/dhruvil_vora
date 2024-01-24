from odoo import fields, models, api
from odoo.exceptions import ValidationError


class productDesktop(models.Model):
    _name = "scrapapp_product.category"
    _description = "category of product"
    _rec_name = "scrapapp_product_category_name"
    scrapapp_product_category_name = fields.Char("product Category name", required=True)
    # scrapapp_product_category_price = fields.Float(string="product Price", digits=(2, 1))
    scrapapp_product_category_image = fields.Image(string="product Image")


_sql_constraints = [
    (
        "unique_scrapapp_product_category_name",
        "unique(scrapapp_product_category_name)",
        "Category name should be unique !",
    ),
]
