from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapSelling(models.Model):
    _name = "scrap.selling"
    _description = "showing the selling scrap"
    # scrap_name = fields.Char("Scrap name")
    _rec_name = "scrap_category"
    scrap_price = fields.Float(string="Scrap Price", digits=(2, 1), required=True)
    scrap_category = fields.Many2one("scrap.category", string="Scrap category")
    scrap_quantity = fields.Float(
        string="Scrap Quantity",
        digits=(2, 1),
        default=1.0,
        required=True,
    )
    selling_to_inventory_count = fields.Float(
        string="Inventory", readonly=True, compute="show_quantity"
    )
    scrap_buyer_name = fields.Char(string="Buyer name ", default="Scrap app")
    scrap_total_price = fields.Float(
        string="Total price",
        digits=(2, 1),
        required=True,
    )
    scrap_selling_date = fields.Date(
        string="collected Date", default=fields.Datetime.now
    )
    scrap_address = fields.Char(
        string="Address",
        required=True,
    )

    @api.onchange(
        "scrap_category", "scrap_quantity", "scrap_price", "scrap_total_price"
    )
    def onchange_scrap_price(self):
        # if self.scrap_category:
        #     if self.scrap_category.scrap_category_price:
        self.scrap_total_price = self.scrap_price * self.scrap_quantity

    @api.constrains("scrap_quantity")
    def checking_quantity(self):
        if self.scrap_quantity <= 0.0 or 0:
            raise ValidationError("quanity should be greater than 0 ")
        sell_date = fields.Date.from_string(self.scrap_selling_date)
        today = fields.Date.from_string(fields.Datetime.now())
        if sell_date > today:
            raise ValidationError(("Please Enter appropiate dates."))

    # for category_name in self.env["scrap.category"]:
    #     if category_name.scrap_category_name is not self.scrap_category:
    # raise ValidationError("Please choose from the category")

    # this depends is working ok but shows a different error for the list view

    # @api.depends("scrap_price", "scrap_quantity")
    # def compute_total(self):
    #     for total in self:
    #         total.scrap_total_price = total.scrap_price * total.scrap_quantity

    def show_quantity(self):
        for res in self:
            cat_name = self.env["scrap.inventory"].search(
                [
                    (
                        "scrap_inventory_category",
                        "=",
                        res.scrap_category.scrap_category_name,
                    )
                ]
            )
        self.selling_to_inventory_count = cat_name.current_scrap_quantity

    # def no_of_inventory_values(self):

    def selling_to_inventory(self):
        mode_of_view = ""
        for res in self:
            no_of_item = self.env["scrap.inventory"].search_count(
                [
                    (
                        "id",
                        ">",
                        0,
                    )
                ]
            )
            print("no_of_item")
            print(no_of_item)

        if no_of_item == 0 or no_of_item == 1:
            mode_of_view = "tree,form,kanban"
        else:
            mode_of_view = "form,tree,kanban"
            print("mode of view ", mode_of_view)
        return {
            "name": "Scrap Inventory",
            "res_model": "scrap.inventory",
            "view_id": False,
            "view_mode": "tree,form,kanban",
            # "domain": [("teacher_id", "=", self.id)],
            "type": "ir.actions.act_window",
        }

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
                    cat_name.current_scrap_quantity - self.scrap_quantity
                )
