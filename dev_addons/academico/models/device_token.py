from odoo import models, fields

class DeviceToken(models.Model):
    _name = 'academico.token'
    _description = 'academico Token'

    name = fields.Char('Device Name')
    token = fields.Char('Token')
    user_id = fields.Many2one('res.users', 'User')
