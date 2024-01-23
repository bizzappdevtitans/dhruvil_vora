from odoo import fields, models, api
from odoo.exceptions import ValidationError


class scrapapp_product(models.Model):
    _name = "scrapapp_product.products"
    _description = "product of product"
    _rec_name = "scrapapp_product_name"
    scrapapp_product_name = fields.Char("product name", required=True, size=50)
    scrapapp_product_price = fields.Float(
        string="product Price", digits=(2, 1), required=True
    )
    scrapapp_product_image = fields.Image(string="product Image")
    # scrapapp_product_priority = fields.Html(string="priority")

    product_count = fields.Integer(
        string="product Count", compute="compute_product_count"
    )

    def compute_product_count(self):
        for res in self:
            product_count = self.env["scrapapp_product.products"].search_count(
                [("id", "=", res.id)]
            )
            res.product_count = product_count
