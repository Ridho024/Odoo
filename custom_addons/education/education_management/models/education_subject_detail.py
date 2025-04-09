from odoo import models, fields

class EducationSubjectDetail(models.Model):
    _name = 'education.subject.detail'
    _description = 'Subject Detail'
    _rec_name = 'studies'

    subject_id = fields.Many2one('education.subject', string='Subject', required=True, ondelete='cascade')
    curriculum_id = fields.Many2one('education.major.curriculum', string='Curriculum', required=True)
    studies = fields.Text(string='Lesson / Study Material', required=True)
