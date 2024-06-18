from odoo import http
from odoo.http import request
import json

class BoletinAPI(http.Controller):

    @http.route('/api/boletin/<string:ci>', type='http', auth='none', methods=['GET'])
    def get_boletin_by_ci(self, ci, **kwargs):
        try:
            student = request.env['academico.estudiante'].sudo().search([('ci', '=', ci)])
            if not student:
                return json.dumps({'error': 'Estudiante no encontrado'})
            
            boletin_ids = student.boletin_ids.ids
            boletin_data = []
            for boletin_id in boletin_ids:
                boletin = request.env['academico.boletin'].sudo().browse(boletin_id)
                boletin_data.append({
                    'curso': boletin.curso_id.name,
                    'promedio': boletin.promedio,
                    'estado_aprobacion': boletin.estado_aprobacion,
                    # Agrega más campos según sea necesario
                })
            
            return json.dumps({'boletines': boletin_data})

        except Exception as e:
            return json.dumps({'error': str(e)})
