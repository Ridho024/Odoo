from odoo import models, fields, api

class AssessmentCategory(models.Model):
    _name = 'assessment.category'
    _description = 'Student Assessment Category'
    
    name = fields.Char(string='Name', required=True)
    _description = fields.Text(string='Description')