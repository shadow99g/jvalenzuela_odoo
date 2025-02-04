from odoo import models, fields, api
import base64
import logging
import time

_logger = logging.getLogger(__name__)


class Account_12_13(models.TransientModel):
    _name = "libreria.account_12_13"
    _description = "Cuenta_12_13"

    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')
    txt_filename = fields.Char('filename', readonly=True)
    txt_binary = fields.Binary('file', readonly=True)

    @api.multi
    def generate_file(self):
        # modelo a buscar
        # ('dummy_account_id.code', 'like', 121100
        # dominio = ([('line_ids.account_id.code', 'ilike', '121100')])
        # Filtro
        lst_account_move_line = self.env['account.move'].search([('line_ids.account_id.code', 'ilike', '121100')])

        # variables creadas
        content_txt = ""
        estado_ope = ""
        _catalogo = ""
        _fec_per = ""
        _resid = ""
        _FecDoc = ""
        _fact = "INV"
        _refe = "POS"
        _sinFact = ""

        # Iterador
        for line in lst_account_move_line:

            # Catalogo
            if line.partner_id.catalog_06_id.code:
                _catalogo = line.partner_id.catalog_06_id.code

            # fecha del documento
            # if line.invoice_id.date_document:
            #     _fec_per = line.invoice_id.date_document

            # residual - importe adeudado
            for res in line.line_ids:
                if res.invoice_id.residual:
                    _resid = res.invoice_id.residual
                # for res1 in res.invoice_id:
                #     if res1.residual:
                #         _resid = res1.residual

                # si no hay factura   ref
            for refer in line.line_ids:
                # Referencia tiene POS
                if refer.ref == _refe:  # si en referencia es igual a POS
                    # if refer.ref:  # Lib Mayor (de Auditoria) / As. Cont. / Cta. 12 / As. Cont. / Referencia
                    _sinFact = refer.move_id.ref
                if refer.ref == _fact:  # si en referencia es igual a INV
                    # if refer.ref == _ref: # Lib Mayor (de Auditoria) / As. Cont. / Cta. 12 / Factura / Fech. Doc
                    _FecDoc = refer.invoice_id.date_document.strftime("%d%m%Y")

                # if fec_Doc == _fact:
                #     _sinFact = refer.date_document.strftime("%d%m%Y")
                # else:
                #     _sinFact = refer.ref

            # Estado de operacion
            if line.create_date.strftime("%m%Y") == time.strftime("%m%Y"):
                estado_ope = "1"
            else:
                if line.create_date.strftime("%Y") != time.strftime("%Y"):
                    estado_ope = "8"
                else:
                    if int(time.strftime("%Y")) == int(time.strftime("%Y")) - 2:
                        estado_ope = "9"
                    else:
                        estado_ope = "1"

            txt_line = "%s|%s|%s|%s|%s|%s|%s|%s|%s" % (
                line.create_date.strftime("%Y%m%d") or '',  # 1 Periodo- Fecha contable
                line.name or '',  # 2 ASIENTO CONTABLE (nombre del asiento ... referencia ya no)
                line.x_studio_field_fwlP9 or '',  # 3 Asiento contable _ ID
                _catalogo or '',  # 4 ID - RUC
                line.partner_id.vat or '',  # 5 Tipo de Doc. Identidad - RUC, enteros
                line.partner_id.registration_name or '',  # 6 Nombre de la empresa
                _FecDoc or _sinFact,  # 7 Referencia (si no tiene factura) - Fecha de doc. (si tiene factura)
                _resid or '',  # 8 importe adeudado
                estado_ope or '',
            )

            # Agregamos la linea al TXT
            content_txt = content_txt + "" + txt_line + "\r\n"

        self.write({
            'state': 'get',
            'txt_binary': base64.b64encode(content_txt.encode('ISO-8859-1')),
            'txt_filename': "Cuenta_12_13.txt"
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cuenta_12_13',
            'res_model': 'libreria.account_12_13',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new'
        }
