from odoo import models, fields, api

class EducationStudent(models.Model):
    _name = 'education.student'
    _description = 'Student Record'

    name = fields.Char(string='Nama', required=True, help='Nama lengkap siswa.')
    birth_date = fields.Date(string='Tanggal Lahir', required=True, help='Tanggal lahir siswa.')
    student_id = fields.Char(string='Nomor Induk', required=True, help='Nomor induk siswa atau nomor induk siswa nasional.')
    class_id = fields.Many2one('education.class', string='Kelas', required=True, help='Kelas siswa.')
    parent_name = fields.Char(string='Nama Orang Tua', required=True, help='Nama orang tua siswa.')
    contact = fields.Char(string='Kontak', help='Nomor telepon atau email orang tua / siswa.')
    # attendance_ids = fields.One2many('education.attendance', 'student_id', string='Absensi', help='Absensi siswa.')

