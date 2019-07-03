# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError


class DnkProductDevelopmentStage(models.Model):
    _name = "dnk.crm.pd.stage"
    _description = "Stage of PD"
    _rec_name = 'dnk_name'
    _order = "dnk_sequence, dnk_name, id"

    dnk_name = fields.Char('- Nombre Etapa', required=True, translate=True)
    dnk_description = fields.Text(translate=True)
    dnk_sequence = fields.Integer('- Secuencia', default=1, help="Orden de las etapas.")
    #dnk_fold = fields.Boolean('- Mostrado en Kanban',
        #help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    fold = fields.Boolean('- Mostrado en Kanban',
        help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')


class DnkProductDevelopmentStyle(models.Model):
    _name = 'dnk.crm.pd.style'
    _rec_name = 'dnk_name'

    dnk_name = fields.Char('- Nombre', required=True)


class DnkProductDevelopmentAttachments(models.Model):
    _name = 'dnk.crm.pd.attachments'
    _rec_name = 'dnk_name'

    dnk_name = fields.Char('- Nombre', required=True)

class DnkProductDevelopmentThickness(models.Model):
    _name = 'dnk.crm.pd.thickness'
    _rec_name = 'dnk_function'

    dnk_sequence = fields.Integer('- Secuencia')
    dnk_function = fields.Char('- Función')
    dnk_um = fields.Selection([('mm','mm'),('cm','cm')],'- Unidad de medida')
    dnk_size = fields.Float('- Tamaño')
    dnk_pd_id = fields.Many2one('dnk.crm.product.development', 'Desarrollo de Producto', ondelete='cascade')

class DnkProductDevelopmentMaterials(models.Model):
    _name = 'dnk.crm.pd.materials'
    _rec_name = 'dnk_name'
    _order = 'dnk_sequence,dnk_name'


    dnk_name = fields.Char('- Nombre', required=True)
    dnk_sequence = fields.Integer('- Sequence')

class DnkProductDevelopmentClothing(models.Model):
    _name = 'dnk.crm.pd.clothing'
    _rec_name = 'dnk_name'
    _order = 'dnk_sequence,dnk_name'


    dnk_name = fields.Char('- Nombre', required=True)
    dnk_sequence = fields.Integer('- Sequence')

class DnkProductDevelopmentClothingCut(models.Model):
    _name = 'dnk.crm.pd.clothing.cut'
    _rec_name = 'dnk_name'
    _order = 'dnk_sequence,dnk_name'


    dnk_name = fields.Char('- Nombre', required=True)
    dnk_sequence = fields.Integer('- Sequence')

class DnkProductDevelopmentClothingCustomisations(models.Model):
    _name = 'dnk.crm.pd.clothing.customisations'
    _rec_name = 'dnk_name'

    dnk_sequence = fields.Integer('- Secuencia')
    dnk_name = fields.Char('- Nombre', required=True)
    dnk_pd_id = fields.Many2one('dnk.crm.product.development', 'Desarrollo de Producto', ondelete='cascade')

class DnkProductDevelopmentMaterialProperties(models.Model):
    _name = 'dnk.crm.pd.material.properties'
    _rec_name = 'dnk_name'
    _order = 'dnk_sequence,dnk_name'


    dnk_name = fields.Char('- Nombre', required=True)
    dnk_sequence = fields.Integer('- Sequence')

class DnkProductDevelopmentAccesories(models.Model):
    _name = 'dnk.crm.pd.accessories'
    _rec_name = 'dnk_name'
    _order = 'dnk_sequence,dnk_name'


    dnk_name = fields.Char('- Nombre', required=True)
    dnk_sequence = fields.Integer('- Sequence')


class DnkProductDevelopmentSerial(models.Model):
   _name = 'dnk.crm.pd.serial'
   _rec_name = 'dnk_name'

   dnk_name = fields.Char('Nombre', required=True)


