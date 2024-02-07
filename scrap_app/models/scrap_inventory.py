from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ScrapInventory(models.Model):
    _name = "scrap.inventory"
    _description = "showing the inventory scrap"
    _rec_name = "scrap_inventory_category"
    # scrap_price = fields.Float(string="Price", digits=(2, 1))
    scrap_inventory_category = fields.Char(string="Category")
    current_scrap_quantity = fields.Float(string="Quantity", digits=(5, 1), default=0)
    # total_number_of_category = fields.Integer(string="total", default=0)
    # scrap_total_price = fields.Float(
    #     string="price",
    #     digits=(2, 1),
    #     store=True,
    # )
    # scrap_inventory_date = fields.Date(string="Date", default=fields.Datetime.now)

    @api.depends("scrap_inventory_category")
    def check_unique_name(self):
        company_ids = self.search([])
        value = [x.name.lower() for x in company_ids]
        if self.name and self.name.lower() in value:
            raise ValidationError(_("The combination is already Exist"))

    _sql_constraints = [
        (
            "unique_name",
            "unique(scrap_inventory_category)",
            "Please choose a unique name !",
        )
    ]
