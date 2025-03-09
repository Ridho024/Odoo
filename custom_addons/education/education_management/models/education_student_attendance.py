from odoo import models, fields, api

class EducationStudentAttendance(models.Model):
    _name = 'education.student.attendance'
    _description = 'Student Attendance'

    date = fields.Date(string='Date', default=fields.Date.today)
    student_id = fields.Many2one('education.student', string='Student')
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    teacher_id = fields.Many2one('education.teacher', string='Teacher')
    state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ], string='Status', default='present')
    # course_id = fields.Many2one('education.course', string='Course')
    # note = fields.Text(string='Note')
    # check_in = fields.Datetime(string='Check-in Time')
    # check_out = fields.Datetime(string='Check-out Time')
    
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