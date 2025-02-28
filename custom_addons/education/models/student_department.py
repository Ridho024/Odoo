from odoo import models, fields

class StudentDepartment(models.Model):
    _name = 'student.department'
    _description = 'Student Department'
    
    name = fields.Char(string='Nama Jurusan', required=True, help='Nama jurusan.')
    academic_year = fields.Char(string='Tahun Ajar', required=True, help='Tahun akademik jurusan.')