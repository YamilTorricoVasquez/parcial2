from odoo import http
from odoo.http import request

class BoletinController(http.Controller):

    @http.route('/api/boletin/<string:ci>', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def buscar_boletin_por_ci(self, ci, **kwargs):
        try:
            if not ci:
                return {'status': 400, 'message': 'Cédula es requerida'}

            estudiante = request.env['academico.estudiante'].sudo().search([('ci', '=', ci)], limit=1)
            if not estudiante:
                return {'status': 404, 'message': 'Estudiante no encontrado'}

            boletin = request.env['academico.boletin'].sudo().search([('estudiante_id', '=', estudiante.id)], limit=1)
            if not boletin:
                return {'status': 404, 'message': 'Boletín no encontrado'}

            # Construir la respuesta
            boletin_data = {
                'estudiante': estudiante.name,
                'curso': boletin.curso_id.name,
                'nivel': boletin.nivel_id,
                'notas': [{'materia': nota.materia_id.name, 'nota': nota.nota} for nota in boletin.nota_ids],
                'estado_aprobacion': boletin.estado_aprobacion,
                'promedio': boletin.promedio
            }

            return {'status': 200, 'data': boletin_data}

        except Exception as e:
            # Manejar cualquier error y retornar una respuesta adecuada
            return {'status': 500, 'message': 'Internal Server Error'}

