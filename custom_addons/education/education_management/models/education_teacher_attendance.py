from odoo import models, fields, api

class EducationTeacherAttendance(models.Model):
    _name = 'education.teacher.attendance'
    _description = 'Teacher Attendance'
    _rec_name = "teacher_id"
    _sql_constraints = [
        ('unique_attendance', 'UNIQUE(teacher_id)', 'Attendance for this teacher already exists!')
        ]
    
    teacher_id = fields.Many2one('res.partner', string="Teacher", required=True, domain="[('is_teacher', '=', True)]")
    nip = fields.Char(string="NIP", related='teacher_id.nip', required=True, store=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today, readonly=True)
    classroom_id = fields.Many2one('education.classroom', string="Classroom")
    subject_id = fields.Many2one('education.subject', string="Subject", domain="[('id', 'in', available_subjects)]")
    attendance_status = fields.Selection([  
        ('absent', 'Absent'),
        ('present', 'Present'),
    ], string='Status', default='absent')
    absent_reason = fields.Selection([
        ('alpha', 'Alpha'),  
        ('sick', 'Sick'),
        ('permit', 'Permit'),
    ], string='Reason')

    # Hanya menampilkan subject yang diajar oleh guru
    available_subjects = fields.Many2many('education.subject',
                                          compute='_compute_available_subjects',
                                          store=False)
    
    @api.depends('teacher_id', 'classroom_id')
    def _compute_available_subjects(self):
        Schedule = self.env['education.schedule']
        for record in self:
            if record.teacher_id and record.classroom_id:
                record.available_subjects = Schedule.search([
                    ('teacher_id', '=', record.teacher_id.id),
                    ('classroom_id', '=', record.classroom_id.id)
                ]).mapped('subject_id')
            else:
                record.available_subjects = []
    
    """
    Menghitung jumlah kehadiran dan absensi guru di attendance.record.
    """            
    @api.model
    def write(self, vals):
        teacher_attendance = super(EducationTeacherAttendance, self).write(vals)
        
        if 'attendance_status' in vals:
            attendance_record = self.env['attendance.record']
            for record in self:
                attendance = attendance_record.search([
                    ('date', '=', record.date),
                    ('teacher_id', '=', record.teacher_id.id),
                ], limit=1)
                
                if attendance:
                    if vals['attendance_status'] == 'absent' and 'absent_reason' in vals:
                        attendance.absent += 1
                        if vals['absent_reason'] == 'alpha':
                            attendance.absent_alpha += 1
                        elif vals['absent_reason'] == 'sick':
                            attendance.absent_sick += 1
                        elif vals['absent_reason'] == 'permit':
                            attendance.absent_permit += 1
                            
                    elif vals['attendance_status'] == 'present':
                        attendance.present += 1
                        
        return teacher_attendance
                