from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapSelling(models.Model):
    _name = "scrap.selling"
    _description = "showing the selling scrap"
    # scrap_name = fields.Char("Scrap name")
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
    scrap_seller_name = fields.Char(string="Seller name ")
    scrap_total_price = fields.Float(
        string="Total price",
        digits=(2, 1),
        required=True,
    )
    scrap_selling_date = fields.Date(
        string="collected Date", default=fields.Datetime.now
    )
    scrap_address = fields.Char(
        string="Address", required=True, compute="compute_address"
    )

    # @api.onchange("scrap_category", "scrap_quantity")
    # def onchange_scrap_price(self):
    #     # if self.scrap_category:
    #     #     if self.scrap_category.scrap_category_price:
    #     #self.scrap_price = self.scrap_category.scrap_category_price
    #     self.scrap_total_price = (
    #         self.scrap_price * self.scrap_quantity
    #     )


# this depends is working ok but shows a different error for the list view

# @api.depends("scrap_total_price", "scrap_price", "scrap_quantity")
# def compute_ytd(self):
#     self.scrap_total_price = self.scrap_price * self.scrap_quantity

# @api.constrains("scrap_quantity")
# def checking_quantity(self):
#     if self.scrap_quantity <= 0:
#         raise ValidationError("quanity should be greater than 0 ")
#     # for category_name in self.env["scrap.category"]:
#     #     if category_name.scrap_category_name is not self.scrap_category:
#         raise ValidationError("Please choose from the category")


@api.constrains("scrap_quantity", "scrap_category")
def checking_quantity(self):
    if self.scrap_quantity <= 0:
        raise ValidationError("quanity should be greater than 0 ")
    for category_name in self.env["scrap.category"]:
        if category_name.scrap_category_name is not self.scrap_category:
            raise ValidationError("Please choose from the category")
