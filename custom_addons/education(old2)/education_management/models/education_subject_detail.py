from odoo import models, fields

class EducationSubjectDetail(models.Model):
    _name = 'education.subject.detail'
    _description = 'Subject Detail'
    _rec_name = 'subject_id'
    
    subject_id = fields.Many2one('education.subject', string='Subject', readonly=True)
    curriculum_id = fields.Many2one('education.major.curriculum', string='Curriculum', required=True)
    studies = fields.Text(string='Lesson', required=True)