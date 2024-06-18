from odoo import http
from odoo.http import request
import json

class BoletinController(http.Controller):

    @http.route('/api/boletines', type='http', auth='none', methods=['GET'], cors='*', csrf=False)
    def get_boletines(self):
        boletines = request.env['academico.boletin'].sudo().search([])
        boletin_list = []
        for boletin in boletines:
            boletin_data = {
                'id': boletin.id,
                'estudiante': boletin.estudiante_id.name,
                'ci_estudiante': boletin.ci_estudiante,
                'curso': boletin.curso_id.name,
                'nivel': boletin.nivel_id,
                'estado_aprobacion': boletin.estado_aprobacion,
                'promedio': boletin.promedio,
            }
            boletin_list.append(boletin_data)
        return json.dumps(boletin_list)
