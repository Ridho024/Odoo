from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit ='res.partner'
    
    is_teacher = fields.Boolean(string='Is Teacher')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')
                               ], string='Gender')
    # subject_ids = fields.Many2many('education.subject', string='Subjects')
    class_ids = fields.Many2many('education.classroom', string='Assigned Classes')
    
    # Education Management
    major_ids = fields.Many2many('education.major', string='Major Assigned')
    class_ids = fields.Many2many('education.classroom', string='Class Assigned')
    
    #Administration
    nip = fields.Char(string='NIP')