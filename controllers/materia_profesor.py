from odoo import http
from odoo.http import request
import json

class MateriaProfesor(http.Controller):

    @http.route('/api/materia/curso/profesor/<string:ci>', auth='public', website=False, csrf=False, type='http', methods=['GET'], cors='*')
    def hello(self, ci, **kw):
        try:
            # Buscar al profesor por su CI
            profesor = request.env['academico.profesor'].sudo().search([('ci', '=', ci)])
            if not profesor:
                return request.make_response(
                    json.dumps({'status': 404, 'message': 'Profesor no encontrado'}),
                    headers={'Content-Type': 'application/json'}
                )

            # Obtener las materias asignadas al profesor
            materias = profesor.materia_ids.mapped('name')

            # Obtener el curso del profesor
            curso = profesor.curso_id.name if profesor.curso_id else None

            # Obtener el nivel del curso del profesor
            nivel = profesor.nivel

            # Preparar la respuesta JSON
            response_data = {
                'materias': list(materias),
                'curso': curso,
                'nivel': nivel,
            }

            return request.make_response(
                json.dumps({'status': 200, 'message': 'Success', 'data': response_data}),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'status': 500, 'message': str(e)}),
                headers={'Content-Type': 'application/json'}
            )
