from odoo import models, fields, api
import base64
import logging
import time

_logger = logging.getLogger(__name__)


class Account_17(models.TransientModel):
    _name = "libreria.account_17"
    _description = "Cuenta_17"

    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')
    txt_filename = fields.Char('filename', readonly=True)
    txt_binary = fields.Binary('file', readonly=True)

    @api.multi
    def generate_file(self):
        # filtro de fecha
        dominio = [('dummy_account_id.code', 'like', '171110')]

        # modelo a buscar
        lst_account_move_line = self.env['account.move'].search(dominio)

        # variables creadas
        content_txt = ""
        _debito=""
        _catalogo = ""
        _vat = ""
        cantidad = ""
        estado_ope =""

        # Iterador
        for line in lst_account_move_line:
            # _debito
            for imp in line.line_ids:
                if imp.debit:
                    _debito = imp.debit

            for imp1 in line.line_ids:
                if imp1.partner_id.catalog_06_id.code:
                    _catalogo = imp1.partner_id.catalog_06_id.code

            # _vat
            for imp2 in line.line_ids:
                if imp2.partner_id.vat:
                   _vat = imp2.partner_id.vat

            # _nombre
            for imp3 in line.line_ids:
                if imp3.partner_id.name:
                   _nombre = imp3.partner_id.name


            #8 total de monto a cobrar
            for p2 in line.line_ids:
                cantidad = sum(line.debit for line in line.line_ids)  # #8 Sumar la cantidad de monto a cobrar que haya

            #9

            if line.create_date.strftime("%m%Y") == time.strftime("%m%Y"):
                estado_ope = "01"
            else:
                if line.create_date.strftime("%Y") != time.strftime("%Y"):
                    estado_ope = "09"
                else:
                    if int(time.strftime("%m")) == int(time.strftime("%m")) - 1:
                        estado_ope = "00"
                    else:
                        estado_ope = "01"

            # datos a exportar a txt

            txt_line = "%s|%s|M%s|%s|%s|%s|%s|%s|%s|%s" % (
                line.date.strftime("%Y%m00") or '',  # 1 fecha en formato codigo
                line.name.replace("/", "") or '', #2 nombre de la factura
                line.x_studio_field_fwlP9 or '', #3 codigo de almacenamiento
                _catalogo or '', #4 codigo de la compañia a quien se brindo el servicio
                line.partner_id.vat or '', #5 ruc de la empresa
                line.partner_id.name or '', #6 nombre de la empresa
                line.date.strftime("%d/%m/%Y") or '', #7 fecha de elaboración
                cantidad or '', #8 total de monto a cobrar
                estado_ope or '',
                '',
            )

            # Agregamos la linea al TXT
            content_txt = content_txt + "" + txt_line + "\r\n"

        self.write({
            'state': 'get',
            'txt_binary': base64.b64encode(content_txt.encode('ISO-8859-1')),
            'txt_filename': "Ple. Cuenta 17"
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ple. Cuenta 17',
            'res_model': 'libreria.account_17',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new'
        }
