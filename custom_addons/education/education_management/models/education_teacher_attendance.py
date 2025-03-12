from odoo import models, fields

class EducationTeacherAttendance(models.Model):
    _name = 'education.teacher.attendance'
    _description = 'Teacher Attendance'
    _rec_name = "teacher_id"
    
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    teacher_id = fields.Many2one('education.teacher', string="Teacher", required=True)
    course_id = fields.Many2one('education.course', string="Course")
    classroom_id = fields.Many2one('education.classroom', string="Classroom", required=True)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ], string="Attendance Status", required=True, default="present")

    # Metode untuk Menandai Guru Hadir
    def mark_present(self):
        self.write({'status': 'present'})

    # Metode untuk Menandai Guru Tidak Hadir
    def mark_absent(self):
        self.write({'status': 'absent'})

    # Metode untuk Menandai Guru Terlambat
    def mark_late(self):
        self.write({'status': 'late'})

    # Metode untuk Menandai Guru Izin
    def mark_excused(self):
        self.write({'status': 'excused'})
