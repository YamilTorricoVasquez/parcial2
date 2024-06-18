from odoo import models, fields, api, exceptions

class Nota(models.Model):
    _name = 'academico.nota'
    _description = 'Nota'

    boletin_id = fields.Many2one('academico.boletin', string='Boletín')
    estudiante_id = fields.Many2one('academico.estudiante', string='Estudiante', required=True)
    curso_id = fields.Many2one(related='estudiante_id.curso_id', string='Curso')
    nivel_id = fields.Selection(related='estudiante_id.nivel_id', string='Nivel')
    materia_id = fields.Many2one('academico.materia', string='Materia', required=True)
    
    nota = fields.Float(string='Nota', required=True)
    trimestre = fields.Selection([('1', '1er Trimestre'), ('2', '2do Trimestre'), ('3', '3er Trimestre')], string='Trimestre', required=True)
    anio= fields.Date(string='año', required=True)
    _sql_constraints = [
      ('unique_estudiante_materia_trimestre', 'UNIQUE(estudiante_id, materia_id, trimestre)', 'Ya existe una nota para esta materia en este trimestre para este estudiante.'),
        ('check_notas_limit', 'CHECK(_check_notas_limit())', 'No se pueden agregar más de 3 notas para una materia.'),
    ]
   
    
    def _check_notas_limit(self):
        for nota in self:
            count = self.env['academico.nota'].search_count([
                ('materia_id', '=', nota.materia_id.id),
            ])
            if count >= 3:
                return False
        return True

    @api.constrains('materia_id', 'trimestre')
    def _check_unique_materia_trimestre(self):
        for nota in self:
            existing_notas = self.env['academico.nota'].search([
                ('materia_id', '=', nota.materia_id.id),
                ('trimestre', '=', nota.trimestre),
                ('id', '!=', nota.id),  # Excluyendo la nota actual si está siendo actualizada
            ])
            if existing_notas:
                raise exceptions.ValidationError('Ya existe una nota para esta materia en este trimestre.')
    @api.constrains('estudiante_id', 'materia_id', 'trimestre')
    def _check_notas_limit(self):
        for record in self:
            notas_count = self.search_count([
                ('estudiante_id', '=', record.estudiante_id.id),
                ('materia_id', '=', record.materia_id.id),
                ('trimestre', '=', record.trimestre)
            ])
            if notas_count > 3:
                raise exceptions.ValidationError('No se pueden agregar más de 3 notas para una materia en un trimestre para un estudiante.')