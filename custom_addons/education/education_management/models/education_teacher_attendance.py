from odoo import models, fields, api

class EducationTeacherAttendance(models.Model):
    _name = 'education.teacher.attendance'
    _description = 'Education Teacher Attendance'
    _rec_name = 'teacher_id'
    
    classroom_id = fields.Many2one('education.classroom', string='Classroom', required=True)
    subject_id = fields.Many2one('education.subject', string='Subject')
    teacher_id = fields.Many2one('res.partner', string='Teacher', required=True)
    date = fields.Date(string='Date', default=fields.Date.today())
    status = fields.Selection([('present', 'Present'),
                               ('absent', 'Absent')], string='Status', default='absent')
    absent_reason = fields.Selection([('permit', 'Permit'),
                                      ('sick', 'Sick'),
                                      ('alpha', 'Alpha')], string='Absent Reason', default='permit')
    teacher_ids = fields.Many2many('res.partner', string='Subject Teachers', compute='_compute_teachers', store=False)
    
    @api.depends('subject_id')
    def _compute_teachers(self):
        for record in self:
            record.teacher_ids = record.subject_id.teacher_ids if record.subject_id else False