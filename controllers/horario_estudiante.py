from odoo import http
from odoo.http import request
import json

class HorarioController(http.Controller):

    @http.route('/api/horario/estudiante/<string:ci>', type='http', auth='none', methods=['GET'], cors='*')
    def get_horario_by_ci(self, ci, **kwargs):
        try:
            # Buscar al estudiante por su CI
            estudiante = request.env['academico.estudiante'].sudo().search([('ci', '=', ci)])
            if not estudiante:
                return json.dumps({'error': 'Estudiante no encontrado'})

            # Obtener el curso del estudiante
            curso = estudiante.curso_id
            if not curso:
                return json.dumps({'error': 'El estudiante no tiene un curso asignado'})

            # Buscar los horarios del curso del estudiante
            horarios = request.env['academico.horario'].sudo().search([('name', '=', curso.id)])
            if not horarios:
                return json.dumps({'error': 'No se encontraron horarios para el curso del estudiante'})

            # Preparar la estructura de datos para los horarios
            horarios_data = []
            for horario in horarios:
                horarios_data.append({
                    'curso': curso.name,
                    'nivel': horario.nivel_id,
                    'materia': horario.materia_id.name,
                    'aula': horario.aula_id.name,
                    'start_time': horario.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time': horario.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    
                })

            return json.dumps({'horarios': horarios_data})

        except Exception as e:
            return json.dumps({'error': str(e)})
