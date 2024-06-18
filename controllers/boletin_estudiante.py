from odoo import http
from odoo.http import request
import json

class BoletinAPI(http.Controller):

    @http.route('/api/boletin', auth='public', website=False, csrf=False, type='http', methods=['GET'], cors='*')
    def get_boletines(self, **kw):
        try:
            boletines = request.env['academico.boletin'].sudo().search([])

            boletin_data = []
            for boletin in boletines:
                boletin_data.append({
                    'estudiante': boletin.estudiante_id.name,
                    'ci_estudiante': boletin.ci_estudiante,
                    'curso': boletin.curso_id.name,
                    'nivel': boletin.nivel_id,
                    'notas': [{'nombre': nota.name, 'valor': nota.valor} for nota in boletin.nota_ids],
                    'estado_aprobacion': boletin.estado_aprobacion,
                    'promedio': boletin.promedio,
                })

            return json.dumps({'boletines': boletin_data})

        except Exception as e:
            return json.dumps({'error': str(e)})
