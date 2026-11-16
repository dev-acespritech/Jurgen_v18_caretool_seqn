from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_event_journal(self):
        """Return (or create) the dedicated Event invoice journal for this company."""
        self.ensure_one()
        Journal = self.env['account.journal'].sudo()
        journal = Journal.search([('code', '=', 'EVINV'),
            ('type', '=', 'sale'),
            ('company_id', '=', self.company_id.id),
        ], limit=1)
        if not journal:
            journal = Journal.create({
                'name': 'Event Invoices',
                'code': 'EVINV',
                'type': 'sale',
                'company_id': self.company_id.id,
            })
        return journal

    def _post(self, soft=True):
        for move in self:
            if move.move_type != 'out_invoice' or move.state != 'draft':
                continue
            sale_lines = move.invoice_line_ids.sale_line_ids
            if sale_lines and any(l.event_id or l.event_ticket_id for l in sale_lines):
                journal = move._get_event_journal()
                if move.journal_id != journal:
                    move.journal_id = journal
        return super()._post(soft=soft)