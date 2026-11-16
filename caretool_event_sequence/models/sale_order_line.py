from odoo import models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines.mapped('order_id').sudo()._apply_event_quotation_sequence()
        return lines

    def write(self, vals):
        res = super().write(vals)
        if 'product_id' in vals:
            self.mapped('order_id').sudo()._apply_event_quotation_sequence()
        return res