from odoo import models, fields, api

class StudentClass(models.Model):
    _name = 'student.class'
    _description = 'Student Class'
    
    grade = fields.Selection([
        ('10', 'X'),
        ('11', 'XI'),
        ('12', 'XII'),
        ('13', 'XIII'),], string='Tingkat', help='Tingkat kelas.')
    name = fields.Char(string='Kelas', required=True, help='Nama kelas.')
    department = fields.Many2one('student.department', string='Jurusan', help='Jurusan kelas jika.')
    academic_year = fields.Char(string='Tahun Ajar', required=True, help='Tahun akademik kelas.')
    teacher_id = fields.Many2one('teacher.teacher', string='Wali Kelas',help='Wali kelas.')
    total_student = fields.Integer(string='Total Siswa', help='Jumlah siswa di kelas', readonly=True, compute='_compute_total_student')
    student_ids = fields.One2many('student.student', 'class_id', string='Siswa/Siswi', help='Siswa/siswi kelas.')    
    schedule_ids = fields.One2many('class.schedule', 'class_id', string='Jadwal Pelajaran', help='Jadwal pelajaran kelas.')
    attendance_ids = fields.One2many('class.attendance', 'class_id', string='Absensi Siswa', help='Absensi siswa kelas.')
    
    @api.depends('student_ids')
    def _compute_total_student(self):
        for rec in self:
            rec.total_student = len(rec.student_ids)
    

class ClassSchedule(models.Model):
    _name = 'class.schedule'
    _description = 'Student Class Schedule'
    
    name = fields.Char(string='Mata Pelajaran', required=True, help='Nama mata pelajaran.')
    day = fields.Selection([
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
        ('minggu', 'Minggu'),], string='Hari', required=True, help='Hari pelajaran.')
    teacher_id = fields.Many2one('teacher.teacher', required=True, string='Guru Pengajar', help='Guru pengajar.')
    start_time = fields.Float(string='Jam Mulai', required=True, help='Jam mulai pelajaran.')
    end_time = fields.Float(string='Jam Selesai', required=True, help='Jam selesai pelajaran.')
    duration = fields.Float(string='Durasi', required=True, help='Durasi pelajaran.')
    classroom_id = fields.Many2one('classroom.classroom', string='Ruang Kelas', help='Ruang kelas.')
    class_id = fields.Many2one('student.class', string='Kelas', help='Kelas.')

class StudentAttendance(models.Model):
    _name = 'class.attendance'
    _description = 'Student Attendance'
    _rec_name = 'schedule_id'
    
    schedule_id = fields.Many2one('class.schedule', string='Jadwal Pelajaran', help='Jadwal pelajaran.')
    teacher_id = fields.Many2one('teacher.teacher', string='Guru Pengajar', help='Guru pengajar.')
    student_id = fields.Many2one('student.student', string='Siswa', help='Siswa yang melakukan absen.')
    date = fields.Date(string='Tanggal', help='Tanggal absen.')
    status = fields.Selection([
        ('hadir', 'Hadir'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit'),
        ('alpa', 'Alpa'),], string='Status', help='Status kehadiran siswa.')
    note = fields.Text(string='Catatan', help='Catatan absen siswa.')
    class_id = fields.Many2one('student.class', string='Kelas', help='Kelas.')