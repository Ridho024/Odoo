from odoo import models, fields

class MessageWizard(models.TransientModel):
    _name = 'message.wizard'
    _description = 'Popup Message Wizard'

    message = fields.Text(string='Message', readonly=True)
