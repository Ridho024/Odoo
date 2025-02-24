from odoo import models, fields, api

class EducationClass(models.Model):
    _name = 'education.class'
    _description = 'Class Record'
    
    name = fields.Char(string='Nama', required=True, help='Nama kelas.')
    class_major = fields.Char(string='Jurusan', help='Jurusan kelas jika.')
    academic_year = fields.Integer(string='Tahun Akademik', required=True, help='Tahun akademik kelas.')
    homeroom_teacher = fields.Many2one('education.teacher', string='Wali Kelas', help='Wali kelas.')
    total_student = fields.Integer(string='Total Siswa', help='Jumlah siswa di kelas')
    student_ids = fields.One2many('education.student', 'class_id', string='Siswa Kelas', help='Siswa kelas.')    
    schedule_ids = fields.One2many('class.schedule', 'class_id', string='Jadwal Pelajaran', help='Jadwal pelajaran kelas.')

class EducationClassSchedule(models.Model):
    _name = 'class.schedule'
    _description = 'Class Schedule Record'
    
    class_id = fields.Many2one('education.class', string='Kelas', required=True, help='Kelas pelajaran.')
    day = fields.Selection([
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
        ('minggu', 'Minggu'),], string='Hari', required=True, help='Hari pelajaran.')
    lesson_name = fields.Char(string='Mata Pelajaran', required=True, help='Nama mata pelajaran.')
    teacher_id = fields.Many2one('education.teacher', required=True,string='Guru Pengajar', help='Guru pengajar.')
    start_time = fields.Float(string='Jam Mulai', required=True, help='Jam mulai pelajaran.')
    end_time = fields.Float(string='Jam Selesai', required=True, help='Jam selesai pelajaran.')
    duration = fields.Float(string='Durasi', required=True, help='Durasi pelajaran.')
    classroom = fields.Char(string='Ruang Kelas', required=True,help='Ruang kelas.')

    