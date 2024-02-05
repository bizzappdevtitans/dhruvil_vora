from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ScrapCollection(models.Model):
    _name = "scrap.collection"
    _description = "showing the collected scrap"
    _rec_name = "scrap_collection_seq"
    scrap_seller_name = fields.Char("Seller name", required=True)

    scrap_total_quantity = fields.Float(
        string="Quantity",
        digits=(10, 1),
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
            ("confirm", "Confirmed"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="in_process",
        readonly=True,
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
        "scrap.items", "scrap_collection_id", string="Scraps values"
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
        self.parameters_for_validation(vals)
        return super(ScrapCollection, self).write(vals)

    def unlink(self):
        for record in self:
            if record.scrap_collection_state == "confirm":
                raise UserError(_("record can't be deleted after Confirmed!!"))
            else:
                return super(ScrapCollection, self).unlink()

    # update and write are same
    # def update(self, values):
    #     """Update the records in ``self`` with ``values``."""
    #     for record in self:
    #         for name, value in values.items():
    #             record[name] = value
    #             print(record[name])
    def parameters_for_validation(self, vals):
        if "scrap_seller_name" in vals:
            print("nothiingf")
            para = self.env["ir.config_parameter"].get_param("min_name_length", "")
            if len(vals["scrap_seller_name"]) < int(para):
                raise ValidationError("Enter Proper name ")

    def add_inventory(self):
        total_quantity = 0
        total_value = 0
        for index in self.add_scrap_lines:
            category_name = index.scrap_item_category.scrap_category_name
            category_quantity = index.scrap_item_quantity
            category_total = index.scrap_item_total_price
            category_num = self.env["scrap.inventory"].search_count(
                [("scrap_inventory_category", "=", category_name)]
            )
            total_quantity += category_quantity
            total_value += category_total
            if category_num == 0:
                self.env["scrap.inventory"].create(
                    {
                        "scrap_inventory_category": category_name,
                        "current_scrap_quantity": category_quantity,
                    }
                )
            elif category_num == 1:
                update_value = self.env["scrap.inventory"].search(
                    [
                        (
                            "scrap_inventory_category",
                            "=",
                            category_name,
                        )
                    ]
                )

                update_value.current_scrap_quantity += category_quantity

        self.scrap_collection_state = "confirm"
        self.scrap_total_quantity = category_quantity
        self.scrap_total_price = category_total

    # def _compute_show_quantity(self):
    #     for res in self:
    #         cat_name = self.env["scrap.inventory"].search(
    #             [
    #                 (
    #                     "scrap_inventory_category",
    #                     "=",
    #                     res.scrap_category.scrap_category_name,
    #                 )
    #             ]
    #         )

    #     self.collection_to_inventory_count = cat_name.current_scrap_quantity

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
        # self.scrap_collection_payment = "paid"

    def cancel_collection(self):
        if self.scrap_collection_state == "in_process":
            self.scrap_collection_payment = "cancel"
            self.scrap_collection_state = "cancel"
        elif self.scrap_collection_state == "collected":
            raise ValidationError("Record can't be deleted after collection!")

    def Confirm_collection(self):
        if True:
            self.add_inventory()
