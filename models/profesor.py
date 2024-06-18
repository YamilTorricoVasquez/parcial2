from odoo import models, fields, api

class Profesor(models.Model):
    _name = 'academico.profesor'
    _description = 'Profesor'

    name = fields.Char(string='Nombre completo', required=True)
    ci = fields.Char(string='Cedula de identidad', required=True, unique=True, size=7)
    email = fields.Char(string='Correo electronico',required=True)
    phone = fields.Char(string='Teléfono', required=True, size=8)
    curso_id = fields.Many2one('academico.curso', string='Curso')
    nivel = fields.Selection(related='curso_id.nivel', string='Nivel', readonly=True)
    Lista_estudiantes = fields.Many2many('academico.estudiante', compute='_compute_lista_estudiantes', string='Lista estudiantes')
    materia_ids = fields.Many2many('academico.materia', string='Materias', required=True)
    @api.depends('curso_id')
    def _compute_lista_estudiantes(self):
        for profesor in self:
            estudiantes = self.env['academico.estudiante'].search([('curso_id', '=', profesor.curso_id.id)])
            profesor.Lista_estudiantes = estudiantes.ids

    _sql_constraints = [
        ('ci_unique', 'UNIQUE(ci)', 'La cédula de identidad debe ser única.')
    ]
    # @api.onchange('materia_ids')
    # def _onchange_materia_ids(self):
    #     # Recorremos las materias asignadas al profesor
    #     for materia in self.materia_ids:
    #         # Verificamos si la materia ya tiene asignado este profesor
    #         if materia.profesor_id.id != self.id:
    #             # Si no lo tiene, actualizamos el profesor en la materia
    #             materia.write({'profesor_id': self.id})