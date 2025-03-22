from odoo import models, fields, api

class EducationStudentAttendance(models.Model):
    _name = 'education.student.attendance'
    _description = 'Student Attendance'    
    _sql_constraints = [
        ('unique_attendance', 'UNIQUE(student_id)', 'Attendance for this student already exists!')
        ]

    student_id = fields.Many2one('education.student', string='Student')
    nisn = fields.Char(string='NISN', related='student_id.nisn', store=True)
    classroom_id = fields.Many2one('education.classroom', related='student_id.classroom_id', string='Classroom')
    date = fields.Date(string='Date', default=fields.Date.today)
    subject_id = fields.Many2one('education.subject', string='Subject')
    teacher_id = fields.Many2one('education.teacher', string='Teacher')
    attendance_status = fields.Selection([
        ('absent', 'Absent'),
        ('present', 'Present'),
    ], string='Status', default='absent')
    absent_reason = fields.Selection([
        ('alpha', 'Alpha'),  
        ('sick', 'Sick'),
        ('permit', 'Permit'),
    ], string='Reason')
    