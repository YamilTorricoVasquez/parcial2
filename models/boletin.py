         
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Boletin(models.Model):
    _name = 'academico.boletin'
    _description = 'Boletín de Notas'

    estudiante_id = fields.Many2one('academico.estudiante', string='Estudiante', required=True)
    ci_estudiante = fields.Char(string='CI Estudiante', related='estudiante_id.ci', readonly=True)
    curso_id = fields.Many2one('academico.curso', string='Curso', compute='_compute_curso', store=True)
    nivel_id = fields.Selection(related='curso_id.nivel', string='Nivel')
    gestion = fields.Char(string="Gestion", required=True)

    nota_ids = fields.One2many('academico.nota', 'boletin_id', string='Notas', store=True)
    estado_aprobacion = fields.Char(string='Estado de Aprobación', compute='_compute_estado_aprobacion', store=True)
    promedio = fields.Float(string='Promedio', compute='_compute_promedio', store=True)

    _sql_constraints = [
        ('unique_boletin_per_student_per_gestion', 
         'UNIQUE(estudiante_id, gestion)', 
         'Solo se puede crear un boletín por estudiante y gestión.')
    ]

    @api.model
    def create(self, vals):
        existing_boletin = self.env['academico.boletin'].search([
            ('estudiante_id', '=', vals.get('estudiante_id')),
            ('gestion', '=', vals.get('gestion'))
        ])
        if existing_boletin:
            raise ValidationError('Ya existe un boletín para este estudiante y gestión.')
        return super(Boletin, self).create(vals)

    @api.depends('estudiante_id')
    def _compute_curso(self):
        for boletin in self:
            if boletin.estudiante_id:
                boletin.curso_id = boletin.estudiante_id.curso_id.id
                boletin.nivel_id = boletin.estudiante_id.curso_id.nivel
            else:
                boletin.curso_id = False
                boletin.nivel_id = False

    @api.depends('nota_ids')
    def _compute_promedio(self):
        for boletin in self:
            total_notas = sum(boletin.nota_ids.mapped('nota'))
            boletin.promedio = total_notas / len(boletin.nota_ids) if boletin.nota_ids else 0.0

    @api.depends('promedio')
    def _compute_estado_aprobacion(self):
        for boletin in self:
            boletin.estado_aprobacion = 'Aprobado' if boletin.promedio >= 51 else 'Reprobado'

    @api.onchange('gestion')
    def _onchange_gestion(self):
        if self.gestion and self.estudiante_id:
            # Buscar todas las notas del estudiante para el año seleccionado en gestion
            notas_del_boletin = self.env['academico.nota'].search([
                ('estudiante_id', '=', self.estudiante_id.id),
                ('anio', '=', self.gestion)  # asumiendo que 'anio' es el campo que almacena el año en el modelo Nota
            ])
            # Establecer las notas encontradas en nota_ids
            self.nota_ids = [(6, 0, notas_del_boletin.ids)]

    @api.onchange('estudiante_id')
    def _onchange_estudiante_id(self):
        if self.estudiante_id:
            self.curso_id = self.estudiante_id.curso_id.id
            self.nivel_id = self.estudiante_id.curso_id.nivel
        else:
            self.curso_id = False
            self.nivel_id = False

