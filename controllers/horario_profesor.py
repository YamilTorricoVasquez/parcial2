from odoo import http
from odoo.http import request
import json

class HorarioController(http.Controller):

    @http.route('/api/horario/profesor/<string:ci>', type='http', auth='none', methods=['GET'], cors='*')
    def get_horario_by_profesor(self, ci, **kwargs):
        try:
            # Buscar al profesor por su CI
            profesor = request.env['academico.profesor'].sudo().search([('ci', '=', ci)])
            if not profesor:
                return json.dumps({'error': 'Profesor no encontrado'})

            # Obtener las materias asignadas al profesor
            materias_profesor = profesor.materia_ids
            if not materias_profesor:
                return json.dumps({'error': 'El profesor no tiene materias asignadas'})

            # Obtener el curso del profesor
            curso_profesor = profesor.curso_id
            if not curso_profesor:
                return json.dumps({'error': 'El profesor no tiene un curso asignado'})

            # Buscar los horarios relacionados con las materias y curso del profesor
            horarios_data = []
            for materia in materias_profesor:
                # Filtrar horarios por materia y curso del profesor
                horarios = request.env['academico.horario'].sudo().search([
                    ('materia_id', '=', materia.id),
                    ('name', '=', curso_profesor.id)
                ])
                for horario in horarios:
                    horarios_data.append({
                        'curso': curso_profesor.name,
                        'materia': materia.name,
                        'nivel': horario.nivel_id,
                        'aula': horario.aula_id.name,
                        'start_time': horario.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'end_time': horario.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    })

            if not horarios_data:
                return json.dumps({'error': 'No se encontraron horarios para las materias del profesor'})

            return json.dumps({'horarios': horarios_data})

        except Exception as e:
            return json.dumps({'error': str(e)})
