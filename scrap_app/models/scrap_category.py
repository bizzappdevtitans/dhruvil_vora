from odoo import api, fields, models


class ScrapCategory(models.Model):
    _name = "scrap.category"
    _description = "category of scrap"
    _rec_name = "scrap_category_name"
    scrap_category_sequence = fields.Integer(string="Sequence")
    scrap_category_name = fields.Char("Category name")
    scrap_category_price = fields.Float(string="Price", digits=(2, 1))
    scrap_category_image = fields.Image(string="Image")

    @api.model
    def create(self, vals):
        add_inventory = {
            "scrap_inventory_category": vals["scrap_category_name"],
            "current_scrap_quantity": 0.0,
        }
        self.env["scrap.inventory"].create(add_inventory)
        res = super(ScrapCategory, self).create(vals)
        return res
