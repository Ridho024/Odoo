from odoo import models, fields, api

class EducationTeacher(models.Model):
    _name = 'education.teacher'
    _description = 'Teacher Record'
    
    # Personal Information
    name = fields.Char(string='Nama', required=True, help='Nama lengkap guru.')
    teacher_image = fields.Image(string='Foto', required=True,help='Foto guru.')
    id_card = fields.Char(string='NIK', required=True, help='Nomor Induk Kependudukan guru.')
    employement_id = fields.Char(string='NIP', required=True, help='Nomor Induk Pegawai guru.')
    gender = fields.Selection([
        ('laki-laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string='Jenis Kelamin', required=True, default='laki-laki', help='Jenis kelamin guru.')
    birth_date = fields.Date(string='Tanggal Lahir', required=True, help='Tanggal lahir guru.')
    phone_number = fields.Char(string='Nomor Telepon', required=True,help='Nomor telepon guru.')
    email = fields.Char(string='Email', required=True,help='Alamat email guru.')
    address = fields.Char(string='Alamat', required=True,help='Alamat guru.')
    postcal_code = fields.Char(string='Kode Pos', required=True,help='Kode pos guru.')
    
    # Employement Affair
    unique_id = fields.Char(string='Nomor Unik Guru', required=True, help='Nomor Unik Guru.')
    position = fields.Selection([
        ('guru','Guru'),
        ('staff','Staff'),
        ('wakil_kepala_sekolah','Wakil Kepala Sekolah'),
        ('kepala_sekolah','Kepala Sekolah'),
    ],string='Jabatan', required=True, help='Jabatan guru.')
    entry_date = fields.Date(string='Tanggal Masuk', required=True, help='Tanggal masuk guru.')
    end_date = fields.Date(string='Tanggal Keluar', required=True,help='Tanggal keluar guru.')
    employement_status = fields.Selection([
        ('magang', 'Magang'),
        ('honorer', 'Honorer'),
        ('kontrak', 'Kontrak'),
        ('tetap', 'Tetap'),
        ('pns', 'PNS'),
    ],string='Status Kepegawaian', required=True, help='Status kepegawaian guru.')
    employement_rank = fields.Selection([
        ('III/a', 'Penata Muda, jabatan fungsional guru pertama yang baru dilantik sebagai PNS.'),
        ('III/b', 'Penata Muda Tingkat I, jabatan fungsional guru pertama'),
        ('IV/a', 'Pembina, jabatan fungsional guru madya'),
        ('IV/b', 'Pembina Tingkat I, jabatan fungsional guru madya'),
        ('IV/c', 'Pembina Utama Muda, jabatan fungsional guru madya'),
        ('IV/d', 'Pembina Utama Muda, jabatan fungsional guru madya'),
        ('IV/e', 'Pembina Utama, jabatan fungsional guru utama'),
    ],string='Golongan/Pangkat', required=True, help='Golongan atau pangkat.')
    basic_salary = fields.Float(string='Gaji Pokok', required=True, help='Gaji pokok guru.')
    