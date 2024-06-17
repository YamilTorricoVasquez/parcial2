from odoo import http
from odoo.http import request
import json

class NotificationController(http.Controller):

    @http.route('/save_device_token', type='json', auth='public', methods=['POST'], csrf=False)
    def save_device_token(self, **kwargs):
        token = kwargs.get('token')
        user_id = kwargs.get('user_id')

        # Guarda el token en la base de datos
        if token and user_id:
            request.env['academico.token'].sudo().create({
                'name': 'academico Token',
                'token': token,
                'user_id': int(user_id),
            })
            return {'status': 'success'}
        else:
            return {'status': 'failed', 'message': 'Token or user_id missing'}
