from odoo import models, fields, api

class StudentStudent(models.Model):
    _name = 'student.student'
    _description = 'Student Record'

    # Personal Information
    name = fields.Char(string='Nama', required=True, help='Nama lengkap siswa sesuai kartu keluarga.')
    nik = fields.Char(string='NIK', required=True, help='Nomor induk kependudukan siswa.')
    nisn = fields.Char(string='NISN', required=True, help='Nomor induk siswa nasional.')
    gender = fields.Selection([
        ('laki-laki', 'Laki-laki'),
        ('perempuan', 'Perempuan'),], string='Jenis Kelamin', required=True, help='Jenis kelamin siswa.')
    birth_date = fields.Date(string='Tanggal Lahir', required=True, help='Tanggal lahir siswa.')
    phone_number = fields.Char(string='Nomor Telepon', required=True,help='Nomor telepon aktif siswa.')
    email = fields.Char(string='Email', required=True,help='Alamat email aktif siswa.')
    address = fields.Text(string='Alamat', required=True, help='Alamat lengkap siswa.')
    postcal_code = fields.Char(string='Kode Pos', required=True,help='Kode pos alamat rumah siswa.')
    student_image = fields.Image(string='Foto', help='Foto siswa.', required=True, max_width=128, max_height=128)
    
    # Father
    father_name = fields.Char(string='Nama Ayah', required=True, help='Nama lengkap ayah siswa.')
    father_nik = fields.Char(string='Nomor Induk Ayah', required=True, help='NIK sesuai kartu keluarga ayah siswa.')
    father_phone_number = fields.Char(string='Nomor telepon Ayah', required=True,help='Nomor telepon aktif ayah siswa.')
    father_email = fields.Char(string='Email Ayah', required=True,help='Alamat email aktif ayah siswa.')
    
    # Mother
    mother_name = fields.Char(string='Nama Ibu', required=True, help='Nama lengkap ibu siswa.')
    mother_nik = fields.Char(string='Nomor Induk Ibu', required=True, help='NIK sesuai kartu keluarga ibu siswa.')
    mother_phone_number = fields.Char(string='Nomor Telepon Ibu', required=True,help='Nomor telepon aktif ibu siswa.')
    mother_email = fields.Char(string='Email Ibu', required=True,help='Alamat email aktif ibu siswa.')
    
    # Class
    class_id = fields.Many2one('student.class', string='Kelas', help='Kelas siswa.')
    
    # Student class action
    def action_student_detail(self):
        return {
            'name': 'Student Detail',
            'view_mode': 'form',
            'res_model': 'student.student',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'current',
        }
    
"""
LIST TODO
1. Model untuk data akademik siswa. 
"""

