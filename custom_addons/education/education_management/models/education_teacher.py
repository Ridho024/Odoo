from odoo import models, fields, api

class EducationTeacher(models.Model):
    _name = 'education.teacher'
    _description = 'Education Teacher'

    # Identitas guru
    name = fields.Char(string='Teacher Name', required=True)
    id_teacher = fields.Char(string='Teacher ID', required=True, copy=False, readonly=True, default='New')
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
        ], string='Gender')
    photo = fields.Image(string='Photo')
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    
    # Akedemik & Mata Pelajaran
    subject_ids = fields.Many2many('education.course', string='Subjects')
    class_ids = fields.Many2many('education.classroom', string='Assigned Classes')
    
    # Kehadiran dan Evaluasi
    attendance_ids = fields.One2many('education.teacher.attendance', 'teacher_id', string='Attendances Records')
    # grade_ids = fields.One2many('education.grade', 'teacher_id', string='Assigned Grades')
    
    # Data Administrasi
    employement_date = fields.Date(string='Employement Date')
    salary = fields.Monetary(string='Salary')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)
    
    # Status Guru
    status = fields.Selection([
        ('active', 'Active'),
        ('retired', 'Retired'),
        ('resigned', 'Resigned'),
    ], string='Status', default='active')
    
    # @api.model
    # def create(self, vals):
    #     teacher = super(EducationTeacher, self).create(vals)
    #     teacher_attendance = {
    #         'teacher_id': teacher.id,
    #         'classroom_id': teacher.classroom_id.id,
    #     }
    #     self.env['education.teacher.attendance'].create(teacher_attendance)
    #     return teacher
    
    