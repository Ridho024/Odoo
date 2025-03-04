from odoo import models, fields, api

class EducationAssignment(models.Model):
    _name = 'education.assignment'
    _description = 'Student Assignments'
    
    course_id = fields.Many2one('education.course', string='Course', required=True)
    teacher_id = fields.Many2one('education.teacher', string='Assigned By', required=True)
    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    due_date = fields.Date(string='Due Date', required=True)
    attachment = fields.Binary(string='Attachment')
    attachment_name = fields.Char(string='Attachment Name')
    student_ids = fields.Many2many('education.student', string='Assigned To')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ], string='Status', default='assigned')
    grade = fields.Float(string='Grade', readonly=True)
    teacher_notes = fields.Text(string='Teacher Notes')
    
    def action_submit(self):
        self.write({'state': 'submitted'})
        
    def action_grade(self, grade, notes=""):
        self.write({'state': 'graded', 'grade': self.grade, 'teacher_notes': self.notes})

    