class DnkProductDevelopment(models.Model):
    _name = "dnk.crm.product.development"
    _inherit = ['mail.thread']
    _rec_name = 'dnk_name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    def _default_lead_id(self):
        if self._context and self._context.get('active_model', False) == 'crm.lead':
            return self._context.get('active_id', False)
        return False

    def _default_user_id(self):
        if self._context and self._context.get('active_model', False) == 'crm.lead':
            return self.env['crm.lead'].search([('id','=',self._context.get('active_id', False))]).user_id
        return False


    def _default_stage_id(self):
        pd_stage = self.env['dnk.crm.pd.stage'].sudo().search([])
        return pd_stage and pd_stage[0].id or False


    @api.model
    def get_operative_group(self):
            if self.env.user.has_group('dnk_crm_product_development.dnk_crm_product_develpment_oper_group') :
                self.dnk_operativo = True

            else :
                self.dnk_operativo = False

    @api.model
    def create(self, vals):

        if vals['dnk_piezas_proyecto'] <= 0:
            raise ValidationError(_('El campo [- Piezas por proyecto DP] debe ser mayor a cero'))
        if vals['dnk_cantidad_consumo'] <= 0 and vals['dnk_tiempo_consumo'] != 'unico':
            raise ValidationError(_('El campo [- Veces que será consumido] debe ser mayor a cero'))
        if vals['dnk_precio_estimado'] <= 0:
            raise ValidationError(_('El campo [- Precio estimado] debe ser mayor a cero'))

        vals['dnk_name'] = self.env['ir.sequence'].next_by_code('dnk.crm.product.development') or _('New')
        return super(DnkProductDevelopment, self).create(vals)

    def _get_attachment_qty(self):
        for rec in self:
            attachment_search = self.env['ir.attachment'].search([('res_model','=','product.category'),('res_id','=',rec.dnk_family_id.id)])
            rec.dnk_attachments_qty = len(attachment_search)


    dnk_attachments_qty = fields.Integer(string='- Adjuntos', compute='_get_attachment_qty', readonly=True)
    dnk_lead_id = fields.Many2one('crm.lead','- Lead', required=True, default=lambda self: self._default_lead_id(), track_visibility='onchange')
    dnk_sale_order = fields.Many2one('sale.order','- Order', track_visibility='onchange')
    dnk_name = fields.Char(string='- Folio', index=True, readonly=True, default=lambda self: _('New'))
    dnk_family_id = fields.Many2one('product.category',string='- Familia', related='dnk_lead_id.dnk_family_id', store=True, track_visibility='onchange')
    dnk_pd_form_type = fields.Selection(related="dnk_family_id.dnk_pd_form_type",string="- Formato DP a Usar", required=True)
    dnk_subfamily_id = fields.Many2one('product.category',string='- Subfamilia', related='dnk_lead_id.dnk_subfamily_id', store=True, track_visibility='onchange') #editable
    dnk_final_customer_id = fields.Many2one('res.partner',string='- Cliente Final', related='dnk_lead_id.dnk_final_customer_id', store=True, track_visibility='onchange')
    dnk_partner_id = fields.Many2one('res.partner', string='- Cliente', related='dnk_lead_id.partner_id', store=True, track_visibility='onchange')
    dnk_contact_name = fields.Char(string='- Nombre contacto', related='dnk_lead_id.contact_name', store=True, track_visibility='onchange') #editable
    dnk_planned_revenue = fields.Float(string='- Importe esperado', related='dnk_lead_id.planned_revenue', store=True, track_visibility='onchange')
    dnk_stage_id = fields.Many2one('dnk.crm.pd.stage', string='- Etapa', index=True, group_expand='_read_group_stage_ids', default=lambda self: self._default_stage_id(), track_visibility='onchange')
    dnk_user_id = fields.Many2one('res.users', string='- Vendedor', default=lambda self: self._default_user_id(), track_visibility='onchange') #editable
    dnk_company_id = fields.Many2one('res.company',string='- Compañía', default=lambda self: self.env['res.company']._company_default_get(), readonly=True, track_visibility='onchange')
    dnk_team_id = fields.Many2one('crm.team', string='- Canal de venta', related="dnk_lead_id.team_id")
    dnk_color = fields.Integer('- Color', default=0)
    dnk_active = fields.Boolean('- Activo', default=True)
    dnk_operativo = fields.Boolean('- Operativo', compute='get_operative_group')



    dnk_date = fields.Datetime('- Fecha', default=lambda self: fields.Datetime.now(), readonly=True)
    dnk_date_deadline = fields.Date('- Fecha de entrega estimada', help="Fecha en la que se espera se entregue el códido del producto para cotización")
#
    ## INICIAN VARIABLES EN ESPAÑOL, Pérdonenme dioes y diosas por la mezla :(
    dnk_prenda = fields.Boolean('- ¿Es Prenda?', default=lambda self: self._dnk_valida_por_familia(), compute='_dnk_valida_por_familia')
    dnk_pedido_muestra  = fields.Char('- Pedido de muestra')
    #dnk_tipo_muestra = fields.Selection([('dibuio','Dibujo'),('costeo','Costeo'),('fisica','Muestra Física')],'- Se solicita')
    #request = fields.Selection([('dibuio','Dibuio'),('costeo','Costeo'),('mus_fisica','Muestra Fisica')],'SE SOLICITA')
    dnk_dibujo  = fields.Boolean('- Dibujo')
    dnk_costeo  = fields.Boolean('- Costeo')
    dnk_codigo  = fields.Boolean('- Código')

