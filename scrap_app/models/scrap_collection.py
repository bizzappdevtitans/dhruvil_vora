from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ScrapCollection(models.Model):
    _name = "scrap.collection"
    _description = "showing the collected scrap"
    _rec_name = "scrap_collection_seq"
    scrap_seller_name = fields.Char("Seller name")
    scrap_price = fields.Float(string="Scrap Price", digits=(5, 1))
    scrap_category = fields.Many2one("scrap.category", string="category")

    scrap_quantity = fields.Float(
        string="Quantity",
        digits=(10, 1),
        default=1.0,
    )
    scrap_total_price = fields.Float(string="Total price", digits=(15, 1))
    collection_to_inventory_count = fields.Float(
        string="Inventory", readonly=True, compute="_compute_show_quantity"
    )
    scrap_collection_seq = fields.Char(
        string="Collection id",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
    )
    scrap_collection_state = fields.Selection(
        [
            ("in_process", "In Process"),
            ("collected", "Collected"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="in_process",
        # readonly=True,
    )
    scrap_collection_date = fields.Date(
        string="Collected Date", default=fields.Datetime.now
    )
    scrap_address = fields.Char(string="Address", required=True)

    scrap_collection_payment = fields.Selection(
        [
            ("not_paid", "Not Paid"),
            ("paid", "Paid"),
            ("cancel", "Cancelled"),
        ],
        string="Payment Status",
        default="not_paid",
        readonly=True,
    )
    add_scrap_lines = fields.One2many(
        "scrap.collection_items", "scrap_collection_id", string="Scraps values"
    )

    @api.model
    def create(self, vals):
        if vals.get("scrap_collection_seq", _("New")) == _("New"):
            vals["scrap_collection_seq"] = self.env["ir.sequence"].next_by_code(
                "scrap.collection"
            ) or _("New")
            res = super(ScrapCollection, self).create(vals)
            return res

    def write(self, vals):
        total_value = self.env["scrap.collection_items"].search(
            [
                (
                    "scrap_collection_id",
                    "=",
                    self.scrap_collection_seq,
                )
            ]
        )
        print(
            "total value jhgfdjklgfdjgfjkfjjjfgfljghjfdhgjkdfgbnjkfdngbgb", total_value
        )
        total_price = 0
        total_qty = 0
        for index in total_value:
            total_price += index.scrap_collection_total_price
            total_qty += index.scrap_collection_quantity
        self.scrap_total_price = total_price
        print("jkfdhgjkfdnfdgnfd,mgnfd,mfgmgfdnfdg", self.scrap_total_price)
        self.scrap_quantity = total_qty

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

    def make_payment_from_collection(self):
        print("payment")

    def cancel_collection(self):
        if True:
            if self.scrap_collection_state == "in_process":
                self.scrap_collection_payment = "cancel"
                self.scrap_collection_payment = "cancel"
            elif self.scrap_collection_state == "collected":
                raise ValidationError("Record can't be deleted after collection!")
