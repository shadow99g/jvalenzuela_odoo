from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class first_report_method(models.AbstractModel):
    _name = 'report.account.move.line'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']

        report = report_obj._get_report_from_name('account.move.line')

        docargs = {
        }

        return report_obj.render('account.move.line', docargs)

    def _getLines(self):
        res = []
        lst_account_move_line = self.env['account.move.line'].search([])
        for item in lst_account_move_line:
            _logger.info('Creacion de listado')
            # campos listos
            res.append({
                'id': item,
                'date': item.date,
                'name': item.move_id.name,
                'debit': item.debit,
                'credit': item.credit,
            })
        return res
