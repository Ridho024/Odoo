from odoo import models, fields, api

class EducationStudentAchievement(models.Model):
    _name = 'education.student.achievement'
    _description = 'Education Student Achievement'
    _rec_name = 'student_id'
    
    name = fields.Char(string='Title', required=True)
    student_id = fields.Many2one('education.student', string='Student', readonly=True)
    date = fields.Date(string='Date', required=True)
    description = fields.Text(string='Description', required=True)
    sertificate = fields.Binary(string='Sertificate', required=True)
    