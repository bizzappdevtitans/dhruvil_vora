from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ScrapItems(models.Model):
    _name = "scrap.items"
    _description = "showing the collected scrap"
    _rec_name = "scrap_item_category"
    scrap_collection_id = fields.Many2one(
        "scrap.collection",
        string="id",
        ondelete="cascade",
    )
    scrap_selling_id = fields.Many2one(
        "scrap.selling",
        string="id",
        ondelete="cascade",
    )
    scrap_item_category = fields.Many2one("scrap.category", string="category")
    scrap_item_price = fields.Float(string="Scrap Price", digits=(5, 1), required=True)
    scrap_item_total_price = fields.Float(
        string="Total price",
        digits=(15, 1),
        required=True,
    )
    scrap_item_quantity = fields.Float(
        string="Quantity",
        digits=(10, 1),
        default=1.0,
        required=True,
    )

    @api.constrains("scrap_item_quantity")
    def checking_quantity(self):
        value = self.scrap_item_quantity
        if value <= 0:
            raise ValidationError(_("Do not enter value less or equal to 0"))

    @api.model
    def create(self, vals):
        res = super(ScrapItems, self).create(vals)
        return res

    @api.model
    def write(self, vals):
        return super(ScrapItems, self).write(vals)

    @api.onchange(
        "scrap_item_category",
        "scrap_item_quantity",
        "scrap_item_price",
        "scrap_item_total_price",
    )
    def onchange_scrap_price(self):
        self.scrap_item_price = self.scrap_item_category.scrap_category_price
        self.scrap_item_total_price = (
            self.scrap_item_category.scrap_category_price * self.scrap_item_quantity
        )
