#-*- coding:utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_event_sequence_applied = fields.Boolean(copy=False)
    is_event_order_sequence_applied = fields.Boolean(copy=False)

    def _has_event_lines(self):
        self.ensure_one()
        return any(
                line.event_id or line.event_ticket_id
                for line in self.order_line)

    def _apply_event_quotation_sequence(self):
        for order in self:
            if order.is_event_sequence_applied or order.state not in ('draft', 'sent'):
                continue
            if order._has_event_lines():
                name = self.env['ir.sequence'].sudo().next_by_code('sale.quotation.event')
                if name:
                    order.write({'name': name, 'is_event_sequence_applied': True})

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        orders.filtered('order_line')._apply_event_quotation_sequence()
        return orders

    def write(self, vals):
        res = super().write(vals)
        if 'order_line' in vals:
            self._apply_event_quotation_sequence()
        return res

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.is_event_order_sequence_applied:
                continue
            if order._has_event_lines():
                name = self.env['ir.sequence'].sudo().next_by_code('sale.order.event')
                if name:
                    order.write({'name': name, 'is_event_order_sequence_applied': True})
        return res
