import json
from odoo import http
from odoo.http import request

class BoletinController(http.Controller):

    @http.route('/api/boletin/<string:ci>', auth='public', website=False, csrf=False, type='http', methods=['GET'], cors='*')
    def get_boletin_by_ci(self, ci, **kwargs):
        # Buscar el estudiante por CI
        estudiante = request.env['academico.estudiante'].sudo().search([('ci', '=', ci)], limit=1)
        
        if not estudiante:
            return request.make_response(
                json.dumps({'error': 'No se encontró el estudiante para el CI proporcionado'}),
                headers={'Content-Type': 'application/json'}
            )
        
        # Buscar los boletines utilizando el registro del estudiante
        boletines = request.env['academico.boletin'].sudo().search([('estudiante_id', '=', estudiante.id)])
        
        if not boletines:
            return request.make_response(
                json.dumps({'error': 'No se encontró el boletín para el estudiante con CI proporcionado'}),
                headers={'Content-Type': 'application/json'}
            )

        # Preparar los datos de la respuesta
        boletin_data = []
        for boletin in boletines:
            boletin_info = {
                'estudiante': boletin.estudiante_id.name,
                'ci_estudiante': boletin.ci_estudiante,
                'curso': boletin.curso_id.name,
                'nivel': boletin.nivel_id,
                'estado_aprobacion': boletin.estado_aprobacion,
                'promedio': boletin.promedio,
                'notas': [{'asignatura': nota.asignatura_id.name, 'calificacion': nota.calificacion} for nota in boletin.nota_ids]
            }
            boletin_data.append(boletin_info)

        return request.make_response(
            json.dumps({'status': 200, 'message': 'Success', 'data': boletin_data}),
            headers={'Content-Type': 'application/json'}
        )
