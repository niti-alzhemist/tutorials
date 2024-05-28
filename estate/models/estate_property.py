from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _sql_constraints = [
        (
            "expected_price_strictly_positive",
            "CHECK (expected_price > 0)",
            "Expected price must be strictly positive.",
        ),
        (
            "selling_price",
            "CHECK (selling_price >= 0)",
            "Selling price must be positive.",
        ),
    ]
    _order = "id desc"

    def _default_availability_date(self):
        return fields.Date.add(fields.Date.today(), months=3)

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=_default_availability_date)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    # ----------------- Foreign key -----------------
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner")
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag")

    # Compute fields
    total_area = fields.Float(string="Total area SQM", compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    # ----------------- Compute method -----------------
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_orientation = "north"
                record.garden_area = 10
            else:
                record.garden_orientation = ""
                record.garden_area = 0

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        for record in self:
            if record.date_availability < fields.Date.today():
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": "Date availability must be greater than or equal today",
                    }
                }

    # ----------------- Constraints -----------------
    @api.constrains("selling_price", "expected_price")
    def _constraint_selling_price(self):
        for record in self:
            ninty_percent_value = 90 / 100 * record.expected_price
            if (
                    not float_compare(
                        record.selling_price, ninty_percent_value, precision_digits=0.01
                    )
                        > 0
                    and record.selling_price != 0
            ):
                raise ValidationError(
                    _(
                        "The selling price must be greater than %.2f"
                        % ninty_percent_value
                    )
                )

    # ----------------- action methods -----------------
    def action_sold(self):
        for record in self:
            if "canceled" in record.offer_ids.mapped("status"):
                raise UserError(_("Cannot sold the canceled property"))
            if len(record.mapped("offer_ids")) <= 0:
                raise UserError(_("There are no offers with this property"))

            return record.write({"state": "sold"})

    def action_cancel(self):
        for record in self:
            if "sold" in record.mapped("state"):
                raise UserError(_("Cannot cancel the sold property"))

            return record.write({"state": "canceled"})
