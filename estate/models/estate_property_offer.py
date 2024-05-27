from dateutil.relativedelta import relativedelta

from odoo import fields, api, models, _
from datetime import date

from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _sql_constraints = [
        (
            "expected_price_strictly_positive",
            "CHECK (price > 0)",
            "Offer price must be strictly positive.",
        ),
    ]

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    validity = fields.Integer(default=7)

    # Foreign key
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # Related fields
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", stored=True
    )

    # Compute fields
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    # Compute methods
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            use_date = record.create_date.date() if record.create_date else date.today()
            record.date_deadline = use_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            use_date = record.create_date.date() if record.create_date else date.today()
            record.validity = (record.date_deadline - use_date).days

    # Public method
    def action_accept_offer(self):
        if "sold" in self.mapped("property_id.state"):
            raise UserError(_("Cannot edit offer from SOLD property"))
        if "accepted" in self.mapped("property_id.offer_ids.status"):
            raise UserError(_("Only one offer can be accepted for one property"))

        self.write({"status": "accepted"})
        return self.property_id.write(
            {
                "selling_price": self.price,
                "buyer_id": self.partner_id,
            }
        )

    def action_reject_offer(self):
        if "sold" in self.mapped("property_id.state"):
            raise UserError(_("Cannot edit offer from SOLD property"))
        if "accepted" in self.status:
            self.property_id.write({"selling_price": 0, "buyer_id": False})

        return self.write({"status": "refused"})
