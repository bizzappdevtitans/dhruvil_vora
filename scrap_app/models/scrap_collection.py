from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapDesktop(models.Model):
    _name = "scrap.collection"
    _description = "showing the collected scrap"
    _rec_name = "scrap_category"
    scrap_seller_name = fields.Char("Scrap Seller name")
    scrap_price = fields.Float(string="Scrap Price", digits=(2, 1), required=True)
    scrap_category = fields.Many2one(
        "scrap.category", string="Scrap category", required=True
    )
    scrap_quantity = fields.Float(
        string="Scrap Quantity",
        digits=(2, 1),
        default=1.0,
        required=True,
    )
    scrap_total_price = fields.Float(
        string="Total price",
        digits=(2, 1),
        required=True,
    )
    scrap_collection_date = fields.Date(
        string="collected Date", default=fields.Datetime.now
    )
    scrap_address = fields.Char(string="Address", required=True)

    @api.onchange(
        "scrap_category", "scrap_quantity", "scrap_price", "scrap_total_price"
    )
    def onchange_scrap_price(self):
        # if self.scrap_category:
        #     if self.scrap_category.scrap_category_price:

        self.scrap_price = self.scrap_category.scrap_category_price
        self.scrap_total_price = (
            self.scrap_category.scrap_category_price * self.scrap_quantity
        )

    @api.constrains("scrap_quantity", "scrap_category")
    def checking_quantity(self):
        if self.scrap_quantity <= 0:
            raise ValidationError("quanity should be greater than 0 ")
        for category_name in self.env["scrap.category"]:
            if category_name.scrap_category_name is not self.scrap_category:
                raise ValidationError("Please choose from the category")

    @api.constrains("scrap_category")
    def add_inventory(self):
        for res in self:
            inventory_of_scrap = self.env["scrap.inventory"]
            category = inventory_of_scrap.search_count(
                [
                    (
                        "scrap_inventory_category",
                        "=",
                        res.scrap_category.scrap_category_name,
                    )
                ]
            )
            vals = {
                "scrap_inventory_category": res.scrap_category.scrap_category_name,
                "current_scrap_quantity": self.scrap_quantity,
            }
            if category == 0:
                self.env["scrap.inventory"].create(vals)
            elif category > 0:
                cat_name = inventory_of_scrap.search(
                    [
                        (
                            "scrap_inventory_category",
                            "=",
                            res.scrap_category.scrap_category_name,
                        )
                    ]
                )
                cat_name.current_scrap_quantity = (
                    cat_name.current_scrap_quantity + self.scrap_quantity
                )
