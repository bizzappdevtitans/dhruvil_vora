from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ScrapSelling(models.Model):
    _name = "scrap.selling"
    _description = "showing the selling scrap"
    _rec_name = "scrap_category"
    # _inherit = "scrap.category"
    scrap_price = fields.Float(
        string="Price", digits=(5, 1), required=True, default=1.0
    )
    scrap_category = fields.Many2one("scrap.category", string="category")
    scrap_quantity = fields.Float(
        string="Quantity",
        digits=(2, 1),
        default=1.0,
        required=True,
    )
    selling_to_inventory_count = fields.Float(
        string="Inventory", readonly=True, compute="_compute_show_quantity"
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

    def name_get(self):
        result = []
        for rec in self:
            result.append(
                (
                    rec.id,
                    "%s / %s"
                    % (rec.scrap_buyer_name, rec.scrap_category.scrap_category_name),
                )
            )

        return result

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
        res = super(ScrapSelling, self).read(vals)
        print(res)
        return res

    @api.onchange(
        "scrap_category", "scrap_quantity", "scrap_price", "scrap_total_price"
    )
    def onchange_scrap_price(self):
        self.scrap_total_price = self.scrap_price * self.scrap_quantity
        self._compute_show_quantity()

    @api.depends("selling_to_inventory_count")
    def check_inventory(self):
        if self.scrap_quantity > self.selling_to_inventory_count:
            raise ValidationError("Seeling quanity can't be greater than inventory")

    @api.constrains("scrap_quantity")
    def checking_quantity(self):
        if self.scrap_quantity <= 0.0 or 0:
            raise ValidationError("quanity should be greater than 0 ")
        sell_date = fields.Date.from_string(self.scrap_selling_date)
        today = fields.Date.from_string(fields.Datetime.now())
        if sell_date > today:
            raise ValidationError(("Please Enter appropiate dates."))

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

        self.selling_to_inventory_count = cat_name.current_scrap_quantity

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

    @api.constrains("scrap_category")
    def sub_inventory(self):
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
                if cat_name.current_scrap_quantity < self.scrap_quantity:
                    raise ValidationError(
                        "Selling quantity can't be more than inventory"
                    )
                elif cat_name.current_scrap_quantity > self.scrap_quantity:
                    cat_name.current_scrap_quantity = (
                        cat_name.current_scrap_quantity - self.scrap_quantity
                    )
