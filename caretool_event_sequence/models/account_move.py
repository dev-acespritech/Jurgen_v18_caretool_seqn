from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_event_journal(self):
        """Return (or create) the dedicated Event invoice journal for this company."""
        self.ensure_one()
        Journal = self.env['account.journal'].sudo()
        journal = Journal.search([
            ('code', '=', 'EVINV'),
            ('type', '=', 'sale'),
            ('company_id', '=', self.company_id.id),
        ], limit=1)
        if not journal:
            journal = Journal.create({'name': 'Event Invoices',
                'code': 'EVINV',
                'type': 'sale',
                'company_id': self.company_id.id,
            })
        return journal

    def _is_event_invoice(self):
        self.ensure_one()
        if self.move_type != 'out_invoice':
            return False
        return any(l.event_id or l.event_ticket_id
                   for l in self.invoice_line_ids.sale_line_ids)

    def _post(self, soft=True):
        for move in self:
            if move.state != 'draft' or not move._is_event_invoice():
                continue
            journal = move._get_event_journal()
            if move.journal_id != journal:
                move.journal_id = journal
            # number comes from the editable sequence, only if not numbered yet
            if move.name in (False, '', '/'):
                name = self.env['ir.sequence'].sudo().next_by_code('account.invoice.event')
                if name:
                    move.name = name
        return super()._post(soft=soft)