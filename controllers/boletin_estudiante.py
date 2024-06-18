from odoo import http
from odoo.http import request
import json

class BoletinController(http.Controller):

    @http.route('/api/boletines', auth='public', website=False, csrf=False, type='http', methods=['GET'], cors='*')
    def get_boletines(self, **kw):
        boletines = request.env['academico.boletin'].sudo().search([])
        boletin_list = []
        for boletin in boletines:
            boletin_list.append ({
                
                'estudiante': boletin.estudiante_id,
                'ci_estudiante': boletin.ci_estudiante,
                'curso': boletin.curso_id.name,
                'nivel': boletin.nivel_id,
                'estado_aprobacion': boletin.estado_aprobacion,
                'promedio': boletin.promedio,
            })
           
        return request.make_response(
            json.dumps({
                'status': 200,
                'message': 'Success',
                'data': boletin_list
            }),
            headers={'Content-Type': 'application/json'}
        )

# import json
# from odoo import http
# from odoo.http import request

# class HelloApi(http.Controller):
#     @http.route('/api', auth='public', website=False, csrf=False, type='http', methods=['GET'], cors='*')
#     def hello(self, **kw):
#         estudiantes = request.env['academico.estudiante'].sudo().search([])
#         est_list = []
#         for est in estudiantes:
#             est_list.append({
#                 'name': est.name,
#                 'ci': est.ci,
#                 'email': est.email,
#                 'phone': est.phone,
#                 'curso_id': est.curso_id.name
#             })
#         return request.make_response(
#             json.dumps({
#                 'status': 200,
#                 'message': 'Success',
#                 'data': est_list
#             }),
#             headers={'Content-Type': 'application/json'}
#         )
