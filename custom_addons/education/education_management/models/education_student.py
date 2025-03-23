from odoo import models, fields, api, _

class EducationStudent(models.Model):
    _name = 'education.student'
    _description = 'Education Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence'

    sequence = fields.Integer(string='Sequence')
    # Identitas Siswa
    name = fields.Char(string='Student Name', required=True, tracking=True, default="Rusdi")
    nisn = fields.Char(string='NISN', required=True, tracking=True)
    id_student = fields.Char(string='Student ID', required=True, copy=False, readonly=True, index=True, default='New', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', tracking=True)
    email = fields.Char(string='Student Email', tracking=True)
    phone = fields.Char(string='Student Phone', tracking=True)
    photo = fields.Image(string='Photo')
    
    # Informasi Orang Tua / Wali
    father_name = fields.Char(string='Father Name', tracking=True)
    father_contact = fields.Char(string='Father Contact', tracking=True)
    father_email = fields.Char(string='Father Email', tracking=True)
    mother_name = fields.Char(string='Mother Name', tracking=True)
    mother_contact = fields.Char(string='Mother Contact', tracking=True)
    mother_email = fields.Char(string='Mother Email', tracking=True)
    
    # Informasi Akademik
    classroom_id = fields.Many2one('education.classroom', string='Class', tracking=True, readonly=True)
    
    # Status Siswa
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('dropout', 'Dropout'),
    ], string='Status', tracking=True, compute='_compute_status', store=True)
    
    achievement_ids = fields.One2many('education.student.achievement', 'student_id', string='Academic Achievement', tracking=True)
    
    attendance_ids = fields.One2many('student.attendance.record', 'student_id', string='Attendance Records', tracking=True)
    
    # Attendance Student
    total_absent = fields.Integer(string='Total Absent', help='Total absent for month')
    total_present = fields.Integer(string='Total Present', help='Total present for month')
    total_absent_alpha = fields.Integer(string='Total Alpha', help='Total alpha for month')
    total_absent_sick = fields.Integer(string='Total Sick', help='Total sick for month')
    total_absent_permit = fields.Integer(string='Total Permit', help='Total permit for month')

    @api.depends('classroom_id')
    def _compute_status(self):
        for student in self:
            if student.classroom_id:
                student.status = 'active'
            else:
                student.status = 'draft'
    
    @api.depends('fee_ids.amount_due')
    def _compute_total_fees_due(self):
        for student in self:
            student.total_fees_due = sum(student.fee_ids.mapped('amount_due'))
    
    @api.model_create_multi
    def create(self,vals_list):
        """ Create a sequence for the student model """
        """Optimized create method for students"""
        # Update only records that need an ID
        for vals in vals_list:
            if vals.get('id_student', _('New')) == _('New'):
                vals['id_student'] = self.env['ir.sequence'].next_by_code('education.student')

        # Call super to create records
        students = super(EducationStudent, self).create(vals_list)

        # Bulk create attendance records to optimize performance
        attendance_data = [{
            'student_id': student.id,
            'classroom_id': student.classroom_id.id,
        } for student in students]
        
        if attendance_data:
            self.env['education.student.attendance'].create(attendance_data)

        return students
        
class StudentAttendanceRecord(models.Model):
    _name = 'student.attendance.record'
    _description = 'Student Attendance Record'
    
    student_id = fields.Many2one('education.student', string='Student', readonly=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    subject_id = fields.Many2one('education.subject', string='Subject')
    
    absent = fields.Integer(string='Absent')
    present = fields.Integer(string='Present')
    
    absent_alpha = fields.Integer(string='Alpha')
    absent_sick = fields.Integer(string='Sick')
    absent_permit = fields.Integer(string='Permit')