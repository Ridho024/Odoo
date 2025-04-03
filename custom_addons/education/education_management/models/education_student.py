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
    attendance_ids = fields.One2many('education.student.attendance', 'student_id', string='Attendances')
    
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
        return super(EducationStudent, self).create(vals_list)
    
    def action_create_attendance(self):
        """This function is called when the user clicks the
            'Create Attendance' button on a student's list view. It opens a
            new wizard to compose and create and attendance message."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Student Attendance'),
            'res_model': 'wizard.student.attendance',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_student_id': self.id,
                'default_classroom_id': self.classroom_id.id,
                },
        }
    
    def action_create_student_card(self):
        return (self.env.ref('education_management.action_student_id_card_report').report_action(self))
    
    def action_set_to_dropout(self):
        self.status = 'dropout'
    
class WizardStudentAttendance(models.TransientModel):
    _name = 'wizard.student.attendance'
    _description = 'Wizard student attendance'
    
    student_id = fields.Many2one('education.student', string='Student', required=True)
    classroom_id = fields.Many2one('education.classroom', string='Classroom')
    date = fields.Date(string='Date', default=fields.Date.today())
    subject_id = fields.Many2one('education.subject', string='Subject')
    teacher_id = fields.Many2one('res.partner', string='Teacher', domain="[('id', 'in', teacher_ids)]")
    status = fields.Selection([('present', 'Present'),
                               ('absent', 'Absent')], string='Status', default='absent')
    absent_reason = fields.Selection([('permit', 'Permit'),
                                      ('sick', 'Sick'),
                                      ('alpha', 'Alpha')], string='Absent', default='permit')
    teacher_ids = fields.Many2many('res.partner', string='List Subject Teacher', related='subject_id.teacher_ids', readonly=True)
    
    @api.model
    def create(self, vals):
        """Menyimpan absensi ke model `education.student.attendance`."""
        res = super(WizardStudentAttendance,self).create(vals)
        
        attendance_date = {
            'student_id': res.student_id.id,
            'classroom_id': res.classroom_id.id,
            'date': res.date,
            'subject_id': res.subject_id.id,
            'teacher_id': res.teacher_id.id,
            'status': res.status,
            'absent_reason': res.absent_reason,
        }
        
        self.env['education.student.attendance'].create(attendance_date)
        
        return res