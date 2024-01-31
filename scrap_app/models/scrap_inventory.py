from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapInventory(models.Model):
    _name = "scrap.inventory"
    _description = "showing the inventory scrap"
    _rec_name = "scrap_inventory_category"
    # scrap_price = fields.Float(string="Price", digits=(2, 1))
    scrap_inventory_category = fields.Char(string="Category")
    current_scrap_quantity = fields.Float(
        string="Quantity", digits=(5, 1), default=0
    )
    # total_number_of_category = fields.Integer(string="total", default=0)
    # scrap_total_price = fields.Float(
    #     string="price",
    #     digits=(2, 1),
    #     store=True,
    # )
    scrap_inventory_date = fields.Date(string="Date", default=fields.Datetime.now)
