from odoo import models, fields, api

class EducationClass(models.Model):
    _name = 'education.class'
    _description = 'Class Record'
    
    name = fields.Char(string='Nama', required=True, help='Nama kelas.')
    teacher_id = fields.Many2one('education.teacher', string='Guru', required=True, help='Guru kelas.')
    student_ids = fields.One2many('education.student', 'class_id', string='Siswa', help='Siswa kelas.')
    class_department = fields.Char(string='Jurusan', help='Jurusan kelas untuk SMA/SMK atau institus kejuruan terkait.')
    homeroom_teacher = fields.Many2one('education.teacher', string='Wali Kelas')
    total_student = fields.Integer(string='Total Siswa')