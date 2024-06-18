from odoo import models, fields

class Comunicado(models.Model):
    _name = 'academico.comunicado'
    _description = 'Comunicado del colegio para padres'

    name = fields.Char(string='Título', required=True)
    contenido = fields.Text(string='Contenido')
    fecha_publicacion = fields.Date(string='Fecha de Publicación')
    #visible_para_padres = fields.Boolean('Visible para Padres', default=True)
