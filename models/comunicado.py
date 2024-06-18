from odoo import models, fields

class Comunicado(models.Model):
    _name = 'academico.comunicado'
    _description = 'Comunicado del colegio para padres'

    name = fields.Char('Título', required=True)
    contenido = fields.Html('Contenido')
    fecha_publicacion = fields.Date('Fecha de Publicación')
    #visible_para_padres = fields.Boolean('Visible para Padres', default=True)
