from odoo import models, fields, api

class EducationTeacher(models.Model):
    _name = 'education.teacher'
    _description = 'Teacher Record'
    
    name = fields.Char(string='Nama', required=True, help='Nama lengkap guru.')
    subject = fields.Char(string='Mata Pelajaran', required=True, help='Mata pelajaran yang diajarkan guru.')
    contact = fields.Char(string='Kontak', help='Nomor telepon atau email guru.')
    class_id = fields.One2many('education.class', 'teacher_id', string='Kelas', help='Kelas yang diajar guru.')