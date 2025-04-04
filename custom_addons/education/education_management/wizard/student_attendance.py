from odoo import models, fields, api

class CreateStudentAttendance(models.TransientModel):
    _name = 'create.student.attendance'
    _description = 'Create student attendance'
    
    student_id = fields.Many2one('education.student', string='Student', required=True)
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    date = fields.Date(string='Date', default=fields.Date.today(), readonly=True)
    subject_id = fields.Many2one('education.subject', string='Subject')
    teacher_id = fields.Many2one('res.partner', string='Teacher', domain="[('id', 'in', teacher_ids)]")
    status = fields.Selection([('present', 'Present'),
                               ('absent', 'Absent')], string='Status', default='absent')
    absent_reason = fields.Selection([('permit', 'Permit'),
                                      ('sick', 'Sick'),
                                      ('alpha', 'Alpha')], string='Absent', default='permit')
    teacher_ids = fields.Many2many('res.partner', string='List Subject Teacher', related='subject_id.teacher_ids', readonly=True)
    
    @api.model
    def create(self, vals):
        """Menyimpan absensi ke model `education.student.attendance`."""
        res = super(CreateStudentAttendance,self).create(vals)
        
        attendance = {
            'student_id': res.student_id.id,
            'classroom_id': res.classroom_id.id,
            'date': res.date,
            'subject_id': res.subject_id.id,
            'teacher_id': res.teacher_id.id,
            'status': res.status,
            'absent_reason': res.absent_reason,
        }
        
        self.env['education.student.attendance'].create(attendance)
        
        return res