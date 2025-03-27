from odoo import models, fields

class EducationStudentAttendance(models.Model):
    _name = 'education.student.attendance'
    _description = 'Student Attendance'
    _rec_name = 'student_id'
    
    student_id = fields.Many2one('education.student', string='Student', required=True)
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    date = fields.Date(string='Date')
    subject_id = fields.Many2one('education.subject', string='Subject')
    teacher_id = fields.Many2one('res.partner', string='Teacher', domain="[('id', 'in', teacher_ids)]")
    status = fields.Selection([('present', 'Present'),
                               ('absent', 'Absent')], string='Status', default='absent')
    absent_reason = fields.Selection([('permit', 'Izin'),
                                      ('sick', 'Sick'),
                                      ('alpha', 'Alpha')], string='Absent Reason', default='permit')
    teacher_ids = fields.Many2many('res.partner', string='List Subject Teacher', related='subject_id.teacher_ids', readonly=True)