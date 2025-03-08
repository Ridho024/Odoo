from odoo import models, fields, api

class EducationStudent(models.Model):
    _name = 'education.student'
    _description = 'Education Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Identitas Siswa
    name = fields.Char(string='Student Name', required=True, tracking=True)
    id_student = fields.Char(string='Student ID', required=True, copy=False, readonly=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('education.student') or 'New', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', tracking=True)
    email = fields.Char(string='Student Email', tracking=True)
    phone = fields.Char(string='Student Phone', tracking=True)
    photo = fields.Image(string='Photo', tracking=True)
    
    # Informasi Orang Tua / Wali
    father_name = fields.Char(string='Father Name', tracking=True)
    father_contact = fields.Char(string='Father Contact', tracking=True)
    father_email = fields.Char(string='Father Email', tracking=True)
    mother_name = fields.Char(string='Mother Name', tracking=True)
    mother_contact = fields.Char(string='Mother Contact', tracking=True)
    mother_email = fields.Char(string='Mother Email', tracking=True)
    
    # Informasi Akademik
    academic_year = fields.Char(string='Academic Year', tracking=True)
    classroom_id = fields.Many2one('education.classroom', string='Class', tracking=True)
    
    # Administrasi Keuangan
    # fee_ids = fields.One2many('education.fee', 'student_id', string='Fee Payments')
    # total_fees_due = fields.Monetary(string='Total Fees Due', compute='_compute_total_fees_due', store=True)
    # currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)
    
    # Status Siswa
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('dropout', 'Dropout'),
    ], string='Status', default='draft', tracking=True)
    
    @api.depends('fee_ids.amount_due')
    def _compute_total_fees_due(self):
        for student in self:
            student.total_fees_due = sum(student.fee_ids.mapped('amount_due'))

    