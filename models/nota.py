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
    anio= fields.Char(string='año', required=True, size=4)
    _sql_constraints = [
        ('unique_nota_estudiante_materia_trimestre_anio', 'UNIQUE(estudiante_id, materia_id, trimestre, anio)', 'Ya existe una nota para este estudiante, materia, trimestre y año.'),
    ]

    @api.model
    def create(self, vals):
        # Validar que no se cree una nota duplicada para el mismo estudiante, materia, trimestre y año
        existing_nota = self.env['academico.nota'].search([
            ('estudiante_id', '=', vals.get('estudiante_id')),
            ('materia_id', '=', vals.get('materia_id')),
            ('trimestre', '=', vals.get('trimestre')),
            ('anio', '=', vals.get('anio'))
        ])
        if existing_nota:
            raise ValidationError('Ya existe una nota para este estudiante, materia, trimestre y año.') # type: ignore

        return super(Nota, self).create(vals)