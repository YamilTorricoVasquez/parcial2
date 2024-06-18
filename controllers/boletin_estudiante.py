from odoo import http
from odoo.http import request
import json

class BoletinController(http.Controller):

    @http.route('/api/boletin/nombre/<string:nombre>', type='http', auth='public', methods=['GET'], csrf=False,cors='*')
    def buscar_boletin_por_nombre(self, nombre, **kwargs):
        try:
            if not nombre:
                return http.Response(
                    '{"status": 400, "message": "Nombre es requerido"}',
                    status=400,
                    content_type='application/json'
                )

            estudiante = request.env['academico.estudiante'].sudo().search([('name', 'ilike', nombre)], limit=1)
            if not estudiante:
                return http.Response(
                    '{"status": 404, "message": "Estudiante no encontrado"}',
                    status=404,
                    content_type='application/json'
                )

            boletin = request.env['academico.boletin'].sudo().search([('estudiante_id', '=', estudiante.id)], limit=1)
            if not boletin:
                return http.Response(
                    '{"status": 404, "message": "Boletín no encontrado"}',
                    status=404,
                    content_type='application/json'
                )

            # Construir la respuesta
            boletin_data = {
                'estudiante': estudiante.name,
                'curso': boletin.curso_id.name,
                'nivel': boletin.nivel_id,
                'notas': [{'materia': nota.materia_id.name, 'nota': nota.nota} for nota in boletin.nota_ids],
                'estado_aprobacion': boletin.estado_aprobacion,
                'promedio': boletin.promedio
            }

            return http.Response(
                json.dumps({'status': 200, 'data': boletin_data}),
                status=200,
                content_type='application/json'
            )

        except Exception as e:
            # Manejar cualquier error y retornar una respuesta adecuada
            return http.Response(
                '{"status": 500, "message": "Internal Server Error"}',
                status=500,
                content_type='application/json'
            )
