from odoo import models, fields

class TeacherEmployement(models.Model):
    _name = 'teacher.employement'
    _description = 'Teacher Employement'
    _rec_name = 'nip'
    
    nip = fields.Char(string='NIP', required=True, help='Nomor unik kepegawaian.')
    teacher_id = fields.Many2one('teacher.teacher', string='Data Guru', help='Guru yang bersangkutan.')
    position = fields.Selection([
        ('guru','Guru'),
        ('staff','Staff'),
        ('wakil_kepala_sekolah','Wakil Kepala Sekolah'),
        ('kepala_sekolah','Kepala Sekolah'),
    ],string='Jabatan', required=True, help='Jabatan guru.')
    employement_status = fields.Selection([
        ('magang', 'Magang'),
        ('honorer', 'Honorer'),
        ('kontrak', 'Kontrak'),
        ('tetap', 'Tetap'),
        ('pns', 'PNS'),
    ],string='Status Kepegawaian', required=True, help='Status kepegawaian guru.')
    entry_date = fields.Date(string='Tanggal Masuk', required=True, help='Tanggal masuk guru.')
    active_period = fields.Integer(string='Masa Aktif', required=True, help='Masa aktif guru dalam tahun.')
    basic_salary = fields.Float(string='Gaji Pokok', required=True, help='Gaji pokok guru.')    