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
    
    """
    Menghitung jumlah kehadiran dan absensi murid di student.attendance.record.
    """            
    @api.model
    def write(self, vals):
        student_attendance = super(EducationStudentAttendance, self).write(vals)
        
        if 'attendance_status' in vals:
            attendance_record = self.env['student.attendance.record']
            for record in self:
                attendance = attendance_record.search([
                    ('date', '=', record.date),
                    ('student_id', '=', record.student_id.id),
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
                        
        return student_attendance