#     is_provide = fields.Selection([('muestra_pro','Muestra Producto'),('muestra_comp','Muestra Componente'),('dibujo','DIBUJO')],'SE PROPORCIONA')
    dnk_muestra_producto    = fields.Boolean('- Producto')
    dnk_muestra_componente = fields.Boolean('- Componente')
    dnk_muestra_dibujo     = fields.Boolean('- Dibujo')
    dnk_acomodo   = fields.Selection([('vertical','Vertical'),('horizontal','Horizontal'),('paralelobase','Paralelo a base')],'- Acomodo')
    #pro_muestra = fields.Boolean('Muestra Producto')
    #pro_muestra_com = fields.Boolean('Muestra Componente')
    #pro_dibujo = fields.Boolean('Dibujo')

    #dnk_piezas_op       = fields.Char('- Piezas por Oportunidad')
    dnk_tiempo_consumo  = fields.Selection([('unico','Único'),('mensual','Mensual'),('anual','Anual')], '- Tiempo de consumo')
    dnk_cantidad_consumo  = fields.Integer('- Veces que será consumido')
    #dnk_precio_objetivo = fields.Float('- Precio Objetivo')

    #piezas_opp = fields.Char('PIEZAS POR OPORTUNIDAD')
    #select_1 = fields.Selection([('unico','UNICO'),('mensual','MENSUAL'),('anual','ANUAL')], 'Tiempo De Consumo')
    #target_price = fields.Float('PRECIO OBJETIVO')

    #
    #dnk_cuidado_cosmetico    = fields.Boolean('- Cosmético')
    #dnk_cuidado_conductivo = fields.Boolean('- Conductivo')
    #dnk_cuidado_abrasividad = fields.Boolean('- Abrasivo')
    #dnk_cuidado_disipativo = fields.Boolean('- Disipativo')

    #Datos del componente
    dnk_peso  = fields.Float('- Peso (Kg)')
    dnk_largo = fields.Float('- Largo')
    dnk_ancho = fields.Float('- Ancho')
    dnk_alto  = fields.Float('- Alto')

    dnk_unidad_medida   = fields.Selection([('mm','mm'),('cm','cm')],'- Unidad')

    #dnk_funcion         = fields.Char('- Funcion del Componente')
    #dnk_tiempo_estimado = fields.Selection([('0-6','0-6'),('6-12','6-12'),('12-24','12-24'),('+24','+24')],'- Tiempo estimado de vida (meses)')

    #Datos del Producto
    dnk_largo_producto = fields.Float('- Largo')
    dnk_ancho_producto = fields.Float('- Ancho')
    dnk_espesor_producto  = fields.Float('- Espesor')
    dnk_um_producto = fields.Selection([('mm','mm'),('cm','cm')],'- Unidad de medida')

    #Cavidades

    dnk_largo_cavidad   = fields.Float('- Largo')
    dnk_ancho_cavidad   = fields.Float('- Ancho')
    dnk_espesor_cavidad = fields.Float('- Espesor')
    dnk_um_cavidad   = fields.Selection([('mm','mm'),('cm','cm')],'- Unidad de medida')

    dnk_cavidades  = fields.Char('- Número de cavidades')
    dnk_contenedor = fields.Char('- Referencia contenedor')
    dnk_puerta     = fields.Selection([('no','No'),('unica','Única'),('traslapada','Traslapada')],string='- ¿Requiere puerta?')
    #dnk_tipo       = fields.Selection([('unica','Única'),('traslapada','- Traslapada')],string="- Tipo")
    dnk_estibable  = fields.Boolean('- ¿Es estibable?')
    #dnk_estiba_max = fields.Char(' Estiva Máxima')  # NI LA USÉ
    #dnk_herramental= fields.Boolean('- ¿Requiere Herramental?')
    #dnk_curf       = fields.Boolean('- CURF')
    #dnk_req_instalacion= fields.Boolean('- ¿Requiere Instalación')
    #dnk_instalacion = fields.Selection([('ret','Retainer'),('tu_car','Tuber Carrier'),('vel','Velcro'),('dip','Dipstick'),('tapes','Tapes'),('other','Otro')], '- ¿Con qué se instala?')

    dnk_product_code = fields.Char("- Código del producto")

    #Form Dos
    #dnk_product_id = fields.Many2one('product.product',string='- Artículo', related='dnk_lead_id.dnk_product_id', store=True, track_visibility='onchange')
