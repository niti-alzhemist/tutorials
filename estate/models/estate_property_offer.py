from dateutil.relativedelta import relativedelta

from odoo import fields, api, models
from datetime import date


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

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
