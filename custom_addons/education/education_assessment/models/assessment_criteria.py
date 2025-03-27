from odoo import models, fields, api

class AssessmentCriteria(models.Model):
    _name = 'assessment.criteria'
    _description = 'Assessment Criteria'
    
    name = fields.Char(string='Name', required=True)
    weight = fields.Float(string='Weight (%)')
    assessment_id = fields.Many2one('assessment.record', string='Assessment Record')