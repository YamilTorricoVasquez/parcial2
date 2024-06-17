from odoo import http
from odoo.http import request

class HelloApi(http.Controller):
    @http.route('/api', auth='public', website=False, csrf=False, type='json', methods=['GET'], cors='*')
    def hello(self, **kw):
        estudiantes = request.env['academico.estudiante'].sudo().search([])
        est_list = []
        for est in estudiantes:
            est_list.append({
                'name': est.name,
                'ci': est.ci,
                'email': est.email,
                'phone': est.phone,
                'curso_id': est.curso_id.name
            })
        return {
            'status': 200,
            'message': 'Success',
            'data': est_list
        }
