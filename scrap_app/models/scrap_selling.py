from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class Scrapselling(models.Model):
    _name = "scrap.selling"
    _description = "showing the collected scrap"
    _rec_name = "scrap_selling_seq"
    scrap_buyer_name = fields.Char("Seller name", required=True)

    scrap_total_quantity = fields.Float(
        string="Quantity",
        digits=(10, 1),
    )
    scrap_total_price = fields.Float(string="Total price", digits=(15, 1))
    selling_to_inventory_count = fields.Float(string="Inventory", readonly=True)
    scrap_selling_seq = fields.Char(
        string="selling id",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
    )
    scrap_selling_state = fields.Selection(
        [
            ("in_process", "In Process"),
            ("confirm", "Confirmed"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="in_process",
        readonly=True,
    )
    scrap_selling_date = fields.Date(
        string="Collected Date", default=fields.Datetime.now
    )
    scrap_address = fields.Char(string="Address", required=True)

    scrap_selling_payment = fields.Selection(
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
        "scrap.items", "scrap_selling_id", string="Scraps values"
    )

    @api.model
    def create(self, vals):
        if vals.get("scrap_selling_seq", _("New")) == _("New"):
            vals["scrap_selling_seq"] = self.env["ir.sequence"].next_by_code(
                "scrap.selling"
            ) or _("New")
            res = super(Scrapselling, self).create(vals)
            return res

    def write(self, vals):
        self.parameters_for_validation(vals)
        return super(Scrapselling, self).write(vals)

    def unlink(self):
        for record in self:
            if record.scrap_selling_state == "confirm":
                raise UserError(_("record can't be deleted after Confirmed!!"))
            else:
                return super(Scrapselling, self).unlink()

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
                if update_value.current_scrap_quantity < 0:
                    raise ValidationError(
                        "You can't sell {} because it is only {} left".format(
                            category_name, update_value.current_scrap_quantity
                        )
                    )
                else:
                    update_value.current_scrap_quantity -= category_quantity

        self.scrap_selling_state = "confirm"
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

    #     self.selling_to_inventory_count = cat_name.current_scrap_quantity

    def selling_to_inventory(self):
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

    def make_payment_from_selling(self):
        print("payment")
        # self.scrap_selling_payment = "paid"

    def cancel_selling(self):
        if self.scrap_selling_state == "in_process":
            self.scrap_selling_payment = "cancel"
            self.scrap_selling_state = "cancel"
        elif self.scrap_selling_state == "collected":
            raise ValidationError("Record can't be deleted after selling!")

    def Confirm_selling(self):
        if True:
            self.add_inventory()

    # uploaded earlier will delete after the review of code
    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         result.append(
    #             (
    #                 rec.id,
    #                 "%s "
    #                 % (rec.scrap_buyer_name),
    #             )
    #         )

    #     return result

    @api.model
    def name_search(
        self,
        name,
        args=None,
        operator="=",
        limit=100,
        name_get_uid=None,
    ):
        print("was in this name_search ")
        args = args or []

        domain = []
        if name:
            domain = [
                "|",
                ("scrap_buyer_name", operator, name),
                ("scrap_category", operator, name),
            ]

        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    def read(self, vals):
        res = super(Scrapselling, self).read(vals)
        return res

    def selling_to_inventory(self):
        mode_of_view = ""
        id_res = 0
        value = self.env["scrap.inventory"].search_read([], ["id"])
        print("value is this ", value)
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
