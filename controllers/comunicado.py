import json
from odoo import http
from odoo.http import request

class Comunicado(http.Controller):
    @http.route('/api/comunicado', auth='public', website=False, csrf=False, type='http', methods=['GET'], cors='*')
    def hello(self, **kw):
        estudiantes = request.env['academico.comunicado'].sudo().search([])
        est_list = []
        for est in estudiantes:
            est_list.append({
                'name': est.name,
                'contenido': est.contenido,
                'fecha_publicacion': est.fecha_publicacion.isoformat(), 
            })
        return request.make_response(
            json.dumps({
                'status': 200,
                'message': 'Success',
                'data': est_list
            }),
            headers={'Content-Type': 'application/json'}
        )
