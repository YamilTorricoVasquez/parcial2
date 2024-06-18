from odoo import http
from odoo.http import request

class BoletinController(http.Controller):

    @http.route('/api/boletin/<ci>', type='json', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_boletin_by_ci(self, ci):
        # Fetch the boletin record by CI
        boletin = request.env['academico.boletin'].sudo().search([('ci_estudiante', '=', ci)], limit=1)
        if not boletin:
            return {'error': 'No se encontró el boletín para el CI proporcionado'}

        # Prepare the response data
        boletin_data = {
            'estudiante': boletin.estudiante_id.name,
            'ci_estudiante': boletin.ci_estudiante,
            'curso': boletin.curso_id.name,
            'nivel': boletin.nivel_id,
            'estado_aprobacion': boletin.estado_aprobacion,
            'promedio': boletin.promedio,
            'notas': [{'asignatura': nota.asignatura_id.name, 'calificacion': nota.calificacion} for nota in boletin.nota_ids]
        }

        return boletin_data
