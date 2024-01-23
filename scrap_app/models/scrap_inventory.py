from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapDesktop(models.Model):
    _name = "scrap.inventory"
    _description = "showing the inventory scrap"
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
        store=True,
        compute="compute_ytd",
    )
    scrap_inventory_date = fields.Date(
        string="collected Date", default=fields.Datetime.now
    )
    scrap_address = fields.Char(string="Address", required=True)

