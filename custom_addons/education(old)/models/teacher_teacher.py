from odoo import models, fields, api

class TeacherTeacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teacher Information'
    
    # Personal Information
    name = fields.Char(string='Nama', required=True, help='Nama lengkap.')
    nik = fields.Char(string='NIK', required=True, help='Nomor Induk Kependudukan.')
    gender = fields.Selection([
        ('laki-laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string='Jenis Kelamin', required=True, default='laki-laki', help='Jenis kelamin.')
    birth_date = fields.Date(string='Tanggal Lahir', required=True, help='Tanggal lahir.')
    phone_number = fields.Char(string='Nomor Telepon', required=True,help='Nomor telepon.')
    email = fields.Char(string='Email', required=True,help='Alamat email.')
    address = fields.Char(string='Alamat', required=True,help='Alamat.')
    postcal_code = fields.Char(string='Kode Pos', required=True,help='Kode pos.')
    teacher_image = fields.Image(string='Foto', help='Foto guru.', required=True, max_width=128, max_height=128)
    
    education_ids = fields.One2many('teacher.education', 'teacher_id', string='Riwayat Pendidikan', help='Riwayat pendidikan.')
    training_ids = fields.One2many('teacher.training', 'teacher_id', string='Riwayat Pelatihan', help='Riwayat pelatihan yang pernah diikuti.')
    
class TeacherEducation(models.Model):
    _name = 'teacher.education'
    _description = 'Teacher Education'
    
    name = fields.Char(string='Nama Institusi', required=True, help='Nama institusi.')
    grade = fields.Selection([
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('smk', 'SMK'),
        ('d3', 'D3'),
        ('d4', 'D4'),
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3', 'S3'),
    ], string='Jenjang Pendidikan', required=True, help='Jenjang pendidikan.')
    study_program = fields.Char(string='Program Studi', help='Program studi untuk smk/diploma/sarjana.\n Kosongkan jika jenjang pendidikan adalah sd/smp.')
    graduation_year = fields.Integer(string='Tahun Lulus', required=True, help='Tahun lulus.')
    sertification = fields.Binary(string='Sertifikat', required=True, help='Bukti sertifikasi kelulusan.')
    teacher_id = fields.Many2one('teacher.teacher', string='Guru', help='Guru yang bersangkutan.')

class TeacherTraining(models.Model):
    _name = 'teacher.training'
    _description = 'Teacher Training'
    
    name = fields.Char(string='Nama Pelatihan', required=True, help='Nama pelatihan guru.')
    institution_name = fields.Char(string='Lembaga Pelatihan', required=True, help='Nama institusi atau lembaga pelatihan.')
    training_start_date = fields.Date(string='Tanggal Pelatihan', required=True, help='Tanggal pelatihan.')
    training_end_date = fields.Date(string='Tanggal Selesai Pelatihan', required=True, help='Tanggal selesai pelatihan.')
    training_duration = fields.Integer(string='Durasi Pelatihan', required=True, help='Durasi pelatihan dalam hari.')
    training_sertificate = fields.Binary(string='Bukti Sertifikat', required=True, help='Bukti sertifikat.')
    teacher_id = fields.Many2one('education.teacher', string='Guru', help='Guru yang bersangkutan.')