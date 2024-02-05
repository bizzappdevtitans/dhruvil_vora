from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ScrapCollection(models.Model):
    _name = "scrap.collection"
    _description = "showing the collected scrap"
    _rec_name = "scrap_collection_seq"
    scrap_seller_name = fields.Char("Seller name")
    scrap_price = fields.Float(string="Scrap Price", digits=(5, 1))
    # scrap_category = fields.Many2one("scrap.category", string="category")

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
        for index in vals["add_scrap_lines"]:
            if index[2]:
                print("inner value ", index[1])
                collection_id = self.env["scrap.collection_items"].search(
                    [("id", "=", index[1])]
                )
                old_name = collection_id.scrap_collection_category.scrap_category_name
                old_quantity = collection_id.scrap_collection_quantity
                print("old name", old_name)
                print("old quantity", old_quantity)
                # new_name=index[2].get("")
                new_quantity = index[2].get("scrap_collection_quantity")
                print("new quantity", new_quantity)

                if new_quantity > old_quantity:
                    new_quantity -= old_quantity
                    self.env["scrap.inventory"].update_the_inventory(
                        {
                            "scrap_inventory_category": old_name,
                            "current_scrap_quantity": new_quantity,
                            "update_value": "add",
                        }
                    )
                elif new_quantity < old_quantity:
                    old_quantity-=new_quantity
                    self.env["scrap.inventory"].update_the_inventory(
                        {
                            "scrap_inventory_category": old_name,
                            "current_scrap_quantity": old_quantity,
                            "update_value": "sub",
                        }
                    )
        return super(ScrapCollection, self).write(vals)

    def unlink(self):
        if self.scrap_collection_state != "cancel":
            raise UserError(_("record can be only deleted after cancelling."))
        else:
            return super(ScrapCollection, self).unlink()

    # update and write are same
    # def update(self, values):
    #     """Update the records in ``self`` with ``values``."""
    #     for record in self:
    #         for name, value in values.items():
    #             record[name] = value
    #             print(record[name])

    def add_inventory(self):
        print("yes written")
        for index in self.add_scrap_lines:
            category_id = index.id
            category_name = index.scrap_collection_category.scrap_category_name
            category_quantity = index.scrap_collection_quantity
            category_num = self.env["scrap.inventory"].search_count(
                [("scrap_inventory_category", "=", category_name)]
            )
            if category_num == 0:
                self.env["scrap.inventory"].create(
                    {
                        "scrap_inventory_category": category_name,
                        "current_scrap_quantity": category_quantity,
                    }
                )
            elif category_num == 1:
                print("elif part")
                print("categiory id ", category_id)
                self.env["scrap.inventory"].browse(category_id).update(
                    {"current_scrap_quantity": 5}
                )

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

    def cancel_collection(self):
        if self.scrap_collection_state == "in_process":
            self.scrap_collection_payment = "cancel"
            self.scrap_collection_state = "cancel"
        elif self.scrap_collection_state == "collected":
            raise ValidationError("Record can't be deleted after collection!")
