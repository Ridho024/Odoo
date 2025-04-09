from odoo import models, fields

class EducationStudentAchievement(models.Model):
    _name = 'education.student.achievement'
    _description = 'Education Student Achievement'
    _order = 'date desc'
    
    name = fields.Char(string='Title', required=True)
    student_id = fields.Many2one('education.student', string='Student', required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True)
    description = fields.Text(string='Description')
    certificate = fields.Binary(string='Certificate')
