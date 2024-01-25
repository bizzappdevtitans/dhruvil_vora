from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapCollection(models.Model):
    _name = "scrap.collection"
    _description = "showing the collected scrap"
    _rec_name = "scrap_category"
    scrap_seller_name = fields.Char("Seller name")
    scrap_price = fields.Float(string="Scrap Price", digits=(2, 1), required=True)
    scrap_category = fields.Many2one(
        "scrap.category", string="category", required=True
    )
    scrap_quantity = fields.Float(
        string="Quantity",
        digits=(2, 1),
        default=1.0,
        required=True,
    )
    scrap_total_price = fields.Float(
        string="Total price",
        digits=(2, 1),
        required=True,
    )
    collection_to_inventory_count = fields.Float(
        string="Inventory", readonly=True, compute="_compute_show_quantity"
    )
    scrap_collection_state = fields.Selection(
        [
            ("collected", "Collected"),
            ("in_process", "In Process"),
            ("in_storage", "In Storage"),
        ],
        string="Status",
        default="collected",
    )
    scrap_collection_date = fields.Date(
        string="Collected Date", default=fields.Datetime.now
    )
    scrap_address = fields.Char(string="Address", required=True)

    @api.onchange(
        "scrap_category", "scrap_quantity", "scrap_price", "scrap_total_price"
    )
    def onchange_scrap_price(self):
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

    def _compute_show_quantity(self):
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

        self.collection_to_inventory_count = cat_name.current_scrap_quantity

    def collection_to_inventory(self):
        mode_of_view = ""
        id_res = 0
        value = self.env["scrap.inventory"].search([("id", ">", 0)])
        no_of_item = len(value)
        if no_of_item == 1:
            mode_of_view = "form"
            id_res = value[0].id
        else:
            mode_of_view = "tree,form,kanban"
            print("mode of view ", mode_of_view)
        return {
            "name": "Scrap Inventory",
            "res_model": "scrap.inventory",
            "view_id": False,
            "view_mode": mode_of_view,
            "res_id": id_res,
            "type": "ir.actions.act_window",
        }

    def make_payment(self):
        print("payment")
