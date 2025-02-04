from odoo import models, fields, api
import base64
import logging
import time

_logger = logging.getLogger(__name__)

###########################################################################################
# -- OPTIMIZA
# -- DESCRIPCION: CLASE CHART_ACCOUNT CREACION PARA PROYECTO ODOO
# -- AUTOR: JORDY VALENZUELA VALCARCEL
# -- CAMBIOS: ID     FECHA (DD/MM/YYYY)  PERSONA               CAMBIOS EFECTUADOS
# --          #001   13/03/2019          JORDY VALENZUELA          CREACION DE LA CLASE.
# --          #002   13/03/2019          JORDY VALENZUELA          AGREGADO DE CAMPOS
# --          #003   13/03/2019          JORDY VALENZUELA          VALIDACION DE CAMPOS
# --          #004   13/03/2019          JORDY VALENZUELA          AGREGADO DE FILTROS.
# -----------------------------------------------------------------------------------------

#   Inicio #001 "CREACION DE LA CLASE"
class ChartAccount(models.TransientModel):
    _name = "libreria.chart_accounts"
    _description = "Plan Contable"


#   Inicio #004 "AGREGADO DE FILTROS"
    date_month = fields.Selection(string="Mes", selection=[('01', 'Enero'),
                                                           ('02', 'Febrero'),
                                                           ('03', 'Marzo'),
                                                           ('04', 'Abril'),
                                                           ('05', 'Mayo'),
                                                           ('06', 'Junio'),
                                                           ('07', 'Julio'),
                                                           ('08', 'Agosto'),
                                                           ('09', 'Septiembre'),
                                                           ('10', 'Octubre'),
                                                           ('11', 'Noviembre'),
                                                           ('12', 'Diciembre')])
    date_year = fields.Char(string="Año", size=4)
#   Fin #004

    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')
    txt_filename = fields.Char('filename', readonly=True)
    txt_binary = fields.Binary('file', readonly=True)

    @api.multi
    def generate_file(self):

        # filtro de fecha
        dominio = [('month_year_inv', 'like', self.date_month + "" + self.date_year)]

        # modelo a buscar
        lst_account_move_line = self.env['account.account'].search(dominio)

        # variables creadas
        content_txt = ""
        estado_ope = ""
        campo = ""
        campo1 = ""
        # Inicio #003 "VALIDACION DE CAMPOS"
        # Iterador
        for line in lst_account_move_line:
            # validador de estado de operación
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
            # validador de campo vacio
            if line.account_plan_code:
                campo = line.account_plan_code
            if line.account_plan_code:
                campo1 = line.account_plan_code
        # Fin #003
            # datos a exportar a txt
            # Inicio #002 "AGREGADO DE CAMPOS"
            txt_line = "%s|%s|%s|%s|%s|%s|%s|%s" % (
                line.create_date.strftime("%Y%m00") or '',  # Periodo
                line.code or '',  # codigo cuenta contable
                line.name or '',  # descripcion de cuenta
                campo[0:2] or '',  # Codigo Plan de Cuenta
                campo1[2:50] or '',  # Descripcion del plan de cuenta
                '',  # dejar en blanco
                '',  # dejar en blanco
                estado_ope or ''  # estado de operacion

            )
            # Fin #002

            # Agregamos la linea al TXT
            content_txt = content_txt + "" + txt_line + "\r\n"

        self.write({
            'state': 'get',
            'txt_binary': base64.b64encode(content_txt.encode('ISO-8859-1')),
            'txt_filename': "plan_contable.txt"
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Plan Contable',
            'res_model': 'libreria.chart_accounts',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new'
        }
#   Fin #001
