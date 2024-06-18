import json
from odoo import http
from odoo.http import request

class HelloApi(http.Controller):
    @http.route('/api', auth='public', website=False, csrf=False, type='http', methods=['GET'], cors='*')
    def hello(self, **kw):
        estudiantes = request.env['academico.estudiante'].sudo().search([])
        est_list = []
        for est in estudiantes:
            est_list.append({
                'name': est.name,
                'ci': est.ci,
                'email': est.email,
                'phone': est.phone,
                'curso_id': est.curso_id.name,
                
            })
        return request.make_response(
            json.dumps({
                'status': 200,
                'message': 'Success',
                'data': est_list
            }),
            headers={'Content-Type': 'application/json'}
        )
