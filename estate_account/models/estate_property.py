from odoo import models, fields, Command


class EstateProperty(models.Model):
    _inherit = ['estate.property']

    def action_sold(self):
        res = super().action_sold()
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        for record in self:
            self.env['account.move'].create({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": 6 / 100 * record.selling_price

                    }),
                    Command.create({
                        "name": "administrative fees",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ]
            })

        return res
