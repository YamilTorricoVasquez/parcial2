from odoo import http
from odoo.http import request
import json

class HelloApi(http.Controller):

    @http.route('/api/estudiantes', auth='public', website=False, csrf=False, type='http', methods=['GET'], cors='*')
    def get_estudiantes(self, **kw):
        try:
            estudiantes = request.env['academico.estudiante'].sudo().search([])
            est_list = []
            for est in estudiantes:
                boletines = []
                for boletin in est.boletin_ids:
                    boletines.append({
                        'curso': boletin.curso_id.name,
                        'nivel': boletin.nivel_id,
                        'estado_aprobacion': boletin.estado_aprobacion,
                        'promedio': boletin.promedio,
                    })
                est_list.append({
                    'name': est.name,
                    'ci': est.ci,
                    'email': est.email,
                    'phone': est.phone,
                    'curso_id': est.curso_id.name,
                    'boletines': boletines
                })

            return request.make_response(
                json.dumps({
                    'status': 200,
                    'message': 'Success',
                    'data': est_list
                }),
                headers={'Content-Type': 'application/json'}
            )

        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 500,
                    'message': f'Internal Server Error: {str(e)}',
                    'data': []
                }),
                headers={'Content-Type': 'application/json'},
                status=500
            )
