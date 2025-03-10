from odoo import models, fields, api

class EducationClassroom(models.Model):
    _name = 'education.classroom'
    _description = 'Classroom Information'
    
    name = fields.Char(string='Classroom Name', required=True)
    code = fields.Char(string='Class Code', required=True, copy=False, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('education.classroom'))
    capacity = fields.Integer(string='Capacity', required=True, help='Maximum number of students allowed in the class')
    teacher_id = fields.Many2one('education.teacher', string='Homeroom Teacher', help='Main teacher responsible for class')
    student_ids = fields.One2many('education.student', 'classroom_id', string='Enrolled Student')
    subject_ids = fields.Many2many('education.course', string='Subjects Taught')
    schedule_ids = fields.One2many('education.schedule', 'classroom_id', string='Class Schedule')
    location = fields.Char(string='Location', help='Classroom location in the school building')
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color')
    
    