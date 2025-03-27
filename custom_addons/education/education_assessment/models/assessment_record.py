from odoo import models, fields

class AssessmentRecord(models.Model):
    _name = 'assessment.record'
    _description = 'Student Assessment Record'
    
    name = fields.Char(name='Name', required=True)
    category_id = fields.Many2one('assessment.category', string='Category')
    subject_id = fields.Many2one('education.subject', string='Subject')
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    teacher_id = fields.Many2one('res.partner', string='Teacher', domain=[('is_teacher', '=', True)], help='Teacher who give the assessment')
    date = fields.Date(string='Date', default= fields.Date.today())
    asessment_criteria_ids = fields.One2many('assessment.criteria', 'assessment_id', string='Assessment Criteria')
    assessment_result_ids = fields.One2many('assessment.result', 'assessment_id', string='Assessment Results')  