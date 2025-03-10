from odoo import models, fields, api

class EducationCourse(models.Model):
    _name = 'education.course'
    _description = 'Course Information'
    
    name = fields.Char(string='Course Name', required=True)
    code = fields.Char(string='Course Code', required=True, copy=True, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('education.course') or 'New')
    description = fields.Text(string='Description')
    duration = fields.Integer(string='Duration (hours)', help='Total hours required for this course')
    schedule_ids = fields.One2many('education.schedule', 'course_id', string='Schedules')
    classroom_ids = fields.Many2many('education.classroom', string='Classrooms')
    teacher_id = fields.Many2one('education.teacher', string='Instructor', required=True, help="Main instructor for this course")
    assignment_ids = fields.One2many('education.assignment', 'course_id', string='Assigments')
    exam_ids = fields.One2many('education.exam', 'course_id', string='Exams')
    category_id = fields.Many2one('education.course.category', string='Category')
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color')
