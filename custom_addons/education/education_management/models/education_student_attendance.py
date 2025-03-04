from odoo import models, fields, api

class EducationStudentAttendance(models.Model):
    _name = 'education.student.attendance'
    _description = 'Student Attendance'

    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    classroom_id = fields.Many2one('education.classroom', string='Classroom', required=True)
    course_id = fields.Many2one('education.course', string='Course', required=True)
    student_id = fields.Many2one('education.student', string='Student', required=True)
    teacher_id = fields.Many2one('education.teacher', string='Teacher', required=True)
    state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ], string='Attendance Status', required=True, default='present')
    note = fields.Text(string='Note')
    check_in = fields.Datetime(string='Check-in Time')
    check_out = fields.Datetime(string='Check-out Time')
    
    # Metode untuk Menandai Siswa Hadir
    def mark_present(self):
        self.write({'status': 'present'})

    # Metode untuk Menandai Siswa Tidak Hadir
    def mark_absent(self):
        self.write({'status': 'absent'})

    # Metode untuk Menandai Siswa Terlambat
    def mark_late(self):
        self.write({'status': 'late'})

    # Metode untuk Menandai Siswa Izin
    def mark_excused(self):
        self.write({'status': 'excused'})