from odoo import http
from odoo.http import request

class BoletinController(http.Controller):

    @http.route('/api/boletin/<string:ci>', type='json', auth='public', methods=['GET'], cors='*', csrf=False)
    def get_boletin_by_ci(self, ci):
        # Buscar el estudiante por CI
        estudiante = request.env['academico.estudiante'].sudo().search([('ci', '=', ci)], limit=1)
        
        if not estudiante:
            return {'error': 'No se encontró el estudiante para el CI proporcionado'}
        
        # Buscar el boletín utilizando el registro del estudiante
        boletines = request.env['academico.boletin'].sudo().search([('estudiante_id', '=', estudiante.id)])
        
        if not boletines:
            return {'error': 'No se encontró el boletín para el estudiante con CI proporcionado'}

        # Preparar los datos de la respuesta
        boletin_data = []
        for boletin in boletines:
            boletin_info = {
                'estudiante': boletin.estudiante_id.name,  # Nombre del estudiante
                'ci_estudiante': boletin.ci_estudiante,
                'curso': boletin.curso_id.name,
                'nivel': boletin.nivel_id,
                'estado_aprobacion': boletin.estado_aprobacion,
                'promedio': boletin.promedio,
                'notas': [{'asignatura': nota.asignatura_id.name, 'calificacion': nota.calificacion} for nota in boletin.nota_ids]
            }
            boletin_data.append(boletin_info)

        return boletin_data
