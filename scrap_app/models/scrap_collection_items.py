from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Scrap_Collection_items(models.Model):
    _name = "scrap.collection_items"
    _description = "showing the collected scrap"
    _rec_name = "scrap_collection_id"
    scrap_collection_id = fields.Many2one(
        "scrap.collection", string="collection id", ondelete="cascade"
    )
    scrap_collection_category = fields.Many2one("scrap.category", string="category")
    scrap_collection_price = fields.Float(
        string="Scrap Price", digits=(5, 1), required=True
    )
    scrap_collection_total_price = fields.Float(
        string="Total price",
        digits=(15, 1),
        required=True,
    )
    scrap_collection_quantity = fields.Float(
        string="Quantity",
        digits=(10, 1),
        default=1.0,
        required=True,
    )

    @api.onchange(
        "scrap_collection_category",
        "scrap_collection_quantity",
        "scrap_collection_price",
        "scrap_collection_total_price",
    )
    def onchange_scrap_price(self):
        self.scrap_collection_price = (
            self.scrap_collection_category.scrap_category_price
        )
        self.scrap_collection_total_price = (
            self.scrap_collection_category.scrap_category_price
            * self.scrap_collection_quantity
        )
