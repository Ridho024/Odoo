from odoo import models, fields, api

class EducationStudentAttendance(models.Model):
    _name = 'education.student.attendance'
    _description = 'Student Attendance'
    _rec_name = 'student_id'
    
    student_id = fields.Many2one('education.student', string='Student', required=True, help='Student name')
    classroom_id = fields.Many2one('education.classroom', string='Classroom', required=True)
    date = fields.Date(string='Date', required=True)
    subject_id = fields.Many2one('education.subject', string='Subject', required=True)
    teacher_id = fields.Many2one('res.partner', string='Teacher', domain="[('id', 'in', teacher_ids)]", required=True)
    status = fields.Selection([('present', 'Present'),
                               ('absent', 'Absent')], string='Status', default='absent', required=True)
    absent_reason = fields.Selection([('permit', 'Permit'),
                                      ('sick', 'Sick'),
                                      ('alpha', 'Alpha')], string='Absent Reason')
    
    teacher_ids = fields.Many2many('res.partner', string='List Subject Teacher', compute='_compute_teachers', store=False)
    
    @api.depends('subject_id')
    def _compute_teachers(self):
        for record in self:
            record.teacher_ids = record.subject_id.teacher_ids if record.subject_id else False