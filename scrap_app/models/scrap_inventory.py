from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapInventory(models.Model):
    _name = "scrap.inventory"
    _description = "showing the inventory scrap"
    _rec_name = "scrap_inventory_category"
    scrap_price = fields.Float(string="Scrap Price", digits=(2, 1))
    # scrap_category = fields.Many2one(
    #     "scrap.category", string="Scrap category", required=True, default="iron"
    # )
    scrap_inventory_category = fields.Char(string="Category")
    current_scrap_quantity = fields.Float(
        string="Scrap Quantity", digits=(2, 1), default=0
    )
    total_number_of_category = fields.Integer(string="total", default=0)
    scrap_total_price = fields.Float(
        string="Total price",
        digits=(2, 1),
        store=True,
    )
    scrap_inventory_date = fields.Date(string="Date", default=fields.Datetime.now)
