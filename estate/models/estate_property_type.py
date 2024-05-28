from odoo import fields, models, _


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', )
    offer_count = fields.Integer(compute="_compute_offer_count")

    # compute methods
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.mapped('offer_ids'))

    # actions
    def action_view_offers(self):
        return {
            "name": _("Related Offers"),
            "type": 'ir.actions.act_window',
            "view_mode": "tree,form",
            "res_model": 'estate.property.offer',
            "target": 'current',
            "domain": [('property_type_id', '=', self.id)],
            "context": {
                "default_property_type_id": self.id
            }
        }
