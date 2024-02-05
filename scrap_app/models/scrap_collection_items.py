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

    @api.constrains("scrap_collection_quantity")
    def checking_quantity(self):
        value = self.scrap_collection_quantity
        if value <= 0:
            raise ValidationError("Do not enter value less or equal to 0")

    @api.model
    def create(self, vals):
        print(vals)
        if "scrap_collection_category" in vals:
            category_name = (
                self.env["scrap.category"]
                .browse(vals.get("scrap_collection_category"))
                .scrap_category_name
            )
            category_quantity = vals.get("scrap_collection_quantity")
            add_inventory = {
                "scrap_inventory_category": category_name,
                "current_scrap_quantity": category_quantity,
                "update_value": "add",
            }
            self.env["scrap.inventory"].update_the_inventory(add_inventory)
        res = super(Scrap_Collection_items, self).create(vals)
        return res

    @api.model
    def write(self, vals):
        # print("vals",vals)
        # # for index in self:
        # #     scrap_category = index.scrap_collection_category.scrap_category_name
        # #     scrap_quantity = index.scrap_collection_quantity

        # print("self", self)
        return super(Scrap_Collection_items, self).write(vals)


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
