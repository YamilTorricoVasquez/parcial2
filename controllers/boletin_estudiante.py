from odoo import http
from odoo.http import request
import json

class BoletinAPI(http.Controller):

    @http.route('/api/boletin/<string:ci>/<string:gestion>', type='http', auth='none', methods=['GET'])
    def get_boletin_by_ci(self, ci, gestion, **kwargs):
        try:
            # Buscar al estudiante por su CI
            estudiante = request.env['academico.estudiante'].sudo().search([('ci', '=', ci)], limit=1)
            if not estudiante:
                return json.dumps({'error': 'Estudiante no encontrado'})

            # Buscar el boletín del estudiante encontrado para la gestión específica
            boletin = request.env['academico.boletin'].sudo().search([
                ('estudiante_id', '=', estudiante.id),
                ('gestion', '=', gestion)
            ], limit=1)

            if not boletin:
                return json.dumps({'error': 'Boletín no encontrado'})

            # Preparar la estructura de datos para el boletín
            boletin_data = {
                'estudiante': boletin.estudiante_id.name,
                'ci_estudiante': boletin.ci_estudiante,
                'curso': boletin.curso_id.name if boletin.curso_id else None,
                'nivel': boletin.nivel_id,
                'estado_aprobacion': boletin.estado_aprobacion,
                'promedio': boletin.promedio,
                'notas': []
            }

            for nota in boletin.nota_ids:
                anio_str = nota.anio if isinstance(nota.anio, str) else nota.anio.strftime('%Y-%m-%d') if nota.anio else None

                boletin_data['notas'].append({
                    'materia': nota.materia_id.name,
                    'nota': nota.nota,
                    'trimestre': nota.trimestre,
                    'anio': anio_str,
                })

            return json.dumps({'boletin': boletin_data})

        except Exception as e:
            return json.dumps({'error': str(e)})

