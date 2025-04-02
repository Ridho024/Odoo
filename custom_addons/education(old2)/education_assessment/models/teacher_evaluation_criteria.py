from odoo import models, fields, api

class TeacherEvaluationCriteria(models.Model):
    _name = 'teacher.evaluation.criteria'
    _description = 'Teacher Evaluation Criteria'
    
    name = fields.Char(string='Criteria Name', required=True)
    weight = fields.Float(string='Weight (%)', help='Criteria weight in persen.')