#     articilo = fields.Selection([('elija','Elija una opcion')], string="Articulo", track_visibility='onchange')
    #dnk_um_pulgada = fields.Boolean('- Son Pulgadas?', track_visibility='onchange')
    dnk_um = fields.Selection([('in','in')],'- Unidad de medida', default='in', track_visibility='onchange')
    dnk_tiempo_consumo = fields.Selection([('mensual','Mensual'),
                                          ('semestral','Semestral'),
                                          ('anual','Anual'),
                                          ('unico','Único'),
                                          ], string="- Tiempo de consumo", track_visibility='onchange')
    #dnk_moneda = fields.Many2one('res.currency', string="- Moneda", track_visibility='onchange')
    dnk_nombre = fields.Char('- Nombre del proyecto', track_visibility='onchange')
    dnk_descripcion = fields.Text('- Descripción', track_visibility='onchange')
    dnk_piezas_proyecto = fields.Float("- Piezas anuales por proyecto DP", track_visibility='onchange')
    dnk_precio_estimado = fields.Float('- Precio estimado', track_visibility='onchange')
    dnk_importe_oportunidad = fields.Float(string="- Importe por proyecto DP", compute="_importe_oportunidad",track_visibility='onchange')
    #dnk_piezas_proyecto_dos = fields.Float("- Piezas por Proyecto DP", track_visibility='onchange')
    # Repedito  precio_estimado1 = fields.Float('- Precio Estimado', track_visibility='onchange')
    #dnk_importe_oportunidad_dos = fields.Float(string="- Importe por Proyecto DP", compute="_importe_oportunidad",track_visibility='onchange')

    dnk_observaciones = fields.Text("- Observaciones", track_visibility='onchange')
    #dnk_es_muestra = fields.Boolean('- ¿Es Muestra?')
    #dnk_es_costeo = fields.Boolean('- Costeo')
    dnk_especificacion = fields.Boolean('- ¿Se adjuntó especificación?')


    #form 3
    dnk_serie = fields.Many2one('dnk.crm.pd.serial','- Serie')
    dnk_abertura = fields.Char("- Abertura")
    dnk_altura = fields.Char("- Altura")
    dnk_fuelle = fields.Char("- Fuelle")
    dnk_calibre = fields.Char("- Calibre")
    dnk_estilo = fields.Many2one('dnk.crm.pd.style', '- Estilo')
    #Validar
    dnk_aditamentos = fields.Many2many(comodel_name='dnk.crm.pd.attachments', relation='dnk_pd_attachments_rel', string="- Aditamentos")
    dnk_materiales = fields.Many2many(comodel_name='dnk.crm.pd.materials', relation='dnk_pd_materials_rel', string="- Materiales")
    dnk_propiedades = fields.Many2many(comodel_name='dnk.crm.pd.material.properties', relation='dnk_pd_material_properties_rel', string="- Propiedades del material")
    dnk_accesorios = fields.Many2many(comodel_name='dnk.crm.pd.accessories', relation='dnk_pd_accessories_rel', string="- Accesorios")
    dnk_espesor_ids = fields.One2many('dnk.crm.pd.thickness', 'dnk_pd_id', string="- Espesor de nivel y función")

    dnk_tela = fields.Many2one(comodel_name='dnk.crm.pd.clothing', relation='dnk_crm_pd_clothing_rel', string="- Tela")
    dnk_corte = fields.Many2one(comodel_name='dnk.crm.pd.clothing.cut', relation='dnk_crm_pd_clothing_cut_rel', string="- Corte")
    dnk_personalizaciones_ids = fields.One2many('dnk.crm.pd.clothing.customisations', 'dnk_pd_id', string="- Personalizaciones")

    dnk_codigo_final = fields.Many2one('product.product','- Código final', track_visibility='onchange')
    dnk_codigo_final_desc = fields.Char('- Descripción del código final')
    dnk_rechazado = fields.Boolean('- Rechazado?')
    dnk_rechazado_desc = fields.Char("- Comentarios de rechazo")



    @api.onchange('dnk_piezas_proyecto','dnk_precio_estimado')
    @api.depends('dnk_piezas_proyecto','dnk_precio_estimado')
    def _importe_oportunidad(self):
        for pd in self:
            pd.dnk_importe_oportunidad = pd.dnk_piezas_proyecto * pd.dnk_precio_estimado


    @api.onchange('dnk_date_deadline')
    def _onchange_date_deadline(self):
        if self.dnk_date_deadline:
            if self.dnk_date_deadline <= self.dnk_date:
                raise UserError(_('Por favor seleccione una - Fecha de entrega estimada  anterior al campo de - Fecha + 1.'))


    @api.onchange('dnk_family_id')
    @api.model
    def _dnk_valida_por_familia(self):
        ropa = ["BATA","OVEROL","PRENDA"]
        for dp in self:
            if any(dp.dnk_family_id.name in opcion for opcion in ropa):
                dp.dnk_prenda = True
            else :
                dp.dnk_prenda = False

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.multi
    def close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}
