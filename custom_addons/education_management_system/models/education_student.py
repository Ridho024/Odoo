from odoo import models, fields, api

class EducationStudent(models.Model):
    _name = 'education.student'
    _description = 'Student Record'

    # Student
    student_image = fields.Image(string='Foto', help='Foto siswa.', max_width=128, max_height=128)
    name = fields.Char(string='Nama', required=True, help='Nama lengkap siswa.')
    student_id = fields.Char(string='Nomor Induk', required=True, help='Nomor induk siswa atau nomor induk siswa nasional.')
    birth_date = fields.Date(string='Tanggal Lahir', required=True, help='Tanggal lahir siswa.')
    student_phone_number = fields.Char(string='Nomor Telepon', required=True,help='Nomor telepon siswa.')
    student_email = fields.Char(string='Email', required=True,help='Alamat email siswa.')
    gender = fields.Selection([
        ('laki-laki', 'Laki-laki'),
        ('perempuan', 'Perempuan'),], string='Jenis Kelamin', required=True, help='Jenis kelamin siswa.')
    address = fields.Text(string='Alamat', help='Alamat lengkap siswa.')
    postcal_code = fields.Integer(string='Kode Pos', required=True,help='Kode pos alamat siswa.')
    class_id = fields.Many2one('education.class', string='Kelas', required=True, help='Kelas siswa.')
    
    # Father
    father_name = fields.Char(string='Nama Ayah', required=True, help='Nama lengkap ayah siswa.')
    father_id = fields.Char(string='Nomor Induk Ayah', required=True, help='NIK sesuai kartu keluarga ayah siswa.')
    father_occupation = fields.Char(string='Pekerjaan Ayah', required=True,help='Pekerjaan ayah siswa.')
    father_phone_number = fields.Char(string='Kontak Ayah', required=True,help='Nomor telepon ayah siswa.')
    father_email = fields.Char(string='Email Ayah', required=True,help='Alamat email ayah siswa.')
    
    # Mother
    mother_name = fields.Char(string='Nama Ibu', required=True, help='Nama lengkap ibu siswa.')
    mother_id = fields.Char(string='Nomor Induk Ibu', required=True, help='NIK sesuai kartu keluarga ibu siswa.')
    mother_occupation = fields.Char(string='Pekerjaan Ibu', required=True,help='Pekerjaan ibu siswa.')
    mother_phone_number = fields.Char(string='Kontak Ibu', required=True,help='Nomor telepon ibu siswa.')
    mother_email = fields.Char(string='Email Ibu', required=True,help='Alamat email ibu siswa.')
    
    # attendance_ids = fields.One2many('education.attendance', 'student_id', string='Absensi', help='Absensi siswa.')

