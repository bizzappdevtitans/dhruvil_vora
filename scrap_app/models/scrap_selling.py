from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapDesktop(models.Model):
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
    scrap_address = fields.Char(string="Address", required=True)

    # @api.onchange("scrap_category", "scrap_quantity")
    # def onchange_scrap_price(self):
    #     # if self.scrap_category:
    #     #     if self.scrap_category.scrap_category_price:
    #     #self.scrap_price = self.scrap_category.scrap_category_price
    #     self.scrap_total_price = (
    #         self.scrap_price * self.scrap_quantity
    #     )
    # @api.multi
    @api.depends("scrap_price", "scrap_quantity")
    def _compute_ytd(self):
        self.scrap_total_price = self.scrap_price * self.scrap_quantity
