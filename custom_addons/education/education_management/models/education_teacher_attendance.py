from odoo import models, fields

class EducationTeacherAttendance(models.Model):
    _name = 'education.teacher.attendance'
    _description = 'Education Teacher Attendance'
    
    teacher_id = fields.Many2one('res.partner', string='Teacher')
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    date = fields.Date(string='Date')
    subject_id = fields.Many2one('education.subject', string='Subject')
    status = fields.Selection([('present', 'Present'),
                               ('absent', 'Absent')], string='Status', default='absent')
    absent_reason = fields.Selection([('permit', 'Izin'),
                                      ('sick', 'Sick'),
                                      ('alpha', 'Alpha')], string='Absent Reason', default='permit')
    